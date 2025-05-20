import re
import nltk
from nltk.tokenize import word_tokenize     # tokenizes input text into individual words
from nltk.corpus import stopwords           # removes common words (like 'the', 'and') that don't add meaning
from nltk.stem import WordNetLemmatizer     # reduces words to their base form ('driving' > 'drive')

nltk.download('punkt')          # tokenizer model
nltk.download('stopwords')      # list of stop words
nltk.download('wordnet')        # dictionary used for lemmatization

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    # make input lower case and tokenize
    tokens = word_tokenize(text.lower())

    # remove non-alphabetic tokens
    alpha_tokens = [word for word in tokens if word.isalpha()]

    # remove stopwords
    filtered_tokens = [word for word in alpha_tokens if word not in stop_words]

    # lemmatize
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    return lemmatized_tokens

def extract_filters(text):
    tokens = preprocess(text)
    text = text.lower()

    # dict to check mentions

    filters = {
        'automatic': 'automatic' in tokens,
        'manual': 'manual' in tokens,
        'diesel': 'diesel' in tokens,
        'petrol': 'petrol' in tokens,
        'electric': 'electric' in tokens,
        '4x4': '4x4' in text,
        'awd': 'awd' in tokens,
        'fwd': 'fwd' in tokens,
        'rwd': 'rwd' in tokens,
        'left': 'left' in tokens,
        'right': 'right' in tokens,
        'min_year': None,
        'max_year': None,
    }

    # tries to find mentions of year range
    match_range = re.search(r'(?:from|between)?\s*(\d{4})\s*(?:to|and|-)\s*(\d{4})', text)

    # set dict values
    if match_range:
        y1, y2 = int(match_range.group(1)), int(match_range.group(2))
        filters['min_year'] = min(y1, y2)
        filters['max_year'] = max(y1, y2)

    # individual year mentions
    min_patterns = r'(?:from|after|since|at\s+least|newer\s+than)\s+(\d{4})'
    max_patterns = r'(?:before|until|up\s+to|at\s+most|older\s+than|no\s+later\s+than)\s+(\d{4})'

    min_years = [int(y) for y in re.findall(min_patterns, text)]
    max_years = [int(y) for y in re.findall(max_patterns, text)]

    # combine with existing range if present
    if min_years:
        filters['min_year'] = max(min_years) if filters['min_year'] is None else max(filters['min_year'], max(min_years))
    if max_years:
        filters['max_year'] = min(max_years) if filters['max_year'] is None else min(filters['max_year'], min(max_years))

    return filters

def build_query(user_input):
    filters = extract_filters(user_input)
    where_clauses = []
    params = []
    string_query = []

    # transmission
    if filters['automatic']:
        where_clauses.append('transmission = %s')
        params.append('automatic')
        string_query.append('transmission = automatic')
    elif filters['manual']:
        where_clauses.append('transmission = %s')
        params.append('manual')
        string_query.append('transmission = manual')

    # fuel
    for fuel in ['diesel', 'petrol', 'electric']:
        if filters[fuel]:
            where_clauses.append('fuel_type = %s')
            params.append(fuel)
            string_query.append(f'fuel_type = {fuel}')

    # drive
    for drive in ['4x4', 'awd', 'fwd', 'rwd']:
        if filters[drive]:
            where_clauses.append('LOWER(drive_type) = %s')
            params.append(drive)
            string_query.append(f'LOWER(drive_type) = {drive}')

    # steering
    for side in ['left', 'right']:
        if filters[side]:
            where_clauses.append('LOWER(steering_side) = %s')
            params.append(side)
            string_query.append(f'LOWER(steering_side) = {side}')

    # years
    if filters['min_year']:
        where_clauses.append('year >= %s')
        params.append(filters['min_year'])
        string_query.append(f'year >= {filters["min_year"]}')
    if filters['max_year']:
        where_clauses.append('year <= %s')
        params.append(filters['max_year'])
        string_query.append(f'year <= {filters["max_year"]}')

    base_query = 'SELECT * FROM cars'
    if where_clauses:
        base_query += ' WHERE ' + ' AND '.join(where_clauses)

    final_string = 'SELECT * FROM cars'

    if string_query:
        final_string += ' \nWHERE ' + ' \nAND '.join(string_query)


    return base_query, params, final_string

# query, params, final_string = build_query("I want an electric, automatic car with right-hand steering made after 2020")
# print(query)
# print(params)
# print(final_string)

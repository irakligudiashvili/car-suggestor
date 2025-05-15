import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))

def process_text(text):
    # Tokenize
    words = word_tokenize(text)

    # Remove stopwords
    words = [word for word in words if word.lower() not in stop_words]

    # Lemmatize
    words = [WordNetLemmatizer().lemmatize(word) for word in words]

    # Group
    words = [word for word in words if word.isalpha()]
    print(words)
    return words
from dotenv import load_dotenv
import os
import random
import psycopg2

brands = ['Toyota', 'Honda', 'Ford', 'BMW', 'Audi', 'Nissan']
years = list(range(2014, 2024))
drive_types = ['FWD', 'RWD', '4x4', 'AWD']
transmissions = ['automatic', 'manual']
fuels = ['petrol', 'diesel', 'electric']
steering = ['left', 'right']

pros = [
    'Comfortable',
    'Durable',
    'Fuel-efficient',
    'Reliable',
    'Spacious',
    'Safe',
    'Sporty',
    'Quiet',
    'Powerful',
    'Easy to park',
    'Stylish',
    'Tech-savvy',
    'Off-road capable',
    'Smooth ride',
    'Fast acceleration',
    'All-weather capable',
    'Low maintenance',
    'Great handling',
    'Eco-friendly',
    'Towing capable'
]

# https://www.edmunds.com/sedan/

descriptions = [
    '''
    A well-built small sedan, with plenty of space inside and enough standard technology and safety features to easily justify its price. Slow acceleration is a bummer, but overall it's a smart pick for an affordable small sedan. 
    ''',
    '''
    Boasts praiseworthy performance, high fuel economy, excellent passenger space and a refined design. There are a few minor drawbacks, such as elevated road noise on the highway, but overall the Civic is a great pick for a small sedan. 
    ''',
    '''
    An all-hybrid lineup and it makes perfect sense for this moment. Besides its great mpg, the Camry has a roomy and comfortable cabin, many helpful technology features, and just enough athleticism and style to make it not boring. It's a great pick for a midsize sedan. 
    ''',
    '''
    Bold style, excellent ride comfort and spacious cabin. High fuel economy is another big bonus. Performance from the base engine is lacking, and some shoppers may balk at the price, but overall we highly recommend the Crown for sedan shoppers seeking something different from the norm. 
    ''',
    '''
    Among entry-level luxury cars, stands out for its well-rounded nature. It rides and steers with composure, accelerates briskly, has an upscale cabin and can be fitted with many premium features. 
    ''',
    '''
    Powerful and boldly designed, but it misses its mark in a few areas. Other players have made larger strides in regards to technology. Unfortunately, "benchmark" is no longer one of the descriptors that come to mind. 
    ''',
    '''
    Luxury and comfort are the undisputed strengths. It has an incredibly smooth ride and a classy and well-built cabin. The E-Class is more expensive than its rivals, but it's easy to see why. 
    ''',
    '''
    When it comes to comfort and refinement on four wheels, it really doesn't get much better. It's proven itself one of the best cars on the road, with a luxuriously appointed interior and state-of-the-art in-car tech and driver aids. "The best or nothing" indeed. 
    ''',
    '''
    It's not hard to see where all the money has gone. Feels on a different level than most other luxury sedans, with an interior that feels as good as it looks. Technology features are lacking, but that's the only real weak spot. 
    ''',
    '''
    A hugely impressive little sport sedan that we'd shop against any of today's hot hatches. Overall performance is nearly unparalleled among front-wheel-drive cars thanks to a strong engine, nimble handling and some of the best steering you'll find on the road today. 
    ''',
    '''
    The shot of adrenaline that the brand has needed for so long. It's a gorgeous hot hatch that strikes a wonderful balance between sport compact and entry-level luxury. If you're looking for all the thrills and precise driving of a Honda Civic Type R but crave something a bit more refined, then the Integra Type S is the perfect answer. 
    ''',
    '''
    It's not cheap, but feels like two cars for the money. Around town, it's an extremely comfortable and well-crafted luxury wagon. But push the RS button on the steering wheel and the RS 6 becomes a rewarding and comically quick performance car. 
    ''',
    '''
    A sleek four-door coupe that will happily whisk you around town or across the continent with both grace and pace. If the M8 Gran Coupe is a bit too in your face and a Bentley Flying Spur screams "Russian oligarch" to you, the Alpina will hit the spot. 
    ''',
    '''
    You're going to find a lot to like. It's available as a roomy sedan or practical hatchback and offers a lineup of engines that provide either high mpg or sporty performance. Pricing might be a concern — the Civic is one of the more expensive models in its class — but overall we think you're getting a solid return on your purchase. 
    ''',
    '''
    Has the same appealing qualities as the regular Grand Highlander along with improved fuel economy. There are two versions: Choose the standard Hybrid if you want to maximize fuel efficiency, or opt for the Hybrid Max if you want the most powerful version of the Grand Highlander. 
    ''',
    '''
    This Hybrid is sleek and stylish, but even more exciting are its substantial all-electric range, high fuel economy and pleasing driving characteristics. But the latest Prius does suffer from lackluster space for rear passengers and cargo. 
    ''',
    '''
    The Hybrid is easy to drive and provides sufficient all-electric range. Even those who don't know the ins and outs of a plug-in hybrid will be able to take advantage of its pleasing comfort and value. 
    ''',
    '''
    Admirably combines high fuel efficiency with luxurious accommodations. We're not as fond of the distracting infotainment interface, however. 
    ''',
    '''
    Took what was already one of the best luxury sedans on the road and made it quicker, more efficient and (marginally) less expensive. The only catches here: It's more expensive than its rivals and it fails to look the part from the outside. It also prioritizes passenger space over cargo space almost to a fault. 
    ''',
    '''
    One of the best luxury SUVs on sale today. It brings the heat with a top-notch interior, exceptional build quality, helpful technology features and a diverse lineup of engines. This is a luxury SUV that quietly executes its job with ease. 
    '''
]

def generate_insert_statement(car):
    return f'''
    INSERT INTO cars (
        brand, year, drive_type, transmission, fuel_type, steering_side, pros, description, img_url, price
    ) VALUES (
        '{car['brand']}', {car['year']}, '{car['drive_type']}', '{car['transmission']}', '{car['fuel_type']}', '{car['steering_side']}', ARRAY{car['pros']}, '{car['description'].replace("'", "''")}', '{car['img_url']}', '{car['price']}'
    )
    '''

sql_statements = []

def generate():
    conn = psycopg2.connect(
        host=os.getenv('HOST'),
        dbname=os.getenv('DBNAME'),
        user=os.getenv('USER'),
        port=os.getenv('PORT'),
        password=os.getenv('PASSWORD')
    )

    cur = conn.cursor()

    for _ in range(50):
        car = {
            'brand': random.choice(brands),
            'year': random.choice(years),
            'drive_type': random.choice(drive_types),
            'transmission': random.choice(transmissions),
            'fuel_type': random.choice(fuels),
            'steering_side': random.choice(steering),
            'pros': random.sample(pros, k=random.randint(3, 12)),
            'description': random.choice(descriptions).strip(),
            'img_url': None,
            'price': random.randint(5000, 100000)
        }

        car['pros'] = str([p for p in car['pros']])

        cur.execute(generate_insert_statement(car))

    conn.commit()
    cur.close()
    conn.close()
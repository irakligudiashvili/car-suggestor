from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import db
import nltk_analyzer

all_cars = db.fetch_all_cars()

def format_cars(cars):
    formatted = []

    for car in cars:
        brand, year, drive_type, transmission, fuel_type, steering_side, pros, description, img_url, price = car
        pros_list = ', '.join(pros)

        formatted.append(html.Div([
            html.H3(f'{brand} - {year}'),
            html.P(f'Drive: {drive_type}, Transmission: {transmission}, Fuel: {fuel_type}, Steering: {steering_side}'),
            html.P(f'Pros: {pros_list}'),
            html.P(description)
        ]))

    return formatted

def handle_empty():
    formatted = []

    formatted.append(html.Div([
            html.H3('No matching cars found'),
            html.P('Have you tried lowering your standards')
        ], style={'text-align': 'center'})
    )

    return formatted

def find_relevant_cars(user_input):
    if not user_input:
        return all_cars

    filtered = []

    for car in all_cars:
        brand, year, drive_type, transmission, fuel_type, steering_side, pros, description, img_url, price = car

        car_text = f'{brand} {year} {drive_type} {transmission} {fuel_type} {steering_side} {" ".join(pros)} {description}'.lower()

        if any(word in car_text for word in user_input):
            filtered.append(car)

    return filtered

app = Dash()

app.layout = html.Div([
    html.H1("Dash Car Finder", style={'text-align': 'center'}),
    html.Div([
        html.Div([
            dcc.Textarea(
                id='user-input',
                placeholder='Describe your dream car...',
                style={'height': '150px', 'resize': 'none', 'padding': '5px', 'box-sizing': 'border-box'}
            ),
            html.Button(
                'Submit',
                id='submit-button',
                n_clicks=0
            ),
            html.Div(
                id='output-container',
                style={'padding': '20px', 'background-color': '#242E40', 'color': 'white', 'box-sizing': 'border-box'}
            )
        ], style={'padding': '20px', 'display': 'flex', 'flex-direction': 'column', 'width': '80%', 'gap': '10px'}),
        html.Div(
            id='car-container',
            children=format_cars(all_cars),
            style={'padding': '10px', 'background-color': '#242E40', 'color': 'white', 'width': '80%', 'box-sizing': 'border-box'}
        )
    ], style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-items': 'center'})

])

@app.callback(
    Output('output-container', 'children'),
    Output('car-container', 'children'),
    Input('submit-button', 'n_clicks'),
    State('user-input', 'value')
)

def update_input(n_clicks, user_input):
    if n_clicks > 0 and user_input:
        processed_input = nltk_analyzer.process_text(user_input)
        matching_cars = find_relevant_cars(processed_input)

        if not matching_cars:
            return f'Results for "{processed_input}"', handle_empty()

        return f'Results for: "{processed_input}"', format_cars(matching_cars)

    return "", format_cars(all_cars)

if __name__ == '__main__':
    app.run(debug=True, port=8050)
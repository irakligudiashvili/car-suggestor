from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import db
import nltk_analyzer
import nltk_matcher

all_cars = db.fetch_all_cars()

def format_cars(cars):
    formatted = []

    for car in cars:
        brand, year, drive_type, transmission, fuel_type, steering_side, pros, description, img_url, price = car
        pros_list = ', '.join(pros)

        formatted.append(html.Div([
            html.Div(
                style={'min-width': '120px', 'min-height': '150px', 'background-color': '#D9D9D9', 'border-radius': '15px'}
            ),
            html.Div([
                html.H3(f'{brand} - {year}'),
                html.P(f'Drive: {drive_type}, Transmission: {transmission}, Fuel: {fuel_type}, Steering: {steering_side}'),
                html.P(f'Pros: {pros_list}'),
                html.P(description)
            ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '5px'}),
        ], style={'background-color': '#232C39', 'border-radius': '15px', 'width': '98%', 'display': 'flex', 'gap': '15px', 'padding': '10px', 'box-sizing': 'border-box'}))

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
    query, params, readable_sql = nltk_matcher.build_query(user_input)
    return db.fetch_relevant_cars(query, params), readable_sql

app = Dash()

app.layout = html.Div([
    html.Div([
      html.Div(
          id='car-container',
          children=format_cars(all_cars),
          style={'width': '700px', 'color': 'white', 'height': '750px', 'overflow-y': 'scroll', 'display': 'flex', 'flex-direction': 'column', 'gap': '20px'}
      )
    ], style={'overflow': 'hidden', 'padding': '20px', 'border-box': 'box-sizing', 'width': '700px', 'height': '750px', 'background-color': '#141C25', 'border-radius': '25px'}
    ),

    html.Div([
        html.H1(children='Dash Car Finder', style={'color': 'white', 'text-align': 'center'}),
        html.Div([
            html.Div([
                html.Div([
                    dcc.Textarea(
                        id='user-input',
                        placeholder='Describe your dream car...',
                        style={'height': '100%', 'width': '100%', 'resize': 'none', 'padding': '5px', 'box-sizing': 'border-box', 'border-radius': '10px'}
                    ),
                    html.Div(
                    )
                ], style={'background-color': '#181818','border-color': '#00FF51', 'border-style': 'solid', 'width': '450px', 'height': '225px', 'border-radius': '15px', 'padding': '10px', 'box-sizing': 'border-box'}),
                html.Button(
                    'Search',
                    id='submit-button',
                    n_clicks=0,
                    style={'width': '450px', 'height': '50px', 'background-color': '#D9D9D9',  'border-color': '#00FF51', 'border-style': 'solid', 'border-radius': '20px', 'font-weight': 'bolder', 'font-size': '1.25rem'}
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '25px'}),
            html.Div(
                id='output-container',
                style={'height': '300px', 'width': '250px', 'background-color': '#D9D9D9', 'box-sizing': 'border-box', 'padding': '5px', 'border-color': '#07F2E6', 'border-style': 'solid', 'border-radius': '10px', 'font-size': '0.75rem', 'word-wrap': 'break-word', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
            )
        ], style={'display': 'flex', 'gap': '40px'})
    ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '100px'})

], style={'background-color': '#0D1318', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'min-height': '100vh', 'gap': '200px'})

@app.callback(
    Output('output-container', 'children'),
    Output('car-container', 'children'),
    Input('submit-button', 'n_clicks'),
    State('user-input', 'value')
)

def update_input(n_clicks, user_input):
    if n_clicks > 0 and user_input:
        matching_cars, readable_query = find_relevant_cars(user_input)

        if not matching_cars:
            return html.Pre(f'{readable_query}'), handle_empty()

        return html.Pre(f'{readable_query}'), format_cars(matching_cars)

    return "", format_cars(all_cars)

if __name__ == '__main__':
    app.run(debug=True, port=8050)
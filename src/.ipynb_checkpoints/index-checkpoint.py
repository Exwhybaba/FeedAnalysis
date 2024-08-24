import pandas as pd
import dash
import dash_table
from dash.dependencies import Input, Output, State, ALL
from dash import dcc, html
import random
import string
from datetime import datetime

# Load data
path = r"C:\Users\HomePC\Documents\HTMLcSS\Nutrition\Data\ingredient.csv"
dfx = pd.read_csv(path)
dfx.drop(columns="PRICE/KG", inplace=True)

# Define columns, with Quantity right after INGREDIENT
columns = [
    'INGREDIENT', 'QUANTITY', 'PRICE/KG', 'QUANTITY PRICE', 'DRY MATTER', 'CP', 'FAT', 'FIBRE', 'CAL.', 'PHOS.TOTAL',
    'AVAIL PHOS', 'ME/POULT', 'ME/SWINE', 'METH', 'CYSTINE', 'METH+CYST',
    'LYSINE', 'TRYPTOPHAN', 'THREONINE', 'VIT A IU/GM', 'VIT D3 IU/GM',
    'VIT E IU/GM', 'RIBOFLAVIN', 'PANTO ACID', 'CHOLINE', 'B 12', 'NIACIN',
    'XANTHOPYL', 'SALT', 'SODIUM', 'POTASSIUM', 'MAGNESIUM', 'SULPHUR',
    'MANGANESE', 'IRON', 'COPPER', 'ZINC', 'SELENIUM', 'IODINE', 'LINOLEIC A'
]

# Create a DataFrame for the main table
df = pd.DataFrame(columns=columns)

# Default data for the vitamins/minerals table
default_data = {
    "vitamin/mineral": [
        "Vitamin A IU/GM", "Vitamin D3 IU/GM", "Vitamin E IU/GM", "Riboflavin",
        "Pantothenic acid", "Choline", "Vitamin B 12", "Niacin",
        "Xantophyl", "Linoleic acid", "Salt", "Sodium", "Potassium",
        "Magnesium", "Sulphur", "Manganese", "Iron", "Copper", "Zinc",
        "Selenium", "Iodine"
    ],
    "PRICE/KG": [0] * 21,  
    "QUANTITY": [0] * 21,  
    "AMOUNT": [0] * 21,    
}

# Convert default_data to DataFrame for easy manipulation
df2 = pd.DataFrame(default_data)

# Create options for the dropdown from the vitamins list
dropdown_options = [{'label': vit, 'value': vit} for vit in default_data['vitamin/mineral']]

# Initialize Dash app
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div(children=[
    html.Div(children=[
        html.Div(id="sidebar", children=[
            dcc.Dropdown(
                id='ingredient_dd',
                options=[{'label': ingredient, 'value': ingredient} for ingredient in dfx['INGREDIENT'].unique()],
                multi=True, placeholder="Select ingredients..."
            ),

            html.Div(children=[
                dcc.Dropdown(
                    id='vit_dd',
                    options=dropdown_options,
                    multi=True, placeholder="Select vitamins/minerals...")
            ], style={"position": "relative", "top": "50px"})

        ], className="sidebox"),

        html.Div(children=[
            html.Div(id="topbar"),
            html.Div(children=[
                html.Div(
                    id="firstbar", children=[
                        dash_table.DataTable(
                            id='ingredient_table',
                            columns=[{'name': col, 'id': col, 'editable': col in ['QUANTITY', 'PRICE/KG']} for col in columns],
                            data=[],  # Initially empty
                            style_table={
                                'overflowY': 'auto',  # Enable vertical scroll
                                'overflowX': 'auto',  # Enable horizontal scroll
                                'height': '100%',     # Ensure the table fills the container height
                                'width': '100%',      # Ensure the table fills the container width
                            },
                            style_cell={
                                'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                                'whiteSpace': 'normal',
                                'textAlign': 'left',
                                'padding': '5px'
                            },
                            style_data={
                                'height': 'auto',  # Allow rows to adjust height but limit it below
                                'maxHeight': '65px',  # Set a max height for each row
                                'overflow': 'hidden',  # Hide overflow to prevent table expansion
                            },
                            page_current=0,  # Start on the first page
                            page_size=6,     # Six rows per page
                            page_action="native",  # Native pagination mode
                            style_header={
                                'backgroundColor': 'lightgrey',
                                'fontWeight': 'bold'
                            }
                        ),

                        html.Div(children=[
                            dash_table.DataTable(
                                id='minerals-vitamins-table',
                                columns=[
                                    {"name": "Ingredients", "id": "Ingredients"},
                                    {"name": "QUANTITY", "id": "QUANTITY"},
                                    {"name": "PRICE/KG", "id": "PRICE/KG"},
                                    {"name": "AMOUNT", "id": "AMOUNT"}
                                ],
                                data=[],  
                                editable=True,
                                row_deletable=True,
                                style_table={'height': '200px', 'overflowY': 'auto', 'overflowX': 'auto'},
                                style_cell={'textAlign': 'left', 'fontFamily': 'Arial', 'fontSize': 15},
                                style_header={'backgroundColor': 'lightgrey', 'color': 'black', 'fontWeight': 'bold'})
                        ], style={"position": "relative", "top": "145px"})
                    ]),

                html.Div(
                    id="secondbar",
                    style={
                        'height': '475px',
                        'overflowY': 'auto',
                        'padding': '10px',
                        'border': '1px solid #ddd',
                        'boxSizing': 'border-box',
                    },
                    children=[
                        # Date and Time
                        html.Div(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style={'fontWeight': 'bold', 'marginBottom': '10px'}),

                        # Feed Name Input
                        html.Div([
                            html.Label("Feed Name:", style={'fontWeight': 'bold'}),
                            dcc.Input(id='feed_name', type='text', placeholder='Enter feed name', style={'marginLeft': '10px'})
                        ], style={'marginBottom': '10px'}),

                        # Feed Code Display
                        html.Div([
                            html.Label("Feed Code:", style={'fontWeight': 'bold'}),
                            html.Span(id='feed_code', style={'marginLeft': '10px'})
                        ], style={'marginBottom': '10px'}),

                        # Feed Analysis Report Heading
                        html.H2("Feed Analysis Report", style={'fontWeight': 'bold'}),

                        # Table for selected ingredients
                        dash_table.DataTable(
                            id='report_table',
                            columns=[{'name': col, 'id': col} for col in ['INGREDIENT', 'PRICE/KG', 'QUANTITY', 'AMOUNT']],
                            data=[],  # This will be filled dynamically
                            style_table={
                                'width': '100%',
                            },
                            style_cell={
                                'textAlign': 'left',
                                'padding': '5px'
                            },
                            style_header={
                                'backgroundColor': 'lightgrey',
                                'fontWeight': 'bold'
                            }
                        ),

                        # Table for nutrient composition
                        dash_table.DataTable(
                            id='nutrient_table',
                            columns=[{'name': 'Nutrient Composition', 'id': 'Nutrient'},
                                     {'name': 'Actual', 'id': 'Actual'}],
                            data=[],  # This will be filled dynamically
                            style_table={
                                'width': '100%',
                            },
                            style_cell={
                                'textAlign': 'left',
                                'padding': '5px'
                            },
                            style_header={
                                'backgroundColor': 'lightgrey',
                                'fontWeight': 'bold'
                            }
                        ),

                        # Print Button
                        html.Button("Print", id='print_button', n_clicks=0, style={'marginTop': '20px', 'fontWeight': 'bold'})
                    ]
                )
            ], className="rectangle")
        ], className="box_arrange")
    ], className="all_box")
], className="container")


@app.callback(
    Output('feed_code', 'children'),
    [Input('feed_name', 'value')]
)
def generate_feed_code(feed_name):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))


@app.callback(
    Output('print_button', 'style'),
    [Input('print_button', 'n_clicks')]
)
def hide_print_button(n_clicks):
    if n_clicks > 0:
        return {'display': 'none'}
    return {'display': 'block'}


@app.callback(
    Output('ingredient_table', 'data'),
    Input('ingredient_dd', 'value'),
    allow_duplicate=True
)
def update_table(selected_ingredients):
    if not selected_ingredients:
        return []
    selected_df = dfx[dfx['INGREDIENT'].isin(selected_ingredients)]
    selected_df['QUANTITY'] = 0
    selected_df['PRICE/KG'] = 0
    selected_df['QUANTITY PRICE'] = 0
    return selected_df.to_dict('records')


@app.callback(
    Output('minerals-vitamins-table', 'data'),
    Input('vit_dd', 'value'),
    allow_duplicate=True
)
def update_minerals_vitamins_table(selected_vitamins):
    if not selected_vitamins:
        return []
    selected_vitamins_df = df2[df2['vitamin/mineral'].isin(selected_vitamins)].copy()
    return selected_vitamins_df.to_dict('records')


@app.callback(
    Output('ingredient_table', 'data', allow_duplicate=True),
    [Input('ingredient_table', 'data_timestamp')],
    [State('ingredient_table', 'data')]
)
def calculate_quantity_price(_, rows):
    for row in rows:
        row['QUANTITY PRICE'] = row['QUANTITY'] * row['PRICE/KG']
    return rows


@app.callback(
    Output('minerals-vitamins-table', 'data', allow_duplicate=True),
    [Input('minerals-vitamins-table', 'data_timestamp')],
    [State('minerals-vitamins-table', 'data')]
)
def calculate_vitamin_amount(_, rows):
    for row in rows:
        row['AMOUNT'] = row['QUANTITY'] * row['PRICE/KG']
    return rows


if __name__ == '__main__':
    app.run_server(debug=True)

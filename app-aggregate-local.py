# Run this app with `python app-aggregate-local.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

import pandas as pd
from palmerpenguins import load_penguins

from helpers.aggregate import aggregate_df, agg_function_choices
from helpers.cols import cols_choice, cols_header

penguins = load_penguins()

app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# make `server` available to Heroku
server = app.server

app.layout = html.Div(
    className='container-fluid',
    children=[
        dcc.Store(id='inp', data=penguins.to_dict('records')),
        dcc.Store(id='agg', data=[]),
        html.H2('Aggregator'),
        html.Div(
            className='row',
            children =[
                html.Div(
                    className='col-sm-4',
                    children=[
                        dbc.Card([
                            dbc.CardHeader('Aggregation'),
                            dbc.CardBody([
                                dbc.Label('Grouping columns'),
                                dcc.Dropdown(id='cols-group', multi=True),
                                dbc.Label('Aggregation columns'),
                                dcc.Dropdown(id='cols-agg', multi=True),
                                dbc.Label('Aggregation function'),
                                dbc.Select(
                                    id='func-agg',
                                    options=[{'label': v, 'value': v} for v in agg_function_choices],
                                    value=agg_function_choices[0]
                                ),
                                html.Hr(),
                                dbc.Button(id='button-agg', children='Submit', class_name='btn btn-secondary')
                            ])
                        ])
                    ]
                ),
                html.Div(
                    className='col-sm-8',
                    children=[
                        html.H3('Input data'),
                        dash_table.DataTable(
                            id='table-inp',
                            page_size=10,
                            sort_action='native'
                        ),
                        html.Hr(),
                        html.H3('Aggregated data'),
                        dash_table.DataTable(
                            id='table-agg',
                            page_size=10,
                            sort_action='native'
                        )
                    ]
                )
            ]
        )
    ]
) 


# Inputs
@app.callback(Output('cols-group', 'options'),
              Input('inp', 'data'))
def update_cols_group(data_records):
    df = pd.DataFrame.from_dict(data_records)
    return cols_choice(df, 'object')

@app.callback(Output('cols-agg', 'options'),
              Input('inp', 'data'))
def update_cols_agg(data_records):
    df = pd.DataFrame.from_dict(data_records)
    return cols_choice(df, 'number')


# Calculations

@app.callback(Output('agg', 'data'),
              Input('button-agg', 'n_clicks'),
              State('inp', 'data'),
              State('cols-group', 'value'),
              State('cols-agg', 'value'),
              State('func-agg', 'value'),
              prevent_initial_call=True)
def aggregate(n_clicks, data_records, cols_group, cols_agg, func_agg):
    # create DataFrame
    df = pd.DataFrame.from_dict(data_records)

    # aggregate
    df_new = aggregate_df(df, cols_group, cols_agg, func_agg)

    # serialize DataFrame
    return df_new.to_dict('records')


# Outputs

@app.callback(Output('table-inp', 'columns'),
              Output('table-inp', 'data'),
              Input('inp', 'data'))
def update_table_inp(data_records):
     return cols_header(data_records), data_records   

@app.callback(Output('table-agg', 'columns'),
              Output('table-agg', 'data'),
              Input('agg', 'data'))
def update_table_agg(data_records):
    return cols_header(data_records), data_records


if __name__ == '__main__':
    app.run_server(debug=True)

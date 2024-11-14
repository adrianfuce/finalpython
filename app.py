import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import pathlib
import datetime


# Iniciar la app
app = dash.Dash(__name__)

server=app.server

app.layout = html.Div([
    html.H1("Dashboard Caso Final"),
    
    html.Label("Select Stock"),
    dcc.Dropdown(
        id='stock-dropdown', 
        options=[{'label': stock, 'value': stock} for stock in stocks], 
        value=stocks[0], 
        multi=True
    ),
    
    html.Label("Select Data Type"),
    dcc.Dropdown(
        id='data-type-dropdown', 
        options=[
            {'label': 'Price', 'value': 'price'},
            {'label': 'Return', 'value': 'return'}
        ], 
        value='price'
    ),
    
    # Slicer para el rango de fechas
    dcc.DatePickerRange(
        id='date-range',
        start_date=start_date,
        end_date=end_date,
        display_format='YYYY-MM-DD'
    ),
    
    # Gráfico
    dcc.Graph(id='stock-graph'),
    dcc.Graph(id='histogram1'),
    dcc.Graph(id='histogram2')
])

# Callback para actualizar los gráficos
@app.callback(
    [Output('stock-graph', 'figure'),
     Output('histogram1','figure'),
     Output('histogram2', 'figure')],
    [Input('stock-dropdown', 'value'),
     Input('data-type-dropdown', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_graph(selected_stocks, data_type, start_date, end_date):
    # Filtrar los datos por el rango de fechas
    if data_type == 'price':
        filtered_data = price_data.loc[start_date:end_date, selected_stocks]
    else:
        filtered_data = returns_data.loc[start_date:end_date, selected_stocks]
    
    # Si filtered_data es una Serie, convertirlo a DataFrame
    if isinstance(filtered_data, pd.Series):
        filtered_data = filtered_data.to_frame()

    # Crear el gráfico de líneas
    fig = px.line(filtered_data, x=filtered_data.index, y=filtered_data.columns)
    fig.update_layout(title="Precio y Retornos de la Acción", xaxis_title="Fecha", yaxis_title="Value")

    # Crear los histogramas
    fig2 = px.histogram(returns_data3, x="Portfolio")
    fig3 = px.histogram(returns_data4, x="Portfolio")
    
    return fig, fig2, fig3

#para GITHUB agregar el host y debug
if __name__=="__main__":
    app.run_server(debug=False, host="0.0.0.0",port=67000)

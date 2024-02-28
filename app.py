from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Charger les données depuis un fichier CSV
df = pd.read_csv('data/data1.csv', dtype={'Time': int})

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(df.Location.unique(), 'World', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.Location==value]
    return px.line(dff, x='Time', y='TPopulation1Jan')

if __name__ == '__main__':
    app.run(debug=True)



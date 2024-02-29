from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd

# Charger les données depuis un fichier CSV
df = pd.read_csv(
    "data/data1_with_iso.csv",
    dtype={
        "SortOrder": int,
        "LocID": int,
        "Notes": str,
        "ISO3_code": str,
        "ISO2_code": str,
        "SDMX_code": str,
        "LocTypeID": int,
        "LocTypeName": str,
        "ParentID": int,
        "Location": str,
        "VarID": int,
        "Variant": str,
        "Time": int,
        "TPopulation1Jan": float,
        "TPopulation1July": float,
        "TPopulationMale1July": float,
        "TPopulationFemale1July": float,
        "PopDensity": float,
        "PopSexRatio": float,
        "MedianAgePop": float,
        "NatChange": float,
        "NatChangeRT": float,
        "PopChange": float,
        "PopGrowthRate": float,
        "DoublingTime": float,
        "Births": float,
        "Births1519": float,
        "CBR": float,
        "TFR": float,
        "NRR": float,
        "MAC": float,
        "SRB": float,
        "Deaths": float,
        "DeathsMale": float,
        "DeathsFemale": float,
        "CDR": float,
        "LEx": float,
        "LExMale": float,
        "LExFemale": float,
        "LE15": float,
        "LE15Male": float,
        "LE15Female": float,
        "LE65": float,
        "LE65Male": float,
        "LE65Female": float,
        "LE80": float,
        "LE80Male": float,
        "LE80Female": float,
        "InfantDeaths": float,
        "IMR": float,
        "LBsurvivingAge1": float,
        "Under5Deaths": float,
        "Q5": float,
        "Q0040": float,
        "Q0040Male": float,
        "Q0040Female": float,
        "Q0060": float,
        "Q0060Male": float,
        "Q0060Female": float,
        "Q1550": float,
        "Q1550Male": float,
        "Q1550Female": float,
        "Q1560": float,
        "Q1560Male": float,
        "Q1560Female": float,
        "NetMigrations": float,
        "CNMR": float,
    },
)

# Liste des indicateurs pertinents pour les camemberts
relevant_columns = ["PopSexRatio", "PopDensity", "MedianAgePop"]

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(
            children="Dashboard sur l'évolution de la population mondiale",
            style={"textAlign": "center"},
        ),
        html.Div(
            [
                dcc.Dropdown(
                    options=[
                        {"label": loc, "value": loc}
                        for loc in df["Location"].unique()
                        if loc != "World"
                    ],
                    value=df["Location"].unique()[
                        0
                    ],  # Sélectionner le premier pays par défaut
                    id="dropdown-selection",
                ),
                html.Div(id="key-stats"),
            ]
        ),
        dcc.Graph(id="graph-content"),
        html.Div(id="pie-charts"),
        dcc.Graph(id="map-content"),
        dcc.Graph(id="bubble-chart"),
        dash_table.DataTable(data=df.to_dict("records"), page_size=10),
        dcc.Graph(
            figure=px.histogram(
                df,
                x="Location",
                y="MedianAgePop",
                histfunc="avg",
                title="Répartition de l'âge médian par pays",
                category_orders={
                    "Location": df.groupby("Location")["MedianAgePop"]
                    .mean()
                    .sort_values(ascending=False)
                    .index
                },
            )
        ),
    ]
)


@app.callback(
    Output("graph-content", "figure"),
    [Input("dropdown-selection", "value")],
)
def update_graph(selected_location):
    return px.line(
        df[df["Location"] == selected_location], x="Time", y="TPopulation1Jan"
    )


@app.callback(
    Output("pie-charts", "children"),
    [Input("dropdown-selection", "value")],
)
def update_pie_charts(selected_location):
    pie_charts_children = []
    if selected_location != "World":
        for col in relevant_columns:
            top_10_df = df[df["Location"] != "World"].nlargest(10, col)
            pie_fig = px.pie(
                top_10_df,
                names="Location",
                values=col,
                title=f"Top 10 des pays par {col}",
            )
            pie_charts_children.append(dcc.Graph(figure=pie_fig))
    else:
        for col in relevant_columns:
            top_10_df = df[df["Location"] != "World"].nlargest(10, col)
            pie_fig = px.pie(
                top_10_df,
                names="Location",
                values=col,
                title=f"Top 10 des pays par {col}",
            )
            pie_charts_children.append(dcc.Graph(figure=pie_fig))
    return pie_charts_children


@app.callback(
    Output("map-content", "figure"),
    [Input("dropdown-selection", "value")],
)
def update_map(selected_location):
    return px.choropleth(
        df,
        locations="ISO3_code",
        color="MedianAgePop",
        hover_name="Location",
        color_continuous_scale=px.colors.sequential.Plasma,
    )


@app.callback(
    Output("bubble-chart", "figure"),
    [Input("dropdown-selection", "value")],
)
def update_bubble_chart(selected_location):
    return px.scatter(
        df[df["Location"] == selected_location],
        x="Time",
        y="TPopulation1Jan",
        hover_data={"Time": "|"},
        title=f"Données pour TPopulation1Jan",
    )


@app.callback(
    Output("key-stats", "children"),
    [Input("dropdown-selection", "value")],
)
def update_key_stats(selected_location):
    dff = df[df["Location"] == selected_location]
    total_population = dff["TPopulation1Jan"].sum()
    total_births = dff["Births"].sum()
    total_deaths = dff["Deaths"].sum()
    migration_rate = dff["NetMigrations"].mean()

    return html.Div(
        [
            html.H2("Chiffres clés"),
            html.P(f"Nombre total d'habitants : {total_population}"),
            html.P(f"Nombre total de naissances : {total_births}"),
            html.P(f"Nombre total de décès : {total_deaths}"),
            html.P(f"Taux moyen de migration nette : {migration_rate}"),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)

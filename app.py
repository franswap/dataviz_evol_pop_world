from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_mantine_components as dmc
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

# Définir les styles pour le mode sombre
dark_mode_styles = {"backgroundColor": "#222", "color": "#fff"}

# Définir les styles pour le mode clair
light_mode_styles = {"backgroundColor": "#fff", "color": "#000"}

app.layout = html.Div(
    id="main-content",  # Ajouter un ID pour cibler cet élément dans le callback
    children=[
        html.H1(
            children="Dashboard sur l'évolution de la population mondiale",
            style={"textAlign": "center"},
        ),
        html.Button("Dark Mode", id="dark-mode-toggle", n_clicks=0),
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
        dcc.Graph(id="population-evolution"),
        dcc.Graph(id="death-birth-evolution"),
        dcc.Graph(
            id="histogram",
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
            ),
        ),
        html.Div(id="pie-charts"),
        dcc.Graph(id="map-content"),
        dash_table.DataTable(
            id="table",
            columns=[
                {"name": "Time", "id": "Time"},
                {"name": "TPopulation1Jan", "id": "TPopulation1Jan"},
                {"name": "PopDensity", "id": "PopDensity"},
                {"name": "PopSexRatio", "id": "PopSexRatio"},
                {"name": "MedianAgePop", "id": "MedianAgePop"},
                {"name": "NatChange", "id": "NatChange"},
                {"name": "NatChangeRT", "id": "NatChangeRT"},
                {"name": "PopChange", "id": "PopChange"},
                {"name": "PopGrowthRate", "id": "PopGrowthRate"},
                {"name": "DoublingTime", "id": "DoublingTime"},
                {"name": "Births", "id": "Births"},
                {"name": "Births1519", "id": "Births1519"},
                {"name": "CBR", "id": "CBR"},
                {"name": "TFR", "id": "TFR"},
                {"name": "NRR", "id": "NRR"},
                {"name": "MAC", "id": "MAC"},
                {"name": "SRB", "id": "SRB"},
                {"name": "Deaths", "id": "Deaths"},
                {"name": "DeathsMale", "id": "DeathsMale"},
                {"name": "DeathsFemale", "id": "DeathsFemale"},
                {"name": "CDR", "id": "CDR"},
                {"name": "InfantDeaths", "id": "InfantDeaths"},
                {"name": "LBsurvivingAge1", "id": "LBsurvivingAge1"},
                {"name": "NetMigrations", "id": "NetMigrations"},
            ],
            page_size=15,
        ),
    ],
)


# Callback pour changer le mode
@app.callback(Output("main-content", "style"), [Input("dark-mode-toggle", "n_clicks")])
def update_style(n_clicks):
    if n_clicks % 2 == 0:
        return light_mode_styles
    else:
        return dark_mode_styles


@app.callback(
    Output("population-evolution", "figure"),
    [Input("dropdown-selection", "value")],
)
def update_bubble_chart(selected_location):
    return px.line(
        df[df["Location"] == selected_location],
        x="Time",
        y="TPopulation1Jan",
        hover_data={"Time": "|"},
        title=f"Evolution de la population de 1950 à 2100 (projection)",
    )


@app.callback(
    Output("death-birth-evolution", "figure"),
    [Input("dropdown-selection", "value")],
)
def update_population_evolution(selected_location):
    dff = df[df["Location"] == selected_location]
    fig = px.line(
        dff,
        x="Time",
        y=["Deaths", "Births"],
        title="Evolution du rapport entre les naissances et les décès",
    )
    return fig


@app.callback(
    Output("pie-charts", "children"),
    [Input("dropdown-selection", "value")],
)
def update_pie_charts(selected_location):
    pie_charts_children = []
    if selected_location == "World":
        for col in relevant_columns:
            # Sélectionner les valeurs pour l'année 2022
            df_2022 = df[df["Time"] == 2022]
            # Sélectionner les 10 premières lignes pour chaque colonne
            sorted_values = df_2022.sort_values(by=col, ascending=False).head(10)
            pie_fig = px.pie(
                sorted_values,
                names="Location",
                values=col,
                title=f"Top 10 des pays par {col} en 2022",
                labels={"Location": "Pays", col: "Valeur"},  # Définir les étiquettes
            )
            pie_fig.update_traces(textinfo="value")  # Afficher les valeurs brutes
            pie_charts_children.append(dcc.Graph(figure=pie_fig))
    return (
        pie_charts_children if selected_location == "World" else []
    )  # Retourne une liste vide si un pays est sélectionné


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
            html.H2("Chiffres clés", style={"text-align": "center"}),
            dmc.SimpleGrid(
                cols=4,
                children=[
                    html.Div(
                        [
                            html.P(
                                "Nombre total d'habitants : ",
                                style={"font-size": "1.2em"},
                            ),
                            html.P(
                                round(total_population),
                                style={"font-weight": "bold", "font-size": "1.2em"},
                            ),
                        ],
                        style={"text-align": "center"},
                    ),
                    html.Div(
                        [
                            html.P(
                                "Nombre total de naissances : ",
                                style={"font-size": "1.2em"},
                            ),
                            html.P(
                                round(total_births),
                                style={"font-weight": "bold", "font-size": "1.2em"},
                            ),
                        ],
                        style={"text-align": "center"},
                    ),
                    html.Div(
                        [
                            html.P(
                                "Nombre total de décès : ", style={"font-size": "1.2em"}
                            ),
                            html.P(
                                round(total_deaths),
                                style={"font-weight": "bold", "font-size": "1.2em"},
                            ),
                        ],
                        style={"text-align": "center"},
                    ),
                    html.Div(
                        [
                            html.P(
                                "Taux de migration : ", style={"font-size": "1.2em"}
                            ),
                            html.P(
                                round(migration_rate),
                                style={"font-weight": "bold", "font-size": "1.2em"},
                            ),
                        ],
                        style={"text-align": "center"},
                    ),
                ],
                style={"justify-content": "center"},
            ),
        ]
    )


@app.callback(
    Output("table", "data"),
    [Input("dropdown-selection", "value")],
)
def update_table(selected_location):
    if selected_location != "World":
        return df[df["Location"] == selected_location].to_dict("records")
    else:
        return df[df["Location"] == "World"].iloc[::5].to_dict("records")


# Ajout de l'histogramme à la fin de la mise en page
@app.callback(
    Output("histogram", "figure"),
    [Input("dropdown-selection", "value")],
)
def update_histogram(selected_location):
    if selected_location != "World":
        dff = df[df["Location"] == selected_location]
        fig = px.histogram(
            dff, x="MedianAgePop", title="Distribution de l'âge médian de la population"
        )
        return fig
    else:
        return {}


if __name__ == "__main__":
    app.run_server(debug=True)

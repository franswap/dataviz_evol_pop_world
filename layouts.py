from dash import html, dcc, dash_table
import dash_mantine_components as dmc
import plotly.express as px


# Définir la mise en page de l'application
def home_page(df, df_notes):
    layout = html.Div(
        id="main-content",  # Ajouter un ID pour cibler cet élément dans le callback
        children=[
            html.H1(
                children="Dashboard sur l'évolution de la population mondiale",
                style={"textAlign": "center"},
            ),
            html.Div(
                [
                    dcc.Dropdown(
                        placeholder="Sélectionner une localisation",
                        options=[{"label": "Monde", "value": "World"}]
                        + [
                            {"label": location, "value": location}
                            for location in df["Location"].unique()
                            if location != "World"
                        ],
                        # Sélectionner le premier pays par défaut
                        value=df["Location"].unique()[0],
                        id="dropdown-selection",
                    ),
                    html.Div(id="key-stats"),
                ]
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id="population-evolution",
                        style={"display": "inline-block", "width": "50%"},
                    ),
                    dcc.Graph(
                        id="death-birth-evolution",
                        style={"display": "inline-block", "width": "50%"},
                    ),
                ]
            ),
            dcc.Graph(id="histogram"),
            dmc.SimpleGrid(cols=3, id="pie-charts"),
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
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Dropdown(
                                options=[
                                    {"label": i, "value": i}
                                    for i in df_notes["Indicator"].unique()
                                ],
                                value="InfantDeaths",
                                id="crossfilter-xaxis-column",
                            ),
                            dcc.RadioItems(
                                options=[
                                    {"label": i, "value": i} for i in ["Linear", "Log"]
                                ],
                                value="Linear",
                                id="crossfilter-xaxis-type",
                                labelStyle={
                                    "display": "inline-block",
                                    "marginTop": "5px",
                                },
                            ),
                        ],
                        style={"width": "49%", "display": "inline-block"},
                    ),
                    html.Div(
                        [
                            dcc.Dropdown(
                                options=[
                                    {"label": i, "value": i}
                                    for i in df_notes["Indicator"].unique()
                                ],
                                value="PopDensity",
                                id="crossfilter-yaxis-column",
                            ),
                            dcc.RadioItems(
                                options=[
                                    {"label": i, "value": i} for i in ["Linear", "Log"]
                                ],
                                value="Linear",
                                id="crossfilter-yaxis-type",
                                labelStyle={
                                    "display": "inline-block",
                                    "marginTop": "5px",
                                },
                            ),
                        ],
                        style={
                            "width": "49%",
                            "float": "right",
                            "display": "inline-block",
                        },
                    ),
                ],
                style={"padding": "10px 5px"},
            ),
            html.Div(
                [
                    dcc.Graph(
                        id="crossfilter-indicator-scatter",
                        hoverData={"points": "World"},
                    )
                ],
                style={
                    "width": "49%",
                    "display": "inline-block",
                    "padding": "0 20",
                },
            ),
            html.Div(
                [
                    dcc.Graph(id="x-time-series"),
                    dcc.Graph(id="y-time-series"),
                ],
                style={"display": "inline-block", "width": "49%"},
            ),
            html.Div(
                dcc.Slider(
                    min=df["Time"].min(),
                    max=df["Time"].max(),
                    step=None,
                    id="crossfilter-year--slider",
                    value=2024,
                    marks={
                        str(year): str(year)
                        for year in range(df["Time"].min(), df["Time"].max(), 10)
                    },
                ),
                style={"width": "49%", "padding": "0px 20px 20px 20px"},
            ),
        ],
    )
    return layout

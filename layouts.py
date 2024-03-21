from dash import html, dcc, dash_table
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.express as px

image_path = 'assets/introduction.jpg'

# Définir la mise en page de l'application
def home_page(df, df_notes):
    layout = html.Div(
        id="main-content",  # Ajouter un ID pour cibler cet élément dans le callback
        children=[
            html.Div(
                style={
                    "display": "flex",
                    "align-items": "center",
                    "justify-content": "center",
                    "margin": 25,
                    "padding": 20,
                },
                children=[
                    html.H1(
                        children="Dashboard sur l'évolution de la population mondiale",
                        style={"textAlign": "center", "margin-right": 20},
                    ),
                    dmc.Group(
                        [
                            DashIconify(
                                icon="line-md:document-report-twotone",
                                width=70,
                            ),
                        ]
                    ),
                ],
            ),
dmc.Card(
    children=[
        dmc.CardSection(
            dmc.Image(
                src=image_path,
                height=400,
                width=1000,
            )
        ),
        dmc.Space(h=20),
        dmc.Text(
            "Découvrez les données les plus récentes et pertinentes des Nations Unies à travers notre projet de datavisualisation. Explorez une multitude d'indicateurs démographiques, économiques et environnementaux qui offrent un aperçu approfondi de notre monde en constante évolution. Du taux de natalité à l'espérance de vie, en passant par les migrations, plongez dans les statistiques clés qui façonnent notre compréhension de la société mondiale actuelle.",
            size="md",
            color="dimmed",
            align="center"
        ),
        dmc.Space(h=20),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"width": 1000, "margin": "auto"},  # Ajout de la propriété "margin: auto"
),

            html.Div(
                [
                    html.Div(
                        [
                            html.P(
                                "Sélectionnez un emplacement pour afficher les statistiques démographiques, économiques et environnementales correspondantes. Notre projet de datavisualisation vous permet d'explorer une variété d'indicateurs clés des Nations Unies, offrant un aperçu approfondi de notre monde en constante évolution.",
                                style={"text-align": "center", "padding": 35, "font-size": 20},
                            ),
                            html.Div(
                                [
                                    html.H3(
                                        id="selected-time-heading",
                                        style={"text-align": "center", "padding": 15},
                                    ),
                                    dcc.Dropdown(
                                        placeholder="Sélectionner une date",
                                        clearable=False,
                                        options=[{"label": "Date", "value": "2024"}]
                                        + [
                                            {"label": time, "value": time}
                                            for time in df["Time"].unique()
                                            if time != "2024"
                                        ],
                                        # Définir "2024" comme valeur par défaut
                                        value=2024,
                                        id="dropdown-time-selection",
                                        style={
                                            "width": "300px",
                                            "font-size": "16px",
                                            "font-family": "Arial, sans-serif",
                                            "color": "#333",  # Couleur du texte
                                            "background-color": "#f7f7f7",  # Couleur de fond
                                            "border-radius": "8px",  # Coins arrondis
                                            "border": "1px solid #ccc",  # Bordure
                                            "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",  # Ombre
                                            "margin": "0 auto",  # Centrer le dropdown horizontalement
                                        },
                                    ),
                                ],
                                style={
                                    "display": "inline-block",
                                    "width": "50%",
                                },  # Diviser en deux colonnes
                            ),
                            html.Div(
                                [
                                    html.H3(
                                        id="selected-country-heading",
                                        style={"text-align": "center", "padding": 15},
                                    ),
                                    dcc.Dropdown(
                                        placeholder="Sélectionner une localisation",
                                        clearable=False,
                                        options=[{"label": "Monde", "value": "World"}]
                                        + [
                                            {"label": location, "value": location}
                                            for location in df["Location"].unique()
                                            if location != "World"
                                        ],
                                        # Sélectionner le premier pays par défaut
                                        value=df["Location"].unique()[0],
                                        id="dropdown-selection",
                                        style={
                                            "width": "300px",
                                            "font-size": "16px",
                                            "font-family": "Arial, sans-serif",
                                            "color": "#333",  # Couleur du texte
                                            "background-color": "#f7f7f7",  # Couleur de fond
                                            "border-radius": "8px",  # Coins arrondis
                                            "border": "1px solid #ccc",  # Bordure
                                            "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",  # Ombre
                                            "margin": "0 auto",  # Centrer le dropdown horizontalement
                                        },
                                    ),
                                ],
                                style={
                                    "display": "inline-block",
                                    "width": "50%",
                                },  # Diviser en deux colonnes
                            ),
                        ],
                        style={
                            "text-align": "center"
                        },  # Centrer le contenu horizontalement
                    ),
                    html.Div(id="key-stats"),
                ]
            ),
            html.Div(
                children=[
                    html.H2(
                        children="Tendance sur lévolution des populations",
                        style={"textAlign": "center", "margin-right": 20},
                    ),
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
            # dcc.Graph(id="graphEvol"),
            dcc.Graph(id="histogram"),
            html.Div(
                [
                    html.H2(
                        "Représentation du top pays des principaux indicateurs",
                        style={"text-align": "center"},
                    ),
                    html.Div(
                        [
                            dcc.Slider(
                                id="pie-year-slider",
                                min=df["Time"].min(),
                                max=df["Time"].max(),
                                step=10,
                                value=2024,
                                marks={
                                    str(year): str(year)
                                    for year in range(
                                        df["Time"].min(), df["Time"].max() + 1, 10
                                    )
                                },
                            ),
                            dmc.SimpleGrid(cols=3, id="pie-charts-container"),
                        ],
                        style={"width": "100%", "margin": "0 auto"},
                    ),
                ]
            ),
            html.H2(
                "Ventilation spatiale de l'age médian dans le monde en ",
                id="map-year-title",
                style={"text-align": "center", "padding": 15},
            ),
            # Sélection de l'année pour la carte mondiale
            html.Div(
                [
                    dcc.Slider(
                        id="map-year-slider",
                        min=df["Time"].min(),
                        max=df["Time"].max(),
                        step=10,  # Afficher tous les 10 ans d'intervalle
                        value=2024,  # Année par défaut
                        marks={
                            str(year): str(year)
                            for year in range(
                                df["Time"].min(), df["Time"].max() + 1, 10
                            )
                        },
                    ),
                ],
                style={"width": "90%", "margin": "0 auto", "margin-bottom": "20px"},
            ),
            dcc.Graph(id="map-content"),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Dropdown(
                                options=[
                                    {"label": label, "value": value}
                                    for value, label in zip(
                                        df_notes["Indicator"], df_notes["IndicatorName"]
                                    )
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
                                    {"label": label, "value": value}
                                    for value, label in zip(
                                        df_notes["Indicator"], df_notes["IndicatorName"]
                                    )
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
                        hoverData={"points": [{"hovertext": "World"}]},
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

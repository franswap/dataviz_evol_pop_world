from dash import html, dcc, dash_table
import dash_mantine_components as dmc
import plotly.express as px


# Définir la mise en page de l'application
def home_page(df):
    layout = html.Div(
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
    return layout

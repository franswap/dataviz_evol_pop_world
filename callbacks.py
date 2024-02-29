from dash import html, dcc, callback, Output, Input
import dash_mantine_components as dmc
import plotly.express as px

# Définir les styles pour le mode sombre
dark_mode_styles = {"backgroundColor": "#222", "color": "#fff"}

# Définir les styles pour le mode clair
light_mode_styles = {"backgroundColor": "#fff", "color": "#000"}

# Liste des indicateurs pertinents pour les camemberts
relevant_columns = ["PopSexRatio", "PopDensity", "MedianAgePop"]


def register_callbacks(df):
    # Callback pour changer le mode
    @callback(Output("main-content", "style"), Input("dark-mode-toggle", "n_clicks"))
    def update_style(n_clicks):
        if n_clicks % 2 == 0:
            return light_mode_styles
        else:
            return dark_mode_styles

    @callback(
        Output("population-evolution", "figure"),
        Input("dropdown-selection", "value"),
    )
    def update_bubble_chart(selected_location):
        return px.line(
            df[df["Location"] == selected_location],
            x="Time",
            y="TPopulation1Jan",
            hover_data={"Time": "|"},
            title=f"Evolution de la population de 1950 à 2100 (projection)",
        )

    @callback(
        Output("death-birth-evolution", "figure"),
        Input("dropdown-selection", "value"),
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

    @callback(
        Output("pie-charts", "children"),
        Input("dropdown-selection", "value"),
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
                    labels={
                        "Location": "Pays",
                        col: "Valeur",
                    },  # Définir les étiquettes
                )
                pie_fig.update_traces(textinfo="value")  # Afficher les valeurs brutes
                pie_charts_children.append(dcc.Graph(figure=pie_fig))
        return (
            pie_charts_children if selected_location == "World" else []
        )  # Retourne une liste vide si un pays est sélectionné

    @callback(
        Output("map-content", "figure"),
        Input("dropdown-selection", "value"),
    )
    def update_map(selected_location):
        return px.choropleth(
            df,
            locations="ISO3_code",
            color="MedianAgePop",
            hover_name="Location",
            color_continuous_scale=px.colors.sequential.Plasma,
        )

    @callback(
        Output("key-stats", "children"),
        Input("dropdown-selection", "value"),
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
                                    "Nombre total de décès : ",
                                    style={"font-size": "1.2em"},
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

    @callback(
        Output("table", "data"),
        Input("dropdown-selection", "value"),
    )
    def update_table(selected_location):
        if selected_location != "World":
            return df[df["Location"] == selected_location].to_dict("records")
        else:
            return df[df["Location"] == "World"].iloc[::5].to_dict("records")

    # Ajout de l'histogramme à la fin de la mise en page
    @callback(
        Output("histogram", "figure"),
        [Input("dropdown-selection", "value")],
    )
    def update_histogram(selected_location):
        if selected_location != "World":
            dff = df[df["Location"] == selected_location]
            fig = px.histogram(
                dff,
                x="MedianAgePop",
                title="Distribution de l'âge médian de la population",
            )
            return fig
        else:
            return {}

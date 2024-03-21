from dash import html, dcc, callback, Output, Input
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.express as px

# Liste des indicateurs pertinents pour les camemberts
relevant_columns = ["PopSexRatio", "PopDensity", "MedianAgePop"]


def register_callbacks(df, df_notes):
    # Mise à jour du graphique de l'évolution de la population en fonction de la localisation
    @callback(
        Output("population-evolution", "figure"),
        Input("dropdown-selection", "value"),
    )
    def update_bubble_chart(selected_location):
        return px.line(
            df[df["Location"] == selected_location],
            x="Time",
            y="TPopulation1Jan",
            hover_data={"Time"},
            title=f"Evolution de la population de 1950 à 2100 (projection)",
        )

    @callback(
        Output("selected-country-heading", "children"),
        [Input("dropdown-selection", "value")],
    )
    def update_selected_country_heading(selected_country):
        return f"Pays sélectionné : {selected_country}"

    @callback(
        Output("selected-time-heading", "children"),
        [Input("dropdown-time-selection", "value")],
    )
    def update_selected_time_heading(selected_date):
        return f"Date sélectionnée : {selected_date}"

    # Mise à jour du graphique de l'évolution des naissances et des décès en fonction de la localisation
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

    # Mise à jour des camemberts en fonction de la localisation
    @callback(
        Output("pie-charts-container", "children"),
        [Input("dropdown-selection", "value"), Input("pie-year-slider", "value")],
    )
    def update_pie_charts(selected_location, selected_year):
        pie_charts_children = []

        if selected_location == "World" or selected_location is None:
            for col in relevant_columns:
                # Sélectionner les valeurs pour l'année sélectionnée
                df_year = df[df["Time"] == selected_year]
                # Sélectionner les 5 premières lignes pour chaque colonne
                sorted_values = df_year.sort_values(by=col, ascending=False).head(5)
                pie_fig = px.pie(
                    sorted_values,
                    names="Location",
                    values=col,
                    title=f"Top 5 des pays par {col} en {selected_year}",
                    labels={
                        "Location": "Pays",
                        col: "Valeur",
                    },  # Définir les étiquettes
                )
                pie_fig.update_traces(textinfo="value")  # Afficher les valeurs brutes
                pie_charts_children.append(dcc.Graph(figure=pie_fig))

        # Retourne une liste vide si un pays est sélectionné
        return pie_charts_children

    # Mise à jour du titre de la ventilation spatiale en fonction de l'année sélectionnée dans le slider
    @callback(
        Output("map-year-title", "children"),
        Input("map-year-slider", "value"),
    )
    def update_map_year_title(selected_year):
        return f"Ventilation spatiale de l'age médian dans le monde en {selected_year}"

    # Mise à jour de la carte en fonction de la localisation
    @callback(
        Output("map-content", "figure"),
        [Input("dropdown-selection", "value"), Input("map-year-slider", "value")],
    )
    def update_map(selected_location, selected_year):
        if selected_year is not None:
            df_year = df[df["Time"] == selected_year]
            fig = px.choropleth(
                df_year,
                locations="ISO3_code",
                color="MedianAgePop",
                hover_name="Location",
                color_continuous_scale=px.colors.sequential.Plasma,
            )
            return fig
        else:
            # Si aucune année n'est sélectionnée, afficher la carte avec les données de l'année actuelle par défaut
            fig = px.choropleth(
                df,
                locations="ISO3_code",
                color="MedianAgePop",
                hover_name="Location",
                color_continuous_scale=px.colors.sequential.Plasma,
            )
        return fig

    # Mise à jour des chiffres clés en fonction de la localisation et de la date
    @callback(
        Output("key-stats", "children"),
        [Input("dropdown-selection", "value"), Input("dropdown-time-selection", "value")],
    )
    def update_key_stats(selected_location, selected_date):
        if selected_location is None:
            return html.Div(
                [
                    html.H2("Chiffres clés"),
                    html.P(
                        "Sélectionnez une localisation pour afficher les chiffres clés",
                        style={"font-size": "1.2em"},
                    ),
                ],
                style={"text-align": "center"},
            )

        dff = df[(df["Location"] == selected_location) & (df["Time"] == selected_date)]
        total_population = dff["TPopulation1Jan"].sum()
        total_births = dff["Births"].sum()
        total_deaths = dff["Deaths"].sum()
        migration_rate = dff["NetMigrations"].mean()
        LExMale = dff["LExMale"].mean()
        LExFemale = dff["LExFemale"].mean()

        return html.Div(
            [
                html.H2(
                    "Chiffres clés",
                    style={"text-align": "center"},
                ),
                dmc.SimpleGrid(
                    cols=3,
                    children=[
                        html.Div(
                            [
                                DashIconify(
                                    icon="raphael:people",
                                    width=50,
                                    style={"margin-right": "10px"},
                                ),
                                html.Div(
                                    [
                                        html.H3(
                                            "Nombre total d'habitants",
                                            style={
                                                "margin-bottom": "5px",
                                                "text-align": "center",
                                                "font-size": "1.2em",
                                            },
                                        ),
                                        html.P(
                                            round(total_population),
                                            style={
                                                "font-weight": "bold",
                                                "font-size": "1.1em",
                                                "text-align": "center",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "flex-direction": "column",
                                    },
                                ),
                            ],
                            style={"display": "flex", "align-items": "center"},
                        ),
                        html.Div(
                            [
                                DashIconify(
                                    icon="noto-v1:baby-bottle",
                                    width=50,
                                    style={"margin-right": "10px"},
                                ),
                                html.Div(
                                    [
                                        html.H3(
                                            "Nombre total de naissances",
                                            style={
                                                "margin-bottom": "5px",
                                                "text-align": "center",
                                                "font-size": "1.2em",
                                            },
                                        ),
                                        html.P(
                                            round(total_births),
                                            style={
                                                "font-weight": "bold",
                                                "font-size": "1.1em",
                                                "text-align": "center",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "flex-direction": "column",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "align-items": "center",
                            },
                        ),
                        html.Div(
                            [
                                DashIconify(
                                    icon="healthicons:death-alt2-outline",
                                    width=50,
                                    style={"margin-right": "10px"},
                                ),
                                html.Div(
                                    [
                                        html.H3(
                                            "Nombre total de décès",
                                            style={
                                                "margin-bottom": "5px",
                                                "text-align": "center",
                                                "font-size": "1.2em",
                                            },
                                        ),
                                        html.P(
                                            round(total_deaths),
                                            style={
                                                "font-weight": "bold",
                                                "font-size": "1.1em",
                                                "text-align": "center",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "flex-direction": "column",
                                    },
                                ),
                            ],
                            style={"display": "flex", "align-items": "center"},
                        ),
                                                html.Div(
                            [
                                DashIconify(
                                    icon="fluent-emoji:male-sign",
                                    width=50,
                                    style={"margin-right": "10px"},
                                ),
                                html.Div(
                                    [
                                        html.H3(
                                            "Espérance de vie moyenne des homme",
                                            style={
                                                "margin-bottom": "5px",
                                                "text-align": "center",
                                                "font-size": "1.2em",
                                            },
                                        ),
                                        html.P(
                                            round(LExMale),
                                            style={
                                                "font-weight": "bold",
                                                "font-size": "1.1em",
                                                "text-align": "center",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "flex-direction": "column",
                                    },
                                ),
                            ],
                            style={"display": "flex", "align-items": "center"},
                        ),
                                                html.Div(
                            [
                                DashIconify(
                                    icon="fluent-emoji:female-sign",
                                    width=50,
                                    style={"margin-right": "10px"},
                                ),
                                html.Div(
                                    [
                                        html.H3(
                                            "Espérance de vie moyenne des femmes",
                                            style={
                                                "margin-bottom": "5px",
                                                "text-align": "center",
                                                "font-size": "1.2em",
                                            },
                                        ),
                                        html.P(
                                            round(LExFemale),
                                            style={
                                                "font-weight": "bold",
                                                "font-size": "1.1em",
                                                "text-align": "center",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "flex-direction": "column",
                                    },
                                ),
                            ],
                            style={"display": "flex", "align-items": "center"},
                        ),
                        html.Div(
                            [
                                DashIconify(
                                    icon="gis:earth-euro-africa-o",
                                    width=50,
                                    style={"margin-right": "10px"},
                                ),
                                html.Div(
                                    [
                                        html.H3(
                                            "Taux de migration",
                                            style={
                                                "margin-bottom": "5px",
                                                "text-align": "center",
                                                "font-size": "1.2em",
                                            },
                                        ),
                                        html.P(
                                            round(migration_rate),
                                            style={
                                                "font-weight": "bold",
                                                "font-size": "1.1em",
                                                "text-align": "center",
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "flex-direction": "column",
                                    },
                                ),
                            ],
                            style={ "display": "flex", "align-items": "center", "justify-content": "center"},
                        ),
                    ],
                ),
            ],
            style={"padding": "20px"},
        )

    @callback(
        Output("crossfilter-indicator-scatter", "figure"),
        Input("crossfilter-xaxis-column", "value"),
        Input("crossfilter-yaxis-column", "value"),
        Input("crossfilter-xaxis-type", "value"),
        Input("crossfilter-yaxis-type", "value"),
        Input("crossfilter-year--slider", "value"),
    )
    def update_graph(
        xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type, year_value
    ):
        dff = df[df["Time"] == year_value]

        # Agréger les données par année et par lieu
        dff_aggregated = (
            dff.groupby("Location")
            .agg({xaxis_column_name: "first", yaxis_column_name: "first"})
            .reset_index()
        )

        fig = px.scatter(
            dff_aggregated,
            x=xaxis_column_name,
            y=yaxis_column_name,
            hover_name="Location",
        )

        fig.update_xaxes(
            title=xaxis_column_name, type="linear" if xaxis_type == "Linear" else "log"
        )

        fig.update_yaxes(
            title=yaxis_column_name, type="linear" if yaxis_type == "Linear" else "log"
        )

        fig.update_layout(
            margin={"l": 40, "b": 40, "t": 10, "r": 0}, hovermode="closest"
        )

        return fig

    @callback(
        Output("x-time-series", "figure"),
        Input("crossfilter-indicator-scatter", "hoverData"),
        Input("crossfilter-xaxis-column", "value"),
        Input("crossfilter-xaxis-type", "value"),
    )
    def update_x_timeseries(hoverData, xaxis_column_name, axis_type):
        return create_time_series(hoverData, xaxis_column_name, axis_type)

    @callback(
        Output("y-time-series", "figure"),
        Input("crossfilter-indicator-scatter", "hoverData"),
        Input("crossfilter-yaxis-column", "value"),
        Input("crossfilter-yaxis-type", "value"),
    )
    def update_y_timeseries(hoverData, yaxis_column_name, axis_type):
        return create_time_series(hoverData, yaxis_column_name, axis_type)

    def create_time_series(hoverData, column_name, axis_type):
        country_name = hoverData["points"][0]["hovertext"]
        dff = df[df["Location"] == country_name]
        label = df_notes.loc[
            df_notes["Indicator"] == column_name, "IndicatorName"
        ].values[0]
        title = "<b>{}</b><br>{}".format(country_name, label)

        fig = px.scatter(dff, x="Time", y=column_name)
        fig.update_traces(mode="lines+markers")
        fig.update_xaxes(showgrid=False, title="Temps")
        fig.update_yaxes(title=label, type="linear" if axis_type == "Linear" else "log")
        fig.add_annotation(
            x=0,
            y=0.85,
            xanchor="left",
            yanchor="bottom",
            xref="paper",
            yref="paper",
            showarrow=False,
            align="left",
            text=title,
        )
        return fig

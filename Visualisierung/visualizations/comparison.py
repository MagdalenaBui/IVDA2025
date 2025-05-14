from typing import Sequence, Union
from dash import Dash
from dash.dcc import Graph
from dash.dependencies import Output
from dash.development.base_component import Component
from dash.html import H3
from pandas import DataFrame
from plotly.express import scatter
from filter import and_, number_range, multi_eq
from id import generate_id
from input import build_dropdown, build_radio_items, build_rangeslider
from visualizations.visualization import Visualization

class Comparison(Visualization):
    # Initialisierung des Vergleichs von Age mit Overall oder Wage(in Euro), auswählbar durch eine Radio-Item Komponente, mit Filterung durch Dropdown und Rangelsider Komponenten
    def __init__(self, app: Dash, dataframe: DataFrame, column:str):
        self.title = H3(f"Gegenüberstellung von Overall bzw. Wage (in Euro) mit Age")

        GRAPH_ID = generate_id(f"graph-comparison")
        self.graph = Graph(id=GRAPH_ID)
        self.scatter_y = column

        self.filter_elements = [
            build_radio_items("Attribut an der Y-Achse", [("Overall", "Overall"), ("Wage(in Euro)", "Wage(in Euro)")],
                              "Wage(in Euro)"),
            build_dropdown("nach Club filtern", dataframe["Club Name"].unique().tolist(), multi=True),
            build_dropdown("nach Nationality filtern", dataframe["Nationality"].unique().tolist(),multi=True),
            build_rangeslider("nach Age filtern", int(dataframe["Age"].min()), int(dataframe["Age"].max())),
            build_rangeslider("nach Wage (in Euro) filtern", int(dataframe["Wage(in Euro)"].min()), int(dataframe["Wage(in Euro)"].max())),
            build_rangeslider("nach Overall filtern", int(dataframe["Overall"].min()), int(dataframe["Overall"].max()))

        ]


        @app.callback(
        Output(GRAPH_ID, "figure"),
        # Input des Callbacks ist ein Tupel aus den Werte der Filter-Komponenten
        inputs=[
            tuple(filter_element["input"] for filter_element in self.filter_elements)
            ]
        )
        def update(
            filters: tuple[str, Union[list[str], str], Union[list[str],str], list[int], list[int], list[int]]

        ):
            scatter_y, club, nationality, age_range, wage_range, overall_range = filters
            # Festlegung des Graphs als Scatter-Plot
            scatter_data = and_(
                dataframe, [
                    multi_eq("Club Name", club),
                    multi_eq("Nationality", nationality),
                    number_range("Age", age_range[0], age_range[1]),
                    number_range("Wage(in Euro)", wage_range[0], wage_range[1]),
                    number_range("Overall", overall_range[0], overall_range[1])
                ]
            ).reset_index()

            return scatter(
                scatter_data, x="Age", y=scatter_y, opacity=0.4, hover_data=["Full Name", "index"]
            )

    # Comparison erbt von Visualization und definiert die Struktur des User Interfaces
    def html(self) -> Sequence[Component]:
        return [self.title, self.graph] + [
            input_element["element"] for input_element in self.filter_elements
    ]
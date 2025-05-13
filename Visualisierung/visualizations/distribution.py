from enum import Enum
from typing import Sequence, Union
from dash import Dash
from dash.dcc import Graph
from dash.dependencies import Output
from dash.development.base_component import Component
from dash.html import H3
from pandas import DataFrame
from plotly.express import histogram, scatter
from filter import and_, eq, number_range, multi_eq
from id import generate_id
from input import build_dropdown, build_radio_items, build_rangeslider
from visualizations.visualization import Visualization

class Distribution(Visualization):

	def __init__(self, app: Dash, dataframe: DataFrame, allowed_attributes: list[str], show_boxplot: bool = True):
		self.title = H3("Verteilung der Items")

		GRAPH_ID = generate_id("graph-distribution")
		SCATTER_ID = generate_id("graph-scatter") # Neue ID für Scatterplot

		self.graph = Graph(GRAPH_ID)
		self.scatter_graph = Graph(SCATTER_ID) # Neuer Graph für Scatterplot
		self.show_boxplot = show_boxplot

		self.filter_elements =  [
			build_dropdown("Attribut auswählen", allowed_attributes, allowed_attributes[0], multi=False),
			build_dropdown("nach Club filtern", dataframe["Club Name"].unique().tolist(), multi=True),
			build_dropdown("nach Nationality filtern", dataframe["Nationality"].unique().tolist(),multi=True),
			build_rangeslider("nach Age filtern", int(dataframe["Age"].min()), int(dataframe["Age"].max())),
			build_rangeslider("nach Wage (in Euro) filtern", int(dataframe["Wage(in Euro)"].min()), int(dataframe["Wage(in Euro)"].max())),
			build_rangeslider("nach Overall filtern", int(dataframe["Overall"].min()), int(dataframe["Overall"].max()))
			build_radio_items("Scatter Y-Achse", ["Wage (in Euro)", "Overall"], "Wage (in Euro)")
		]


		@app.callback(
			Output(GRAPH_ID, "figure"),
			inputs=[
				tuple(filter_element["input"] for filter_element in self.filter_elements),
			]
		)

		def update(
			filters: tuple[str, Union[list[str], str], Union[list[str],str], list[int], list[int], list[int]]
		):
			column, club, nationality, age_range, wage_range, overall_range = filters

			chart = histogram(
				and_(dataframe, [
					multi_eq("Club Name", club),
					multi_eq("Nationality", nationality),
					number_range("Age", age_range[0], age_range[1]),
					number_range("Wage(in Euro)",wage_range[0], wage_range[1]),
					number_range("Overall", overall_range[0], overall_range[1])
				]).reset_index(), #was macht das?
				x=column,
				marginal="box" if self.show_boxplot else None,
				hover_data=["Full Name", "index"]
			)
								
			return chart
		

		@app.callback(
            Output(SCATTER_ID, "figure"),
            inputs=[
                [f["input"] for f in self.filter_elements]

            ]
        )

        def update_scatter(
            filters: tuple[str, list[int], list[int], list[int]]
			#scatter_y: str, age_range: list[int], wage_range: list[int], overall_range: list[int]
        ):
            scatter_y, age_range, wage_range, overall_range = filters
		
			scatter_data = scatter(
				and_(dataframe, [
					number_range("Age", age_range[0], age_range[1]),
					number_range("Wage(in Euro)", wage_range[0], wage_range[1]),
					number_range("Overall", overall_range[0], overall_range[1])
				]).reset_index(),
				x="Age",
				y=scatter_y,
				opacity=0.4, # Transparenz einzelner Datenpunkte
				color="blue",
				marginal="box" if self.show_boxplot else None,
				hover_data=["Full Name", "index"]
			
			)

            return scatter_data


	def html(self) -> Sequence[Component]:
		return [self.title, self.graph, self.scatter_graph] + [
			input_element["element"] for input_element in self.filter_elements
		]

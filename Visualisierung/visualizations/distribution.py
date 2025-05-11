from enum import Enum
from typing import Sequence
from dash import Dash
from dash.dcc import Graph
from dash.dependencies import Output
from dash.development.base_component import Component
from dash.html import H3
from pandas import DataFrame
from plotly.express import histogram
from filter import and_, eq
from id import generate_id
from input import build_dropdown, build_radio_items
from visualizations.visualization import Visualization

class Distribution(Visualization):

	def __init__(self, app: Dash, dataframe: DataFrame, allowed_attributes: list[str]):
		self.title = H3("Verteilung der Items")

		GRAPH_ID = generate_id("graph-distribution")
		self.graph = Graph(GRAPH_ID)

		self.filter_elements =  [
			build_dropdown("Attribut auswählen", allowed_attributes, allowed_attributes[0]),
			build_dropdown("nach Club filtern", dataframe["Club Name"].unique().tolist()),
			build_dropdown("nach Nationality filtern", dataframe["Nationality"].unique().tolist()),
			build_dropdown("nach Best Position filtern", dataframe["Best Position"].unique().tolist()),
			build_dropdown("nach Age filtern", dataframe["Age"].unique().tolist()),
		]


		@app.callback(
			Output(GRAPH_ID, "figure"),
			inputs=[
				tuple(filter_element["input"] for filter_element in self.filter_elements),

			]
		)
		def update(
			filters: tuple[str, str, str, str, int]
		):
			column, club, nationality, best_position, age = filters

			chart = histogram(
				and_(dataframe, [
					eq("Club Name", club),
					eq("Nationality", nationality),
					eq("Best Position", best_position),
					eq("Age", age)
				]).reset_index(),
				x=column,
				marginal="box",
				hover_data=["Full Name", "index"]
			)

			return chart

	def html(self) -> Sequence[Component]:
		return [self.title, self.graph] + [
			input_element["element"] for input_element in self.filter_elements
		]

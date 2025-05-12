from enum import Enum
from typing import Sequence
from dash import Dash
from dash.dcc import Graph
from dash.dependencies import Output
from dash.development.base_component import Component
from dash.html import H3
from pandas import DataFrame
from plotly.express import histogram
from filter import and_, eq, number_range
from id import generate_id
from input import build_dropdown, build_radio_items, build_rangeslider
from visualizations.visualization import Visualization

class Distribution(Visualization):

	def __init__(self, app: Dash, dataframe: DataFrame, allowed_attributes: list[str], show_boxplot: bool = True):
		self.title = H3("Verteilung der Items")

		GRAPH_ID = generate_id("graph-distribution")
		self.graph = Graph(GRAPH_ID)
		self.show_boxplot = show_boxplot

		self.filter_elements =  [
			build_dropdown("Attribut auswählen", allowed_attributes, allowed_attributes[0]),
			build_dropdown("nach Club filtern", dataframe["Club Name"].unique().tolist()),
			build_dropdown("nach Nationality filtern", dataframe["Nationality"].unique().tolist()),
			build_rangeslider("nach Age filtern", int(dataframe["Age"].min()), int(dataframe["Age"].max())),
			build_rangeslider("nach Wage (in Euro) filtern", int(dataframe["Wage(in Euro)"].min()), int(dataframe["Wage(in Euro)"].max())),
			build_rangeslider("nach Overall filtern", int(dataframe["Overall"].min()), int(dataframe["Overall"].max()))
		]


		@app.callback(
			Output(GRAPH_ID, "figure"),
			inputs=[
				tuple(filter_element["input"] for filter_element in self.filter_elements),
			]
		)
		def update(
			filters: tuple[str, str, str, list[int], list[int], list[int]]
		):
			column, club, nationality, age_range, wage_range, overall_range = filters

			chart = histogram(
				and_(dataframe, [
					eq("Club Name", club),
					eq("Nationality", nationality),
					number_range("Age", age_range[0], age_range[1]),
					number_range(column,wage_range[0], wage_range[1]),
					number_range("Overall", overall_range[0], overall_range[1])
				]).reset_index(),
				x=column,
				marginal="box" if self.show_boxplot else None,
				hover_data=["Full Name", "index"]
			)

			return chart

	def html(self) -> Sequence[Component]:
		return [self.title, self.graph] + [
			input_element["element"] for input_element in self.filter_elements
		]

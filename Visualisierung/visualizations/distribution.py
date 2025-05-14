from typing import Sequence, Union
from dash import Dash
from dash.dcc import Graph
from dash.dependencies import Output
from dash.development.base_component import Component
from dash.html import H3
from pandas import DataFrame
from plotly.express import histogram
from filter import and_, number_range, multi_eq
from id import generate_id
from input import build_dropdown, build_rangeslider
from visualizations.visualization import Visualization

class Distribution(Visualization):
#Initialisierung der Werteverteilung mit Filterung durch Dropdown und Rangelsider Komponenten und der Möglichkeit einen Boxplot anzuzeigen zur prominenten Darstellung von Ausreisern
	def __init__(self, app: Dash, dataframe: DataFrame, allowed_attributes: list[str], show_boxplot: bool = True):
		self.title = H3("Verteilung der Items")

		GRAPH_ID = generate_id("graph-distribution")
		self.graph = Graph(GRAPH_ID)
		self.show_boxplot = show_boxplot

		self.filter_elements =  [
			build_dropdown("Attribut auswählen", allowed_attributes, allowed_attributes[0], multi=False, clearable=False),
			build_dropdown("nach Club filtern", dataframe["Club Name"].unique().tolist(), multi=True, clearable=True),
			build_dropdown("nach Nationality filtern", dataframe["Nationality"].unique().tolist(),multi=True, clearable=True),
			build_rangeslider("nach Age filtern", int(dataframe["Age"].min()), int(dataframe["Age"].max())),
			build_rangeslider("nach Wage (in Euro) filtern", int(dataframe["Wage(in Euro)"].min()), int(dataframe["Wage(in Euro)"].max())),
			build_rangeslider("nach Overall filtern", int(dataframe["Overall"].min()), int(dataframe["Overall"].max()))
		]


		@app.callback(
			Output(GRAPH_ID, "figure"),
			#Input des Callbacks ist ein Tupel aus den Werte der Filter-Komponenten
			inputs=[
				tuple(filter_element["input"] for filter_element in self.filter_elements),
			]
		)
		def update(
			filters: tuple[str, Union[list[str], str], Union[list[str],str], list[int], list[int], list[int]]
		):
			column, club, nationality, age_range, wage_range, overall_range = filters
			#Festlegung des Graphs als Histogramm
			chart = histogram(
				and_(dataframe, [
					multi_eq("Club Name", club),
					multi_eq("Nationality", nationality),
					number_range("Age", age_range[0], age_range[1]),
					number_range("Wage(in Euro)",wage_range[0], wage_range[1]),
					number_range("Overall", overall_range[0], overall_range[1])
				#Ermöglicht eine korrekte Zuordnung und Anzeige der Datenpunkte
				]).reset_index(),
				x=column,
				marginal="box" if self.show_boxplot else None,
				hover_data=["Full Name", "index"]
			)

			return chart

	#Distribution erbt von Visualization und definiert die Struktur des User Interfaces
	def html(self) -> Sequence[Component]:
		return [self.title, self.graph] + [
			input_element["element"] for input_element in self.filter_elements
		]

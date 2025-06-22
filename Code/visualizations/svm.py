import numpy as np
import matplotlib.pyplot as plt
from base64 import b64encode
from dash import Dash
from dash.dcc import Dropdown, Graph
from dash.dependencies import Input, Output
from dash.html import H1, H3, H5, Div, Img
from io import BytesIO
from src.models import SVMResult
from pandas import DataFrame, Series
from plotly.graph_objs import Contour, Figure, Scatter
from sklearn.decomposition import PCA
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from src.visualizations.shared import generate_confusion_matrix, generate_id, generate_score_chart

class SVMVisualization:

	def __init__(self, dash: Dash, results: list[SVMResult], X: DataFrame, y: Series):
		SCORE_GRAPH_ID = generate_id()
		DROPDOWN_SCORE_GRAPH_ORDER_ID = generate_id()
		DROPDOWN_SELECT_A_ID = generate_id()
		DROPDOWN_SELECT_B_ID = generate_id()
		CONFUSION_MATRIX_A_ID = generate_id()
		CONFUSION_MATRIX_B_ID = generate_id()
		DECISION_BOUNDARY_DISPLAY_A = generate_id()
		DECISION_BOUNDARY_DISPLAY_B = generate_id()


		#Ändert Score-Diagramm je nach Änderung der Soortierreihenfolge
		@dash.callback(
			Output(SCORE_GRAPH_ID, "figure"),
			Input(DROPDOWN_SCORE_GRAPH_ORDER_ID, "value")
		)
		def update_score_graph(order):
			return generate_score_chart(results, self.result_to_string, order)

		#Auswahl von zwei Modellen um sie zu vergleichen und Änderung von Konfusionsmatrizen und Entscheidungsgrenzen
		@dash.callback(
			inputs=[
				Input(DROPDOWN_SELECT_A_ID, "value"),
				Input(DROPDOWN_SELECT_B_ID, "value")
			],
			output=[
				Output(CONFUSION_MATRIX_A_ID, "src"),
				Output(CONFUSION_MATRIX_B_ID, "src"),
				Output(DECISION_BOUNDARY_DISPLAY_A, "src"),
				Output(DECISION_BOUNDARY_DISPLAY_B, "src")
			]
		)
		def update(i, j):
			a = results[i]
			b = results[j]

			a_estimator = a["estimator"]
			a_X_test = X.iloc[a["indices"]["test"]]
			a_y_test = y.iloc[a["indices"]["test"]]

			b_estimator = b["estimator"]
			b_X_test = X.iloc[b["indices"]["test"]]
			b_y_test = y.iloc[b["indices"]["test"]]

			return [
				generate_confusion_matrix(a_estimator, a_X_test, a_y_test),
				generate_confusion_matrix(b_estimator, b_X_test, b_y_test),
				self.generate_decision_boundary_plot(a_estimator, a_X_test, a_y_test),
				self.generate_decision_boundary_plot(b_estimator, b_X_test, b_y_test)
			]

		self.container = Div(
			[
				H1("SVM"),
				H3("Scores"),
				Graph(
					id=SCORE_GRAPH_ID
				),
				H5("order by"),
				Dropdown(
					id=DROPDOWN_SCORE_GRAPH_ORDER_ID,
					options=["params", "accuracy", "precision", "recall", "f1"],
					value="params",
					style={"width": "250px"}
				),
				H3("compare"),
				Div(
					[
						Div([
			 				self.build_select_model_dropdown(DROPDOWN_SELECT_A_ID, results),
		 					Img(id=CONFUSION_MATRIX_A_ID),
		 					Img(id=DECISION_BOUNDARY_DISPLAY_A)
						], style={"margin-right": "5px"}),
						Div([
				 			self.build_select_model_dropdown(DROPDOWN_SELECT_B_ID, results, len(results) - 1),
							Img(id=CONFUSION_MATRIX_B_ID),
	 						Img(id=DECISION_BOUNDARY_DISPLAY_B)
						])
					],
					style={"display": "flex"}
				)
			]
		)

	#Dropdown-Menüs erstellen, damit Modelle ausgewählt werden können
	def build_select_model_dropdown(self, id: str, results: list[SVMResult], value: int = 0):
		options = sorted(
			[
				{
					"label": self.result_to_string(result),
					"value": i
				} for i, result in enumerate(results)
			],
			key=lambda d: d["label"]
		)

		return Dropdown(
			id=id,
			options=options,
			value=options[value]["value"],
			style={"width": "100%"}
		)

	#Entscheidungsgrenzen durch ein Streudiagramm visualisieren mithilfe von Dimensionsreduktion (PCA)
	def generate_decision_boundary_plot(self, estimator: Pipeline, X: DataFrame, y: Series):
		pca = PCA(n_components=2)

		X_reduced = pca.fit_transform(estimator[0].transform(X))

		xx, yy = np.meshgrid(
			np.linspace(X_reduced[:, 0].min() - 1, X_reduced[:, 0].max() + 1, 250),
			np.linspace(X_reduced[:, 1].min() - 1, X_reduced[:, 0].max() + 1, 250)
		)

		grid = np.vstack([xx.ravel(), yy.ravel()]).T

		z = np.reshape(estimator[1].predict(pca.inverse_transform(grid)), xx.shape)

		db = DecisionBoundaryDisplay(
			xx0=xx,
			xx1=yy,
			response=z
		)

		db.plot(
			alpha=0.5,
			plot_method="pcolormesh",
			cmap="viridis_r"
		)

		scatter = plt.scatter(
			X_reduced[:, 0],
			X_reduced[:, 1],
			c=y,
			edgecolors="k",
			cmap="viridis_r"
		)

		plt.legend(handles=scatter.legend_elements()[0], labels=[0, 1])

		bio = BytesIO()
		plt.savefig(bio, format="png")
		bio.seek(0)
		plt.close(db.figure_) # type: ignore

		src = b64encode(bio.read()).decode("utf-8").replace("\n", "")

		return f"data:image/png;base64,{src}"

	#Modellparameter zu lesbarem String formatieren
	def result_to_string(self, result: SVMResult):
		string = f"C: {result['params']['C']}, kernel: {result['params']['kernel']}"

		gamma = result["params"].get("gamma")

		if gamma:
			string += f", gamma: {gamma}"

		return string

	def html(self):
		return self.container

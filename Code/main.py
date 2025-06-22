from typing import cast
from dash import Dash
from pandas import DataFrame, Series
from data import load_data
from models import mlp, svm
from visualizations.mlp import MLPVisualization
from visualizations.svm import SVMVisualization

def main() -> None:
	#Daten laden und entfernen der NaN-Werte
	dataframe = load_data("pulsar_data.csv").dropna()

	#Trennen der Daten in Features (X) und Zielvariable (y)
	X: DataFrame = dataframe.loc[:, dataframe.columns != "target_class"]
	y: Series = cast(Series, dataframe["target_class"])

	#Trainieren der verschiedenen Modelle
	svm_results = svm(X, y)
	mlp_results = mlp(X, y)

	app = Dash()

	app.layout = [
		SVMVisualization(app, svm_results, X, y).html(),
		MLPVisualization(app, mlp_results, X, y).html()
	]

	app.run(debug=False)

if __name__ == "__main__":
	main()

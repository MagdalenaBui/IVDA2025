from dash import Dash
from data import load, remove_dots_before_commas
from visualizations.linear_regression_np import LinearRegressionVis
from visualizations.cluster import ClusterVis
import numpy as np

def main() -> None:

    remove_dots_before_commas()
    #dataframe = load("wein_cleaned.csv")
    data, column_names = load("wein_cleaned.csv")

    dash = Dash()

    visualizations = [
        LinearRegressionVis(data, column_names, dash),
        ClusterVis(data, column_names, dash)
    ]

    dash.layout = [
        component for visualization in visualizations for component in visualization.html()
    ]

    dash.run(debug=True)

if __name__ == "__main__":
	main()

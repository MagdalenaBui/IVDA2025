from dash import Dash
from data import load
from visualizations.comparison import Comparison
from visualizations.distribution import Distribution

def main() -> None:
	dataframe = load("Aufgabe-1_clean.csv")

	app = Dash()

	visualizations = [
		Distribution(app, dataframe, ["Age", "Wage(in Euro)", "Overall"], show_boxplot=True),
		Distribution(app, dataframe, ["Nationality", "Club Name"], show_boxplot= False),
		Comparison(app, dataframe, "Overall")
	]
#What: # Layout ist eine Liste von Komponenten, die in der App angezeigt werden sollen
	app.layout = [
		component for visualization in visualizations for component in visualization.html()
	]

	app.run(debug=True)

if __name__ == "__main__":
	main()

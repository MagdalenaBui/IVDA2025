from dash import Dash
from data import load
from visualizations.distribution import Distribution

def main() -> None:
	dataframe = load("Aufgabe-1_clean.csv")
	#print(dataframe)

	app = Dash()

	visualizations = [
		Distribution(app, dataframe, ["Age", "Wage(in Euro)", "Overall"], show_boxplot=True),
		Distribution(app, dataframe, ["Nationality", "Club Name"], show_boxplot= False)
	]
#What
	app.layout = [
		component for visualization in visualizations for component in visualization.html()
	]

	app.run(debug=True)

if __name__ == "__main__":
	main()

from dash import Dash
from numpy import nan
from pandas import DataFrame, to_numeric
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from data import load, data_cleaning
from validation import bootstrap, kfold
from visualizations.evaluation import Evaluation

def main() -> None:
	data_cleaning('titanic.csv', 'titanic_cleaned.csv')
	dataframe = load('titanic_cleaned.csv')

	#Datenvorverarbeitung: Variablen Sex und Embarked werden mit LabelEncoder in numerische Werte umgewandelt und Fehlende Werte werden durch einen Mittelwert ersetzt
	encoder = LabelEncoder()
	imputer = SimpleImputer(missing_values=nan, strategy="mean")

	#Trennung in Ziel- ("Survived") und Merkmalsvariablen ("Survived", "PassengerId")
	Y = dataframe["Survived"]
	X = dataframe.drop(columns=["Survived", "PassengerId"])

	# Umwandeln in numerische Werte
	X.loc[:, "Sex"] = encoder.fit_transform(X["Sex"])
	X.loc[:, "Embarked"] = encoder.fit_transform(X["Embarked"])

	# Sicherstellen des numerischen Werteformat
	X["Sex"] = to_numeric(X["Sex"])
	X["Embarked"] = to_numeric(X["Embarked"])

	#Für X werden nur numerische Werte genutzt
	X = X._get_numeric_data()

	# Ersetzt fehlende Werte
	X = DataFrame(imputer.fit_transform(X), columns=X.columns)

	dash = Dash()

	results = [
		(name, [kfold(model, X, Y), bootstrap(model, X, Y)]) for name, model in	[
			("Logistic Regression", LogisticRegression(max_iter=200)),
			("Decision Tree Classifier", DecisionTreeClassifier()),
			("K Neighbors Classifier", KNeighborsClassifier(n_neighbors=3))
		]
	]

	visualizations = [
		Evaluation(results, X, Y)
	]

	dash.layout = [
		component for visualization in visualizations for component in visualization.html()
	]

	dash.run(debug=True)


if __name__ == "__main__":
	main()
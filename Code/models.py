from typing import Dict, Literal, NotRequired, Tuple, TypedDict, cast
from numpy import argmax, float64, int64
from numpy.typing import NDArray
from pandas import DataFrame, Series
from sklearn.base import BaseEstimator
from sklearn.model_selection import ParameterGrid, cross_validate
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

#Basis-Ergebnistyp für beide Modelle
class Result(TypedDict):
	fit_time: float64
	score_time: float64
	estimator: Pipeline
	indices: Dict[Literal["test", "train"], NDArray[int64]]
	accuracy: float64
	f1: float64
	precision: float64
	recall: float64

class SVMParams(TypedDict):
	C: int
	gamma: NotRequired[str]
	kernel: str

class SVMResult(Result):
	params: SVMParams

class MLPParams(TypedDict):
	hidden_layer_sizes: Tuple[int]
	activation: str

class MLPResult(Result):
	params: MLPParams

class SLPParams(TypedDict):
	hidden_layer_sizes: Tuple[int]
	activation: str

class SLPResult(Result):
	params: MLPParams

# Kreuzvalidierung zum AUfteilen der Daten in Test- und Trainingsdaten mit Datennormalisierung (Standardscaler) und Berechnung der verschiedenen Metriken, wobei nach der Accuracy das beste Modell gewählt wird
def cv(estimator: type[BaseEstimator], configs, X: DataFrame, y: Series) -> list[Result]:
	results = []

	for config in configs:
		print(config)


		result = cross_validate(
			make_pipeline(
				StandardScaler(),
				estimator(**config)
			),
			X,
			y,
			cv=10,
			return_estimator=True,
			return_indices=True,
			scoring=["accuracy", "f1", "precision", "recall"],
			n_jobs=-1 #parallele Verarbeitung auf allen Verfügbaren CPU-Kernen, damit die Rechenzeit nicht zu hoch wird
		)

		best_index = argmax(result["test_accuracy"])

		for key in result:
			if key == "indices":
				result[key]["train"] = result[key]["train"][best_index]
				result[key]["test"] = result[key]["test"][best_index]
				continue

			result[key] = result[key][best_index]

		result["params"] = config

		results.append(
			{ (key[5:] if key.startswith("test_") else key): result[key] for key in result }
		)

	return results

#SVM Klassifikation mit verschiedenen Hyperparametern (Kernel, C-Werte, Gamma-Werte)
def svm(X: DataFrame, y: Series) -> list[SVMResult]:
	C = [0.01, 0.1, 1, 10]

	result = cv(
		SVC,
		list(
			ParameterGrid({
				"kernel": ["rbf", "poly"],
				"C": C,
				"gamma": [0.01, 0.1]
			}),
		) + list(
			ParameterGrid({
				"kernel": ["linear"],
				"C": C
			})
		),
		X,
		y
	)

	return cast(list[SVMResult], result)

#MLP KLassifikation mit zwei Netzwerk-Konfigurationen
def mlp(X: DataFrame, y: Series) -> list[MLPResult]:
	result = cv(
		MLPClassifier,
		[
			{ "hidden_layer_sizes": (10, 10, 10), "max_iter": 2000},
			{ "hidden_layer_sizes": (14, 14, 14), "max_iter": 2000}
		],
		X,
		y
	)

	return cast(list[MLPResult], result)

def slp(X: DataFrame, y: Series) -> list[SLPResult]:
	result = cv(
		MLPClassifier,
		[
			{ "hidden_layer_sizes": (4,),"max_iter": 2000},
			{"hidden_layer_sizes": (8,),"max_iter": 2000}
		],
		X,
		y
	)
	return cast(list[SLPResult], result)

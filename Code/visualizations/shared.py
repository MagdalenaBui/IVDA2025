from base64 import b64encode
from io import BytesIO
from typing import Callable, TypeVar
from matplotlib.pyplot import close, savefig
from plotly.graph_objs import Bar, Figure
from sklearn.pipeline import Pipeline
from src.models import MLPResult, SVMResult
from pandas import DataFrame, Series
from sklearn.metrics import ConfusionMatrixDisplay
from uuid import uuid4

def generate_id():
	return str(uuid4())

T = TypeVar("T", bound=SVMResult | MLPResult)

#Balkendiagramm für Accuracy, Precision, Recall und F1-Score
def generate_score_chart(results: list[T], params_to_string: Callable[[T], str], order_by: str) -> Figure:
	dataframe = DataFrame(
		[
			{
				key: result[key]
				if key != "params"
				else params_to_string(result)
				for key in ["params", "accuracy", "precision", "recall", "f1"]
			}
			for result in results
		]
	).sort_values(order_by, ascending=order_by=="params")

	data = [
		Bar(
			x=dataframe["params"],
			y=dataframe[key],
			name=key
		)
		for key in dataframe
		if key != "params"
	]

	figure = Figure(data=data)

	figure.update_layout(
		bargap=0.5,
		barmode="group"
	)

	return figure

#Confusion-Matrix erstellen und als PNG zurückgeben
def generate_confusion_matrix(estimator: Pipeline, X: DataFrame, y: Series) -> str:
	confusion_matrix = ConfusionMatrixDisplay.from_estimator(estimator, X, y)

	confusion_matrix.plot(colorbar=False)

	bio = BytesIO()
	savefig(bio, format="png")
	bio.seek(0)
	close(confusion_matrix.figure_)

	src = b64encode(bio.read()).decode("utf-8").replace("\n", "")

	return f"data:image/png;base64,{src}"

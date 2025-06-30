from base64 import b64encode
from dash import Dash
from dash.dcc import Graph
from dash.html import H1, H3, H5, Div, Img
from io import BytesIO
from matplotlib.pyplot import close, savefig
from src.models import SLPResult
from pandas import DataFrame, Series
from plotly import colors
from plotly.graph_objs import Figure, Scatter
from sklearn.model_selection import LearningCurveDisplay
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from typing import cast
from src.visualizations.shared import generate_confusion_matrix, generate_score_chart


class SLPVisualization:

    def __init__(self, dash: Dash, results: list[SLPResult], X: DataFrame, y: Series):
        [a, b] = results

        if self.result_to_string(a) > self.result_to_string(b):
            [a, b] = [b, a]

        self.container = Div(
            [
                H1("SLP"),
                H3("Scores"),
                Graph(
                    figure=generate_score_chart(results, self.result_to_string, "params")
                ),
                H3("Vergleich"),
                Div(
                    [self.generate_visualizations(a, X, y), self.generate_visualizations(b, X, y)],
                    style={"display": "flex"}
                )
            ]
        )

    # Visualisierung beinhalten die Confusion-Matrix, Topologie-Graph und Learning-Curve und Loss-Curve
    def generate_visualizations(self, result: SLPResult, X: DataFrame, y: Series):
        estimator = result["estimator"]
        indices = result["indices"]

        # Confusion-Matrix
        return Div([
            H5(self.result_to_string(result)),
            Img(
                src=generate_confusion_matrix(
                    estimator,
                    X.iloc[indices["test"]],
                    y.iloc[indices["test"]]
                )
            ),
            # Topologie-Graph
            Graph(figure=self.generate_topology_graph(
                cast(MLPClassifier, result["estimator"][1]).coefs_)
            ),
            # Learning-Curve und Loss-Curve
            Img(
                src=self.generate_learning_curve(
                    estimator,
                    X.iloc[indices["train"]],
                    y.iloc[indices["train"]]
                )
            ),
            Graph(figure=self.generate_loss_curve_graph(estimator))
        ])

    # Topologie des SLP Modells mit Darstellung der Gewichte zwischen den Neuronen
    def generate_topology_graph(self, weights: list[list[list[int]]]) -> Figure:
        flat = [a for c in weights for b in c for a in b]
        min_w = min(flat)
        max_w = max(flat)

        traces = []

        largest = len(max(weights, key=len))

        colorscale = "Viridis"

        weights.extend([[[]]])

        for x in range(0, len(weights)):
            for y in range(0, len(weights[x])):
                y_offset = (largest - len(weights[x])) / 2

                for y_2 in range(0, len(weights[x][y])):
                    y_2_offset = (largest - len(weights[x + 1])) / 2

                    traces.append(
                        Scatter(
                            x=[x, x + 1],
                            y=[y + y_offset, y_2 + y_2_offset],
                            mode="lines",
                            line=dict(
                                color=
                                colors.sample_colorscale(colorscale, [(weights[x][y][y_2] - min_w) / (max_w - min_w)])[
                                    0],
                                width=1
                            ),
                            hoverinfo="skip"
                        )
                    )

        nodes_x = []
        nodes_y = []
        node_text = []

        for x in range(0, len(weights)):
            y_offset = (largest - len(weights[x])) / 2

            for y in range(0, len(weights[x])):

                nodes_x.append(x)
                nodes_y.append(y + y_offset)

                if x == len(weights) - 1:
                    continue

                node_text.append(
                    f"weights {x} -> {x + 1} <br>" +
                    "<br>".join([f"{i}: {round(w, 4)}" for i, w in enumerate(weights[x][y])])
                )

        traces.append(
            Scatter(
                x=nodes_x,
                y=nodes_y,
                text=node_text,
                mode="markers",
                marker=dict(
                    color="white",
                    size=10,
                    line_width=2
                ),
                name=""
            )
        )

        traces.append(
            Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(
                    colorscale=colorscale,
                    showscale=True,
                    cmin=min_w,
                    cmax=max_w,
                    colorbar=dict(
                        tickvals=[min_w, 0, max_w],
                        ticktext=[round(min_w, 2), 0, round(max_w, 2)]
                    )
                ),
                hoverinfo="skip"
            )
        )

        figure = Figure(data=traces)

        figure.update_layout(
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )

        return figure

    # Lernkurve
    def generate_learning_curve(self, estimator: Pipeline, X: DataFrame, y: Series) -> str:
        learning_curve = LearningCurveDisplay.from_estimator(estimator, X, y)

        learning_curve.plot()

        bio = BytesIO()
        savefig(bio, format="png")
        bio.seek(0)
        close(learning_curve.figure_)  # type: ignore

        src = b64encode(bio.read()).decode("utf-8").replace("\n", "")

        return f"data:image/png;base64,{src}"

    # Verlustfunktion
    def generate_loss_curve_graph(self, estimator: Pipeline) -> Figure:
        mlp = cast(MLPClassifier, estimator[1])

        figure = Figure(
            data=Scatter(
                x=[i for i in range(0, len(mlp.loss_curve_))],
                y=mlp.loss_curve_,
            )
        )

        figure.update_layout(
            xaxis_title="Number of Iterations",
            yaxis_title="Loss"
        )

        return figure

    def result_to_string(self, result: SLPResult):
        return f"hidden layer sizes: {result['params']['hidden_layer_sizes']}"

    def html(self):
        return self.container

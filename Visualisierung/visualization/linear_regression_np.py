from dash import Dash
from dash.dcc import Dropdown, Graph
from dash.dependencies import Input, Output
from dash.html import H3
import numpy as np
from plotly.graph_objects import Figure, Scatter
from sklearn.linear_model import LinearRegression
from id import generate_id
from visualizations.visualization import Visualization


class LinearRegressionViz(Visualization):
    def __init__(self, data: np.ndarray, column_names: list[str], dash: Dash):
        DROPDOWN_X_ID = generate_id("regression-dropdown-x")
        DROPDOWN_Y_ID = generate_id("regression-dropdown-y")

        self.data = data
        self.column_names = column_names

        self.dropdowns = [
            Dropdown(
                id=DROPDOWN_X_ID,
                options=column_names,
                value=column_names[0],
                style={
                    "max-width": "300px",
                    "margin-bottom": "10px"
                }
            ),
            Dropdown(
                id=DROPDOWN_Y_ID,
                options=column_names,
                value=column_names[1],
                style={
                    "max-width": "300px"
                }
            )
        ]

        GRAPH_ID = generate_id("regression-graph")
        self.graph = Graph(id=GRAPH_ID)

        @dash.callback(
            Output(GRAPH_ID, "figure"),
            Input(DROPDOWN_X_ID, "value"),
            Input(DROPDOWN_Y_ID, "value")
        )
        def update(x: str, y: str):
            x_idx = self.column_names.index(x)
            y_idx = self.column_names.index(y)

            xs = self.data[:, x_idx]
            ys = self.data[:, y_idx]

            # Lineare Regression mit sklearn
            model = LinearRegression()
            X = xs.reshape(-1, 1)
            model.fit(X, ys)

            # Vorhersagen berechnen
            y_pred = model.predict(X)

            # R-Quadrat berechnen
            rsquared = model.score(X, ys)

            # Figure erstellen
            figure = Figure()

            # Scatter Plot hinzufügen
            figure.add_trace(Scatter(
                x=xs,
                y=ys,
                mode='markers',
                name='Datenpunkte'
            ))

            # Regressionslinie hinzufügen
            figure.add_trace(Scatter(
                x=xs,
                y=y_pred,
                mode='lines',
                name='Regression',
                line=dict(color='red'),
                hovertemplate="<br>".join([
                    "<b>linear regression</b>",
                    f"r squared: {round(rsquared, 4)}",
                    "x = %{x}, y = %{y}"
                ])
            ))

            # Achsenbeschriftungen aktualisieren
            figure.update_layout(
                xaxis_title=x,
                yaxis_title=y
            )

            return figure

    def html(self):
        return [H3("Lineare Regression"), self.graph] + [dropdown for dropdown in self.dropdowns]

from dash.dcc import Graph, Tabs, Tab
import matplotlib.pyplot as plt
from io import BytesIO
from dash.html import H2, H3, H4, H5, H6, Div, Img
from pandas import DataFrame
from plotly.graph_objs import Bar, Figure
from sklearn.metrics import confusion_matrix
from sklearn.metrics._plot.confusion_matrix import ConfusionMatrixDisplay
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_graphviz
from visualizations.visualization import Visualization
from base64 import b64encode
from numpy import argmax, mean
from dash_interactive_graphviz import DashInteractiveGraphviz
import graphviz

class Evaluation(Visualization):
    def __init__(self, model_results, X,Y):
        self.div =Div(
            [
                *self.generate_score_chart(model_results),
                *self.generate_confusion_matrix(model_results, X,Y),
                *self.generate_tree_chart(model_results, X,Y)
            ]
        )

    def generate_score_chart(self, model_results):

        #Erstellt eine Liste von Scores aus model_results bestehend aus Keys, die mit "test_" anfangen
        score_names = [
            key for key in model_results [0][1][0].keys()
            if key.startswith("test_")
        ]

        scores = DataFrame([
            {
                #Für jeden Key in score_names + ["name"] wird, wenn er in score_names ist ein Mittelwert berechnet, sonst wird ein "Modellname (Split-Methode)" String erstellt
                key: mean(result[key])
                    if key in score_names
                    else f"{name} ({str(result['split_method'].value)})"
                    for key in score_names + ["name"]
            }
            for name, results in model_results
            for result in results
         ])

        #Balkendiagramm erstellen für jeden Score
        data = [
            Bar(
                y=scores[key],
                x=scores["name"],
                name=key[5:] #"test_" vom Namen entfernen
            )
            for key in scores
            if key != "split_method" and key != "name"
        ]

        figure = Figure(data=data)

        return [
            H2("Performance Evaluierung"),
            Graph(figure=figure)
        ]

    #Erstellt Confusion-Matrix für die verschiedenen Modelle
    def generate_confusion_matrix(self, model_results, X, Y):
        divs = []

        for name, results in model_results:
            graphs = []

            for result in results:
                cm = mean([
                    confusion_matrix(Y[test], estimator.predict(X.iloc[test]))
                    for estimator, test
                    in zip(result["estimator"], result["indices"]["test"])
                ], axis=0)

                # Erstelle Heatmap mit Plotly
                figure = Figure(data=[
                    {
                        'type': 'heatmap',
                        'z': cm,
                        'x': [f'Predicted {i}' for i in range(len(cm))],
                        'y': [f'Actual {i}' for i in range(len(cm))],
                        'text': cm,
                        'texttemplate': '%{text:.1f}',
                        'textfont': {'size': 16},
                        'showscale': True,
                        'colorscale': 'Blues'
                    }
                ])

                figure.update_layout(
                    title=f'Confusion Matrix',
                    xaxis_title='Predicted Label',
                    yaxis_title='True Label',
                    width=500,
                    height=500
                )

                graphs.append(
                    Div([
                        H5(result["split_method"].value),
                        Graph(figure=figure)
                    ])
                )

            divs.append(
                Div([
                    H4(name),
                    *graphs
                ])
            )

        return [
            H2("Confusion matrix"),
            Div(
                divs,
                style={
                    "display": "flex",
                    "width": "100%",
                    "justify-content": "space-between",
                    "flex-wrap": "wrap"
                }
            )
        ]

    def generate_tree_chart(self, model_results, X, Y):
        # Ergebnisse des DecisionTreeClassifiers finden
        results = next(
            result[1] for result in model_results if isinstance(result[1][0]["estimator"][0], DecisionTreeClassifier))

        # Erstelle die Graphen für beide Validierungsmethoden
        graphs = []
        for result in results:
            # Besten Baum auswählen
            best_tree = result["estimator"][argmax(result["test_accuracy"])]

            dot = graphviz.Digraph()
            dot.attr(rankdir='LR')  # Links nach rechts Layout

            # DOT-Daten erstellen
            dot_data = export_graphviz(
                best_tree,
                feature_names=X.columns,
                filled=True,
                rounded=True,
                class_names=['0', '1'],
                out_file=None

            )

            # Graph mit Validierungsmethode als Label
            graphs.append({
                'label': result["split_method"].value,
                'graph': DashInteractiveGraphviz(dot_data,
                style = {'width': '100%', 'height': '800px'}
            )

            })

        return [
            H2("Decision Trees"),
            Tabs([
                Tab(
                    label=graph['label'],
                    children=graph['graph']
                ) for graph in graphs
            ])
        ]

    def html(self):
        return [self.div]


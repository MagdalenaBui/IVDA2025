from dash.dcc import Graph
import matplotlib.pyplot as plt
from io import BytesIO
from dash.html import H3, H5, H6, Div, Img
from pandas import DataFrame
from plotly.graph_objs import Bar, Figure
from sklearn.metrics import confusion_matrix
from sklearn.metrics._plot.confusion_matrix import ConfusionMatrixDisplay
from sklearn.tree import DecisionTreeClassifier, plot_tree
from visualization import Visualization
from base64 import b64encode
from numpy import argmax, mean

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
                #Für jeden Key in score_names + ["name"] wird, wenn er in score_names ist ein Mittelwert berechnet, sonst wird ein String erstellt
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
                name=key[5:]
            )
            for key in scores
            if key != "split_method" and key != "name"
        ]

        figure = Figure(data=data)

        return [
            H3("scores"),
            Graph(figure=figure)
        ]

    #Erstellt Confusion-Matrix für die verschiedenen Modelle
    def generate_confusion_matrix(self, model_results, X, Y):
            divs = []

        #Iteriere über alle Modelle und deren Ergebnisse
            for name, results in model_results:
                    images = []

                # Für jedes Trainingsergebnis wird der Durchschnitt der Confusion-Matrix berechnet
                    for result in results:
                        cm = mean(
                            [
                                confusion_matrix(Y[test], estimator.predict(X.iloc[test]))
                                for estimator, test
                                in zip(result["estimator"], result["indices"]["test"])
                            ],
                            axis=0
                        )

                        #Erstellt eine ConfusionMatrixDisplay-Instanz
                        cm = ConfusionMatrixDisplay(confusion_matrix=cm)

                        cm.plot(values_format=".1f")

                        #Plot wird als Bild im Speicher gespeichert
                        bio = BytesIO()
                        plt.savefig(bio, format="png")
                        bio.seek(0) # Cursor Zurücksetzten
                        plt.close() # Matplotlib Figur wieder schließen

                        #Bild konvertieren zu Base64
                        src = b64encode(bio.read()).decode("utf-8")

                        #Bild wird zum Container hinzugefügt
                        images.append(
                            Div(
                                [
                                    H6(result["split_method"].value),
                                    Img(src=f"data:image/png;base64,{src}")
                                ]
                            )
                        )

                    #Alle Bilder eines Modells werden zusammengefügt
                    divs.append(
                        Div(
                            [
                                H5(name),
                                *images
                            ]
                        )
                    )

                #Gibt HTML Struktur zurück
            return [
                    H3("confusion matrix"),
                    Div(
                        [*divs],
                        style={
                            "display": "flex",
                            "width": "100%",
                            "justify-content": "space-between"
                        }
                    )
                ]


    def generate_tree_chart(self, model_results, X, Y):
        # Ergebnisse des DecisionTreeCLassifiers finden
        results = next(
            result[1] for result in model_results if isinstance(result[1][0]["estimator"][0], DecisionTreeClassifier))

        # Beste Bäume auswählen durch die Accuracy des Tests (aber ist das wirklich das beste?)
        trees = [
            result["estimator"][argmax(result["test_accuracy"])] for result in results
        ]

        images = []

        # Erstellt Visualisierung für jeden Baum
        for tree in trees:
            plt.figure(figsize=(130, 50))  # Darstellung soll groß sein
            plot_tree(
                tree,
                fontsize=10,
                filled=True,
                rounded=True,
                feature_names=X.columns
            )

            # Baum wird als Bild gespeichert
            bio = BytesIO()
            plt.savefig(bio, format="png")
            bio.seek(0)
            plt.close()

            # Konvertiere Bild in Base64
            src = b64encode(bio.read()).decode("utf-8").replace("\n", "")

            images.append(Img(src=f"data:image/png;base64,{src}"))

        # Gibt HTML Struktur zurück
        return [
            Div(
                [
                    H3("Decision Trees"),
                    *images
                ]
            )
        ]


    def html(self):
        return [self.div]


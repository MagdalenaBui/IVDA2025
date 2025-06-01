from dash import Dash
from dash.dcc import Graph
from dash.html import H3
import numpy as np
from numpy.typing import NDArray
from plotly.graph_objects import Figure
from plotly.express import scatter
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import davies_bouldin_score, silhouette_score
from sklearn.preprocessing import MinMaxScaler
from visualizations.visualization import Visualization


class ClusterVis(Visualization):
    def __init__(self, data: np.ndarray, column_names: list[str], dash: Dash):
        # Entferne Ausreiser: Zeilen mit Farbwert 906
        farbwert_idx = column_names.index("Farbwert")
        mask = data[:, farbwert_idx] != 906
        filtered_data = data[mask]

        # Normalisierung des Wertebereichs der Daten auf zwischen 0 und 1
        normalized_data = MinMaxScaler().fit_transform(filtered_data)

        # PCA auf 2
        pca = PCA(n_components=2)
        self.reduced_data = pca.fit_transform(normalized_data)

        # Erstelle alle Plots
        self.score_graph = self.build_score_plot()
        self.cluster_graphs = self.build_all_cluster_plots()
        self.pca_graph = self.build_scree_plot(filtered_data)

    def build_score_plot(self) -> Graph:
        k_values = range(2, 10)
        silhouette_scores = []
        davies_bouldin_scores = []

		#Für jeden k-Wert wird K-Means durchgeführt und jeweilige Qualitätsmetriken berechnet
        for k in k_values:
            kmeans = KMeans(n_clusters=k)
            labels = kmeans.fit_predict(self.reduced_data)
            silhouette_scores.append(silhouette_score(self.reduced_data, labels))
            davies_bouldin_scores.append(davies_bouldin_score(self.reduced_data, labels))

        fig = Figure()
        for scores, name in [(silhouette_scores, 'Silhouette Coefficient'),
                             (davies_bouldin_scores, 'Davies-Bouldin')]:
            fig.add_trace({
                'type': 'scatter',
                'x': list(k_values),
                'y': scores,
                'name': name,
                'mode': 'lines+markers'
            })
        return Graph(figure=fig)

    def build_all_cluster_plots(self) -> list[Graph]:
        return [Graph(figure=scatter(
            x=self.reduced_data[:, 0],
            y=self.reduced_data[:, 1],
            color=KMeans(n_clusters=k).fit_predict(self.reduced_data),
            title=f'K-Means (k={k})',
            color_continuous_scale=["black", "blue", "purple", "red", "orange"]
        )) for k in range(2, 10)]

    def build_scree_plot(self, data: NDArray) -> Graph:
        pca = PCA()
        pca.fit(data)

        fig = Figure()
        fig.add_trace({
            'type': 'scatter',
            'x': list(range(1, len(pca.singular_values_) + 1)),
            'y': pca.singular_values_,
            'mode': 'lines+markers',
            'name': 'Eigenwerte'
        })
        return Graph(figure=fig)

    def html(self):
        return [
            H3("Silhouette Coefficient und Davies-Bouldin Index"),
            self.score_graph,
            H3("K-Means Clustering"),
            *self.cluster_graphs, #Anzeige/Entpacken aller Cluster-Plots
            H3("Scree Plot"),
            self.pca_graph
        ]

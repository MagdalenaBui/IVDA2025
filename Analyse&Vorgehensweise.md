# Analyse Datensatz 

## 1. Einlesen und erkennen von Datumswert 
Datums Attribut fehlt -> versteckt in anderen Daten, min und max Werte bestimmen um Spalte mit Ausreißern zu erkennen -> da automatisiert Datenveränderung stattgefunden hat wird sich hier ein Muster zeigen. Andere mögliche Ideen: korrekte Formatierung (einige Werte mit . und , getrennt -> Formatierung in nachfolgenden Zellen also auch betroffen und fehlerhaft.) 

- , ist Separator/Delimiter und . wird in der Value Trennung genutzt bzw. ist das der Standard Float Trennzeichen -> Werte mit einer Schleife durchgehen und korrigieren
- ., werden random in den Werten versteckt vertauscht, aber wenigstens 1x bis zu 3x pro Zeile (auf den ersten Blick) -> Datumswert kann gebildet werden (YAY!)
- Datentypen Vergleich, ist Spalte float oder int und würde nach der Reinigung dann der Wert noch passen -> automatisches erkennen 

## 2. Lineare Regression von zwei Attributen 

- Visualisierung, frei wählbare Attribute
- Qualitätswerte der Regression (?) -> Erfolgsparameter, Durchschnittswert & Median, Top und Bottom 10% der Daten markieren

## 3. k-Means Clustering , Silhouette Coefficient & Daviies Bouldin Index (optimale Clusteranzahl)

- k-Means mit 2 bis 5 Clustern berechnen
- Berechnung und Visualisierung des Silhouette Coefficient & Davies Boulding Index 

## 4. Scatterplot, Dimensionsreduktion PCA, Scree Plot 

- PCA & Scree Plot visualisieren
- Datenpunkte nach Cluster einfärben 

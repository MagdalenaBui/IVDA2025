# Analyse Datensatz 

Datums Attribut fehlt -> versteckt in anderen Daten, min und max Werte bestimmen um Spalte mit Ausreißern zu erkennen -> da automatisiert Datenveränderung stattgefunden hat wird sich hier ein Muster zeigen. Andere mögliche Ideen: korrekte Formatierung (einige Werte mit . und , getrennt -> Formatierung in nachfolgenden Zellen also auch betroffen und fehlerhaft.) 

- , ist Separator/Delimiter und . wird in der Value Trennung genutzt bzw. ist das der Standard Float Trennzeichen -> Werte mit einer Schleife durchgehen und korrigieren
- ., werden teilweise random in den Werten versteckt vertauscht 

# datacleaning

Mögliche Probleme:

- Duplikate
- fehlerhafte Spaltentrennung z.B. Edgar Badia hat Kommas in seinem Value (in Euro) Key → deswegen falsch getrennt
    - gelöst durch delimiter: ' ‘
- fehlerhafte Markierung von Zeichenketten
    - gelöst durch  quotechar: " ' ”
- gemischte Datentypen bei Spalten vom Typ objects z.B. Value in Euros ist ein str und muss in float
- Missing Values in: nationality, height, weight, international reputation, positioning, goal keeper handling
    - gelöst durch einheitliches behandeln von missing Values als NA
 
# Datenvorbereitung mit Python

In diesem Notebook laden wir den Datensatz `Aufgabe-1.csv` ein, identifizieren typische Probleme (Trennzeichen, fehlende Werte, falsche Typen, Inkonsistenzen in Strings, Ausreißer) und bereinigen sie schrittweise. Am Ende speichern wir die bereinigte Datei ab.



Zusammenfassung der Arbeitsschritte

- Format­erkennung mit csv.Sniffer
- Einlesen mit korrekten Parametern und on_bad_lines='warn'

- Inspektion (Typen, fehlende Werte, Ausreißer)
- Bereinigung
  - String-Säuberung und Vereinheitlichung
  - Entfernen von Null-Werten, Duplikaten und anderen Inkonsistenzen - negative Werte, keine einheitliche Nullwert Behandlung 

- Speichern des sauberen Datensatzes


## 2. Dateiformat automatisch erkennen

Statt blind auf Komma oder Semikolon zu setzen, liest `csv.Sniffer()` eine Probe und ermittelt das Trennzeichen (`delimiter`) und das Zeichen für String-Markierung (`quotechar`). Diese können wir danach direkt als Variable nutzen. 



## 3. Datensatz einlesen

Nun laden wir die CSV mit den ermittelten Parametern.  
- `sep=delimiter`: korrektes Spaltentrennzeichen  
- `quotechar=quotechar`: z. B. Anführungszeichen um Strings  
- `encoding='utf-8'`: Annahme; ggf. anpassen, falls Fehler auftreten.



## 4. Erste Inspektion

- `df.info()`: Datentypen, Null-Werte  
- `df.describe()`: statistische Kennzahlen der numerischen Spalten  
- `df.isnull().sum()`: Anzahl fehlender Werte pro Spalte  

### Wofür?

- Fehlende Werte müssen wir später entweder entfernen oder sinnvoll ersetzen.
- Falsche Datentypen (z. B. Zahlen als Strings) müssen korrigiert werden.
- `on_bad_lines='warn'` fängt Zeilen mit unpassender Spaltenzahl und zeigt, wo Probleme sind. Sorgt dafür das nicht korrekt formatierte Zeilen auch eingelesen werden


## 4b. Tiefergehende Typ-Analyse

Um zu erkennen, ob Spalten nicht den erwarteten Datentyp haben oder gemischte Typen enthalten, führen wir nun:

- Eine Übersicht über `df.dtypes`
- Überischt über Datentypen der Object Spalten: Gibt die Anzahl der vorhandenen Elemente zurück, können auch NaN Werte oder andere Datentypen sein
- Übersicht über Datentypen der nummerischen Spalten: Gibt die Anzahl der vorhandenen Elemente zurück, können auch NaN Werte oder andere Datentypen sein

- Übersicht über problematische Spalten, hilft Potenzielle Probleme im Datensatz zu identifizieren, die vor der weiteren Analyse oder Verarbeitung behoben werden müssen. Dies umfasst insbesondere fehlende Werte, inkonsistente Datentypen und nicht-numerische Einträge in numerischen Spalten. 
Der Ablauf ist wie folgt:

1. **Initialisierung einer Liste für den Bericht**:
   - Eine leere Liste `report` wird erstellt, um Informationen zu jeder Spalte zu sammeln.

2. **Iterieren über alle Spalten**:
   - Für jede Spalte im DataFrame werden folgende Analysen durchgeführt:
     - **Fehlende Werte**: Die Anzahl der fehlenden Werte (`NaN`) wird mit `isnull().sum()` ermittelt.
     - **Datentyp**: Der aktuelle Datentyp der Spalte wird mit `dtype` erfasst.
     - **Gemischte Typen**: Es wird geprüft, ob die Spalte mehrere Python-Datentypen enthält (z. B. Strings und Zahlen). Dies wird durch Zählen der verschiedenen Typen in der Spalte erreicht.
     - **Nicht-numerische Einträge**: Für Spalten mit dem Typ `object` wird geprüft, wie viele Einträge sich nicht in numerische Werte umwandeln lassen.

3. **Erstellen eines Berichts**:
   - Die gesammelten Informationen zu jeder Spalte (Name, Datentyp, Anzahl fehlender Werte, gemischte Typen, nicht-numerische Einträge) werden als Dictionary in die `report`-Liste eingefügt.

4. **Erstellen eines DataFrames aus dem Bericht**:
   - Die `report`-Liste wird in einen DataFrame (`report_df`) umgewandelt, um die Ergebnisse übersichtlich darzustellen.

5. **Filtern problematischer Spalten**:
   - Es werden nur die Spalten angezeigt, die mindestens eines der folgenden Probleme aufweisen:
     - Fehlende Werte (`Missing values > 0`)
     - Gemischte Typen (`Mixed types`)

6. **Ausgabe der problematischen Spalten**:
   - Die problematischen Spalten und ihre Kennzahlen werden mit `print(problems.to_string(index=False))` ausgegeben.



## 5. Ausreißer und Null-Werte behandeln

- clean_value_in_euro-Funktion:
  - Abbruch bei Buchstaben sichert, dass fälschlich übergelaufener Text oder ein falsches Parsing nicht in unseren Zahlen landet.
  - Regex entfernt alle anderen unerwünschten Zeichen.
  - Apostroph wird als Tausender-Trenner gelöscht.
  - Es gibt keinen Standarddezimal Trenner mehr  
  - pd.to_numeric(..., errors='coerce') wandelt strings in Floats um, und setzt unlösbare Fälle in NaN.

- Damit ist die Spalte Value(in Euro) hinterher durchgängig ein int64 mit NaN für ungültige oder fehlende Einträge.



## Datentyp-Korrekturen und Bereinigung

- Missing-Value-Marker: Wir ersetzen alle gängigen Platzhalter ("N/A", "n/a", "NaN", "nan", "NULL", "null", "None", "none", "0" etc.) durch NA.
- Nullwerte und Negative Werte werden zu NA
- Duplikatentfernung 



## 6. Bereinigten Datensatz speichern

Am Ende speichern wir die bereinigte CSV ab. So bleibt das Original unverändert und wir haben jederzeit den sauberen Datensatz griffbereit.

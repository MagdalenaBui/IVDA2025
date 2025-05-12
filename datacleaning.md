# datacleaning

Mögliche Probleme:

- Duplikate
- fehlerhafte Spaltentrennung z.B. Edgar Badia hat Kommas in seinem Value (in Euro) Key → deswegen falsch getrennt
    - gelöst durch delimiter: ' ‘
- fehlerhafte Markierung von Zeichenketten
    - gelöst durch  quotechar: " ' ”
- gemischte Datentypen bei Spalten vom Typ objects z.B. Value in Euros ist ein str und muss in float
- Missing Values in: nationality, height, weight, international reputation, positioning, goal keeper handling
    - gelöst durch einheitliches behandeln von missing Values als NaN‘
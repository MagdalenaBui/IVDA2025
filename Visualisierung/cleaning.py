import pandas as pd

# CSV einlesen
df = pd.read_csv('titanic.csv')

# Dezimaltrennzeichen in 'Fare' vereinheitlichen und in numerisch umwandeln
df['Fare'] = (
    df['Fare']
    .astype(str)
    .str.replace(',', '.', regex=False)        # Kommas durch Punkte ersetzen
)
df['Fare'] = pd.to_numeric(df['Fare'], errors='coerce')  # Fehlerhafte Einträge → NaN

# Einheitliches Markieren aller fehlenden Werte mit 'NA'
df = df.fillna('NA')

# Ticket-Strings bereinigen
df['Ticket'] = (
    df['Ticket']
    .str.replace(r'[\./]', '', regex=True)  # Punkte und Schrägstriche entfernen
    .str.replace(r'\s+', '', regex=True)    # Mehrfache Leerzeichen zusammenführen
)

# Name: Überflüssige Leerzeichen entfernen und Anführungszeichen die nicht benötigt werden, entfernen
df['Name'] = (
    df['Name']
    .astype(str)
    .str.replace('"', '', regex=False)      # alle existierenden " löschen
    .str.strip()                            # Leerraum am Rand entfernen
)

# Cabin-Spalte: Mehrfach-Kabinen in Tupel umwandeln (ohne 'NA')
df['Cabin_list'] = df['Cabin'].apply(lambda x: tuple(x.split()) if x != 'NA' else tuple())

# Duplikate entfernen
df.drop_duplicates(inplace=True) 

# Bereinigtes DataFrame speichern
df.to_csv('titanic_cleaned.csv', index=False)

# Erste Zeilen zur Kontrolle ausgeben
print(df.head())

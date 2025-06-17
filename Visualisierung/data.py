import pandas as pd
from pandas import DataFrame, read_csv


def load(path: str) -> DataFrame:
	return read_csv(path, quotechar='"')


def data_cleaning(filename, output_filename):
	# CSV einlesen
	df = pd.read_csv(filename)

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

	# Cabin-Spalte: Mehrfache Leerzeichen entfernen und durch Komma trennen und in String umwandeln
	df['Cabin'] = (
		df['Cabin']
		.str.strip()                            # Leerraum entfernen
		.str.replace(r'\s+', ',', regex=True)   # Mehrfache Leerzeichen durch Komma trennen
	)

	# Duplikate entfernen
	df.drop_duplicates(inplace=True)

	# Bereinigtes DataFrame speichern
	df.to_csv(output_filename, index=False)
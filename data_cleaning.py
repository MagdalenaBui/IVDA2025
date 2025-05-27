import numpy as np

def remove_dots_before_commas(filename='wein.csv', output_filename='wein_cleaned.csv'):
    # CSV-Datei einlesen
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # NumPy Array aus den Zeilen erstellen
    lines = np.array(content.strip().split('\n'))
    
    # Punkte vor Kommata entfernen
    clean_func = np.vectorize(lambda x: x.replace('.,', ','))
    cleaned_lines = clean_func(lines)
    
    # Duplikate entfernen mithilfe des dict.fromkeys() Ansatzes (dictionaries in Python enthalten keine Duplikate)
    cleaned_lines = np.array(list(dict.fromkeys(cleaned_lines)))

    # Bereinigte Daten in neue Datei schreiben
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write('\n'.join(cleaned_lines))
    
    print(f"Datei bereinigt und gespeichert als: {output_filename}")

# Ausführen
remove_dots_before_commas()
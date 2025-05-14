from pandas import DataFrame, read_csv
#Laden der CSV Datei
def load(path: str) -> DataFrame:
    return read_csv(
       path,
       sep=',',
       on_bad_lines='warn',
       na_values=['NA']
   )





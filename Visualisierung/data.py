from pandas import DataFrame, read_csv

#def load(path: str) -> DataFrame:
	#return read_csv(path, quotechar="'").drop_duplicates()


def load(path: str) -> DataFrame:
    return read_csv(
       path,
       sep=',',
       on_bad_lines='warn',
       na_values=['NA'],
       engine='python',
   )





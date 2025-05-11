from pandas import DataFrame, read_csv

def load(path: str) -> DataFrame:
	return read_csv(path, quotechar="'").drop_duplicates()
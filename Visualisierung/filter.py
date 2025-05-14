from enum import Enum
from functools import reduce # hilft Filter sequentiell anzuwenden
from typing import Callable, TypeAlias
from pandas import DataFrame, Series
from pandas.api.types import is_numeric_dtype

Filter: TypeAlias = Callable[[DataFrame], Series]

# logische UND-Verknüpfung um mehrere Filter für einen DataFrame dynamisch anzuwenden
def and_(dataframe: DataFrame, filters: list[Filter]):
	return dataframe[
		reduce(
			lambda expression, filter : expression & filter(dataframe), #Kombiniert den vorherigen Filterzustand mit dem Ergebnis des aktuellen Filters
			filters,
			series_true(dataframe)
		)
	]

#Filter der Vergleich von mehreren Werten mit einer Spalte für den Multi-Select-Dropdown ermöglicht
def multi_eq(column: str, values: object) -> Filter:
    def filter_function(dataframe: DataFrame) -> Series:
        # Fall 1: Keine Filterung, wenn values None ist oder eine leere Liste
        if values is None or (isinstance(values, list) and not values):
            return series_true(dataframe)

        # Fall 2: Liste mit mehrere Werte
        if isinstance(values, list):
            return dataframe[column].isin(values)

        # Fall 3: Einzelner Wert
        return dataframe[column] == values

    return filter_function



#Filter für numerische Werte im Dataframe, der es ermöglicht ein Minimum und Maximum einzustellen bei quantitativen Attributen
def number_range(column: str, min_value: float | None, max_value: float | None) -> Filter:

	def filter_function(dataframe: DataFrame) -> Series:
		if not is_numeric_dtype(dataframe[column]):
			return series_true(dataframe)

		result = series_true(dataframe)

		if min_value is not None:
			result = result & (dataframe[column] >= min_value)
		if max_value is not None:
			result = result & (dataframe[column] <= max_value)

		return result
	return filter_function


#Ausgangspunkt bzw. "Default Filter" für die Filteroperationen, bei denen jeder Index des Eingabe-DataFrames TRUE ist
def series_true(dataframe: DataFrame):
	return Series(True, index=dataframe.index)

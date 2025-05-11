from enum import Enum
from functools import reduce # um Filter sequentiell anzuwenden
from typing import Callable, Generic, NotRequired, Optional, TypeAlias, TypeVar, TypedDict, cast
from pandas import DataFrame, Series
from pandas.api.types import is_numeric_dtype

Filter: TypeAlias = Callable[[DataFrame], Series]

# logische UND-Verknüpfung um mehrere Filter für einen DataFrame anzuwenden
def and_(dataframe: DataFrame, filters: list[Filter]):
	return dataframe[
		reduce(
			lambda expression, filter : expression & filter(dataframe),
			filters,
			series_true(dataframe)
		)
	]
# mit den zwei Parametern column (Spalte im DataFrame) und value (beliebiges Objekt zum Vergleichen) wird eine Lambda Funktion erstellt, die als Filter funktioniert, indem wenn Value None ist für den Dataframe in allen Zeilen True zurückgegeben wird, und sonst verglichen wird ob die column im DataFrame gleich der value ist
def eq(column: str, value: object) -> Filter:
	return lambda dataframe : series_true(dataframe) if value is None else dataframe[column] == value


def number_range(column: str, min_value: float | None, max_value: float | None) -> Filter:

	def filter_function(dataframe: DataFrame) -> Series:
		if not is_numeric_dtype(dataframe[column]):
			return series_true(dataframe)

		result = series_true(dataframe)

		if min_value is not None:
			result = result & (dataframe[column] >= min_value)
		if max_value is not None:
			result = result & (dataframe[column] <= max_value)


#Ausgangspunkt bzw. "Default Filter" für meine Filteroperationen, bei denen jeder Index des Eingabe-DataFrames TRUE ist
def series_true(dataframe: DataFrame):
	return Series(True, index=dataframe.index)

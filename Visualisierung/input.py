from dash.html import Div, Label
from dash.dcc import Checklist, Dropdown, Input as DashInputElement, RadioItems
from dash.dependencies import Input
from pandas import DataFrame
from id import generate_id
from typing import TypeVar, TypedDict

T = TypeVar("T")

class InputElement(TypedDict):
	element: Div
	input: Input


def build_dropdown(name: str, options: list[T], default: T | None = None, multi: bool = False) -> InputElement:
	id = generate_id("dropdown")

	element = Div([
		Label(name, htmlFor=id),
		Dropdown(
			id=id,
			value=default,
				options=sorted(options, key=lambda value : str(value)), #Alphabetische Sortierung der Optionen
				multi=multi,
				style={
					"max-width": "300px",
					"margin-bottom": "10px"
				}
			)
		])

	input = Input(id, "value")

	return {
		"element": element,
		"input": input
	}

def build_number_input(name: str, value: int, min: int, max: int) -> InputElement:
	id = generate_id("input")

	element = Div(
		[
			Label(name, htmlFor=id),
			DashInputElement(
				id=id,
				type="number",
				value=value,
				min=min,
				max=max,
				style={
					"width": "292px",
					"margin-bottom": "10px"
				}
			)
		],
		style={
			"display": "flex",
			"flex-direction": "column" #vertikale anordnung der elemente
		}
	)

	input = Input(id, "value")

	return {
		"element": element,
		"input": input
	}

def build_radio_items(name: str, values: list[tuple[str, str]], default: str | None = None) -> InputElement:
	id = generate_id("radio-items")

	element = Div(
		[
			Label(name, htmlFor=id),
			RadioItems(
				id=id,
				options=[{ "label": pair[0], "value": pair[1] } for pair in values], #Durchlaufe jedes Tupel in values und erstelle für jedes Tupel ein Dictionary mit label als pair [0] und value als pair[1]
				value=default
			)
		]
	)

	input = Input(id, "value")

	return {
		"element": element,
		"input": input
	}

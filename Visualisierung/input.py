from dash.html import Div, Label
from dash.dcc import Dropdown, RadioItems, RangeSlider
from dash.dependencies import Input
from id import generate_id
from typing import TypeVar, TypedDict

#Platzhalter für verschiedene Typen
T = TypeVar("T")

class InputElement(TypedDict):
	element: Div
	input: Input

#Bau der Dropdown Komponente, die Multi-Select sein kann, für kategoriale Attribute
def build_dropdown(name: str, options: list[T], default: T | None = None, multi=False, clearable=False) -> InputElement:
	id = generate_id("dropdown")

	element = Div([
			Label(name, htmlFor=id),
			Dropdown(
				id=id,
				value=default,
				# Alphabetische Sortierung der Optionen
				options=sorted(options, key=lambda value : str(value)),
				multi=multi,
				clearable=clearable,
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

#Bau der Rangeslider Komponente für quantitative Attribute
def build_rangeslider(name: str, min: int, max: int) -> InputElement:
	id = generate_id("slider")

	element = Div([
		Label(name),
		RangeSlider(
			id=id,
			min=min,
			max=max,
			value=[min,max],
			allowCross=False,
			updatemode='drag',
			tooltip={"placement": "bottom", "always_visible": True}
		)
	])
	input = Input(id, "value")

	return {
		"element": element,
		"input": input
	}

#Bau der Radio-Item Komponente
def build_radio_items(name: str, values: list[tuple[str, str]], default: str | None = None) -> InputElement:
	id = generate_id("radio-items")

	element = Div(
		[
			Label(name, htmlFor=id),
			RadioItems(
				id=id,
				# Durchläuft jedes Tupel in values und erstellt für jedes Tupel ein Dictionary mit label als pair [0] und value als pair[1]
				options=[{ "label": pair[0], "value": pair[1] } for pair in values],
				value=default
			)
		])

	input = Input(id, "value")

	return {
		"element": element,
		"input": input
	}
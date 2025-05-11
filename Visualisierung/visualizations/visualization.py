from abc import ABC, abstractmethod
from typing import Sequence
from dash import Dash
from dash.development.base_component import Component
from pandas import DataFrame

class Visualization(ABC):

	@abstractmethod
	def html(self) -> Sequence[Component]:
		pass

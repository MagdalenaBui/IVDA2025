from abc import ABC, abstractmethod
from typing import Sequence
from dash.development.base_component import Component

#Initialisierung der abstrakten Klasse Visualization
class Visualization(ABC):

	@abstractmethod
	def html(self) -> Sequence[Component]:
		pass

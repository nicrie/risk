from typing import Self

from .constants import COUNTRIES

class Country():

    def __init__(self, name: str, continent: str, links : list[str]) -> None:
        self.name = name
        self._owner = None
        self._continent = continent
        self._links = links
        self._units = 0

    def set_units(self, units: int) -> None:
        if units >= 1:
            self._units = units
        else:
            raise ValueError('cannot set units to {:} in {:}; elegibile numbers are integeres > 1'.format(units, self.name))
    
    def get_units(self) -> int:
        return self._units

    def add_units(self, units: int) -> None:
        self._units += units
    
    def remove_units(self, units: int) -> None:
        if (self._units - units >= 1):
            self._units -= units
        else:
            raise ValueError('cannot remove units from {:}; at least 1 unit must remain'.format(self.name))
    
    def set_owner(self, name: str) -> None:
        self._owner = name

    def get_owner(self) -> str:
        return self._owner

    def has_border_with(self, country: Self) -> bool:
        return (country.name in self._links)
    
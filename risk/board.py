from sys import exit

import numpy as np
import pandas as pd

from typing import Self
from itertools import product

from .country import Country

from .player import Player
from .action import Action
from .constants import COUNTRIES, COLORS, LINKED_COUNTRIES_MATRIX

class Board():
    def __init__(self, names: list[str], colors: list[str] = None, n_start_units: int = 20) -> None:
        # Add countries to the board
        self.countries = [Country(name, cont, links) for name, cont, links in COUNTRIES]
        self.n_countries = len(COUNTRIES)

        # Counter of rounds
        self.round = 0
        self._has_winner = False

        # Add players to the board
        self.players = []
        self.n_players = 0        
        if colors is None:
            colors = COLORS
        for name, col in zip(names, colors):
            self._add_player(name, col)
            self.n_players += 1

        # Provide players with start untis 
        for player in self.players:
            player.add_available_units(n_start_units)
        
    def _add_player(self, name: str, color: str) -> None:
        self.players.append(Player(name, color))

    def has_winner(self) -> None:
        return self._has_winner

    def get_number_countries_per_player(self) -> list[int]:
        return [player.get_number_countries() for player in self.players]

    def update_win_condition(self):
        n_countries = self.get_number_countries_per_player()
        has_player_with_no_countries = any([number == 0 for number in n_countries])
        is_mid_game = self.get_round() > 0
        self._has_winner = (has_player_with_no_countries & is_mid_game)

    def get_player(self, name: str) -> Player:
            for player in self.players:
                if player.name == name:
                    return player

    def get_state(self) -> Self:
        return self

    def get_player_names(self) -> list[str]:
        return [player.name for player in self.players]

    def get_available_units_of_players(self) -> list[int]:
        return [player.get_number_available_units() for player in self.players]

    def has_available_units(self) -> bool:
        available_units = self.get_available_units_of_players()
        has_units = [units != 0 for units in available_units]
        return any(has_units)

    def get_round(self) -> int:
        return self.round

    def next_round(self) -> None:
        self.round += 1
    
    def get_attack_options(self, player: Player) -> pd.DataFrame:
        '''DataFrame showing attack options from source (columns) to target (row) countries.
        
        '''
        country_labels = [country.name for country in self.countries]

        # Whether two countries are linked with each other
        has_link = LINKED_COUNTRIES_MATRIX

        # Whether two countries have a "hostile" relationship (= county1 is owned by player; country2 is owned by enemy)
        has_hostile_relationship = has_link * np.nan

        is_own_country = [country.get_owner() == player.name for country in self.countries]
        is_hostile_country = [country.get_owner() != player.name for country in self.countries]

        is_own_country = pd.Series(is_own_country, index=country_labels)
        is_hostile_country = pd.Series(is_hostile_country, index=country_labels)

        for target_country, source_country in product(country_labels, country_labels):
            is_hostile = (is_own_country.loc[source_country]) & (is_hostile_country.loc[target_country])
            has_hostile_relationship.loc[target_country, source_country] = is_hostile

        # Country has >1 unit
        has_enough_units = [country.get_units() > 1 for country in self.countries]
        has_enough_units = np.array(has_enough_units)
        has_enough_units = pd.Series(has_enough_units, index=country_labels)

        is_possible_target = has_hostile_relationship * has_link * has_enough_units
        
        return is_possible_target

    def get_country(self, country_name: str) -> Country:
        for country in self.countries:
            if country.name == country_name:
                return country
        raise ValueError('{:} not found in countries'.format(country_name))

        

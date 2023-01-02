import numpy as np

from itertools import product


from ..action import Action
from .agent import Agent

class Nadine(Agent):
    '''Nadine the brain of Mitten im Leben plays overly aggressive.
    
    Although she will put her troops quite randomly, she will attack whenever/whereever she can!
    
    '''
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def act(self, state) -> Action:
        return super().act(state)

    def _move0(self, state: dict) -> Action:
        '''Select countries in a random way.
        
        '''
        neutral_countries = [country for country in state.countries if country.get_owner() is None]
        number_neutral_countries = len(neutral_countries)
        
        own_countries = [country for country in state.countries if country.get_owner() == self.name]

        if number_neutral_countries >=1:
            choose_from_countries = neutral_countries
        else:
            choose_from_countries = own_countries

        # Randomly select country
        rng = np.random.default_rng()
        country = rng.choice(choose_from_countries, 1, replace=False)[0]

        # Add action
        action = Action()
        action.add_country_to_be_selected(country)
        return action

    
    def _move1(self, state: dict) -> Action:
        action = Action()
        return action
    
    def _move2(self, state: dict) -> Action:
        '''Reinforces countries in a random way.
        
        '''
        action = Action()

        own_countries = [country for country in state.countries if country.get_owner() == self.name]
        n_available_units = state.get_player(self.name).get_number_available_units()

        # Randomly select countries
        rng = np.random.default_rng()
        while(n_available_units > 0):
            units = rng.choice(range(1, n_available_units + 1), 1)[0]
            country = rng.choice(own_countries, 1)[0]
            action.add_country_to_be_reinforced(country, units)
            n_available_units -= units

        action.next_move()
        return action
    
    def _move3(self, state: dict) -> Action:
        '''Attack as long as there are troops available.
        
        '''
        action = Action()

        attacker = state.get_player(self.name)
        possible_attack_options = state.get_attack_options(attacker)
        country_names = possible_attack_options.columns
        rng = np.random.default_rng()
        rows = rng.choice(country_names, len(country_names), replace=False)
        cols = rng.choice(country_names, len(country_names), replace=False)
        is_option = False
        for row, col in product(rows, cols):
            is_option = possible_attack_options.loc[row, col]
            # Only if valid attack is possible
            if is_option:
                source_name = col
                target_name = row
                source_country = state.get_country(source_name)
                target_country = state.get_country(target_name)
                defender = state.get_player(target_country.get_owner())

                # Take random number of units
                units = source_country.get_units() - 1
                units = rng.integers(1, units, size=1, endpoint=True)[0]
                # Add action
                action.add_country_to_be_attacked(defender, source_country, target_country, units)

        action.next_move()
        return action
    
    def _move4(self, state: dict) -> Action:
        action = Action()
        action.next_move()
        return action
    
    def _move5(self, state: dict) -> Action:
        action = Action()
        return action


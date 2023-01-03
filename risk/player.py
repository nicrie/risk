import numpy as np
import pandas as pd

from typing import Self

from .action import Action
from .country import Country
from .constants import MOVES

class Player():
    def __init__(self, name: str, color: str) -> None:
        self.name = name
        self.color = color
        
        self._current_move = 0  # Moves= 0 ... 7
        self._available_units = 0
        self._cards = []
        self._countries = {}
    
    def act(self, action: Action) -> None:
        current_move = self.get_current_move()

        # 0. Select countries (only at the beginning)
        if current_move == 0:
            country = action.get_country_to_be_selected()
            if country is not None:
                print('{:} adds 1 unit to {:} ({:} units left)'.format(self.name, country.name, self.get_number_available_units()))
                self._assign_country(country)
                self._add_units_to_country(country, 1)
            
            if(self.get_number_available_units() == 0):
                self.next_move()

                    
        # 1. Activate reinforcement cards
        elif current_move == 1:
            print('\n' + '-'*80 + '\nMake your turn, {:}!\n'.format(self.name) + '-'*80)
            self.get_reinforcements()

            card_set = action.get_card_to_be_activated()
            if card_set is not None:
                self.activate_cards(card_set)
            
            self.next_move()
        
        # 2. Reinforce countries
        elif current_move == 2:
            reinforce_country = action.get_country_to_be_reinforced()
            if reinforce_country is not None:
                self.reinforce_country(*reinforce_country)
            if action.is_done():
                self.next_move()
        
        # 3. Attack countries
        elif current_move == 3:
            attack_operation = action.get_country_to_be_attacked()
            if attack_operation is not None:
                self.attack_country(*attack_operation)
            if action.is_done():
                self.next_move()

        # 4. Relocate troops
        elif current_move == 4:
            reloction_operation = action.get_units_to_be_relocated()
            if reloction_operation is not None:
                self.relocate_units(*reloction_operation)
            if action.is_done():
                self.next_move()
        
        # 5. Draw reinforcement card
        elif current_move == 5:
            draw_card = action.get_state_extra_card()
            if draw_card:
                self.draw_card()
            self.next_move()

        else:
            raise ValueError('{:} is not a valid move counter'.format(current_move))
            
    def get_reinforcements(self) -> None:
        n_countries = len(self._countries)
        min_units = 3
        reinforcements = max(n_countries // 3, min_units)
        self.add_available_units(reinforcements)
        total_reinforcements = self.get_number_available_units()
        print('{:} gets {:} reinforcement troops.'.format(self.name, reinforcements))

    def activate_cards(self, card_set) -> None:
        raise NotImplementedError('cannot play cards yet')
        print('{:} activates reinforcement cards and gains additional {:} troops.'.format(self.name, units))
        self.add_available_units(units)
    
    def reinforce_country(self, country: Country, units: int) -> None:
        print('{:} reinforces {:} with {:} unit(s).'.format(self.name, country.name, units))
        self._add_units_to_country(country, units)

    def attack_country(self, target_player: Self, source_country: Country, target_country: Country, units: int) -> None:
        # Check whether the players own the countries or not
        if not self.owns_country(source_country):
            raise RuntimeError('attack not possible; attacker {:} does not own {:}'.format(self.name, source_country))
        if not target_player.owns_country(target_country):
            raise RuntimeError('attack not possible; defender {:} does not own {:}'.format(target_player.name, target_country))        
        
        # Check whether the countries border each other or not
        if not source_country.has_border_with(target_country):
            raise RuntimeError('attack not possible; {:} has no border with {:}'.format(source_country.name, target_country.name))

        # Additional checks
        if(target_country.get_owner() == self.name):
            raise RuntimeError('are you really trying to attack yourself? Oo')
        if(source_country.get_units() <= units):
            raise RuntimeError('attack with {:} units not possible; only {:} units left in {:}'.format(units, source_country.get_units(), source_country.name))

        # Get number of attackers/defenders
        n_attackers = units
        n_defenders = target_country.get_units()

        # Print info
        attack_msg = '{:} ({:}) attacks {:} ({:})'
        unit_msg = 'Attacker: {:} troops -- Defender: {:} troops.\n'
        attack_msg = attack_msg.format(source_country.name, source_country.get_owner(), target_country.name, target_country.get_owner())
        unit_msg = unit_msg.format(n_attackers, n_defenders)
        print(attack_msg)
        print(unit_msg)

        # Fight!
        n_attackers, n_defenders = self._evaluate_attack(n_attackers, n_defenders)

        # Update number of units in source and target countries
        source_country.remove_units(units)

        # Evaluate battle
        # Attacker won
        if n_defenders == 0:
            target_player._remove_country(target_country)
            self._assign_country(target_country)
            target_country.set_units(n_attackers)
        # Defender won
        elif n_attackers == 0:
            target_country.set_units(n_defenders)
        # Invalid result
        else:
            ValueError('Whoupsi...that shouldn\'t have happened :\'( ')

    def relocate_units(self, source_country: Country, target_country: Country, units: int) -> None:
        print('{:} relocates {:} from {:} to {:}'.format(self.player, units, source_country, target_country))
        if not source_country.has_border_with(target_country):
            raise ValueError('troops cannot be relocated; {:} has no border with {:}'.format(source_country, target_country))
        if not self.owns_country(target_country):
            raise ValueError('troops cannot be relocated; player {:} does not own {:}'.format(self.name, target_country))
        
        self._remove_units_from_country(units)   

    def draw_card(self):
        raise NotImplementedError('cannot draw cards yet')
        print('{:} draws a reinforcement card.'.format(self.player))

    def get_number_units(self) -> int:
        n_units = [country.get_units() for country in self._countries.values()]
        return int(np.sum(n_units))
   
    def get_number_countries(self) -> int:
        return len(self._countries)
 
    def get_number_available_units(self) -> int:
            return self._available_units

    def get_cards(self) -> list[str]:
        return self._cards

    def get_current_move(self) -> str:
        return self._current_move
    
    def next_move(self) -> None:
        '''Go to next move; if at END_OF_TURN go back to first move

        '''
        if self._current_move == 6:
            self._current_move = 1
        else:
            self._current_move += 1

    def show_stats(self) -> None:
        n_available_units = self.get_number_available_units()
        n_tot_countries = self.get_number_countries()
        n_tot_units = self.get_number_units()
        cards = self.get_cards()
        countries = {name: country.get_units() for name, country in self._countries.items()}
        print('{:}'.format(self.name))
        print('-'*80)
        print('Total number of countries: {:}'.format(n_tot_countries))
        print('Total number of units: {:}'.format(n_tot_units))
        # print('Number of available units: {:}'.format(n_available_units))
        print('Reinforcement cards:')
        print(cards)
        print('Individual countries:')
        print(countries)
        print('-'*80)

    def owns_country(self, country: Country) -> bool:
        return country.name in list(self._countries.keys())

    def _evaluate_attack(self, n_attackers, n_defenders) -> None:
        while((n_attackers > 0) & (n_defenders > 0)):
            n_attackers_lost, n_defenders_lost = self._throw_dice(n_attackers, n_defenders)
            n_attackers -= n_attackers_lost
            n_defenders -= n_defenders_lost
            print('The attacker lost {:} and the defender lost {:} units'.format(n_attackers_lost, n_defenders_lost))
        return n_attackers, n_defenders

    def _throw_dice(self, n_attackers, n_defenders) -> None:
        rng = np.random.default_rng()

        n_dice_attackers = min(3, n_attackers)
        n_dice_defenders = min(2, n_defenders)

        dice_attackers = rng.integers(1, 6, endpoint=True, size=n_dice_attackers)
        dice_defenders = rng.integers(1, 6, endpoint=True, size=n_dice_defenders)

        dice_attackers = np.sort(dice_attackers)[::-1]
        dice_defenders = np.sort(dice_defenders)[::-1]

        n_attackers_lost = 0
        n_defenders_lost = 0
        for attack, defence in zip(dice_attackers, dice_defenders):
            if attack > defence:
                n_defenders_lost += 1
            else:
                n_attackers_lost += 1
        return n_attackers_lost, n_defenders_lost

    def _assign_country(self, country: Country) -> None:
        country.set_owner(self.name)
        self._countries[country.name] = country
    
    def _remove_country(self, country: Country) -> Country:
        country.set_owner(None)
        return self._countries.pop(country.name)

    def add_available_units(self, units) -> None:
        self._available_units += units

    def remove_available_units(self, units) -> None:
        if self._available_units - units < 0:
            raise ValueError('insufficient number of available units')
        else:
            self._available_units -= units
    
    def _add_units_to_country(self, country: Country, n_units: int) -> None:
        self.remove_available_units(n_units)
        try:
            self._countries[country.name].add_units(n_units)
        except KeyError:
            raise KeyError('cannot add units to {:} as it does not belong to player {:}'.format(country.name, self.name))

    def _remove_units_from_country(self, country: Country, units: int) -> None:
        try:
            self.countries[country.name].remove_units(units)
        except KeyError:
            raise ValueError('troops cannot be removed from country; player {:} does not own {:}'.format(self.name, country))
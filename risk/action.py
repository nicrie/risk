# NOTE: To avoid circular import between Action, Country and Player, we use forward references as suggested here:
# https://stackoverflow.com/a/33844891/3050730

class Action():
    def __init__(self) -> None:
        self._select_country = None  # <Country>
        self._activate_cards = None  # tuple (<country_name1>, <country_name2>, <country_name3>)
        self._reinforce_country = None  # tuples (<country>, <units>)
        self._attack_country = None  # tuples (<player_defender>, <country_attacker>, <country_defender>, <units>)
        self._relocate_units = None # tuples (<from_country>, <to_country>, <units>)
        self._draw_card = False
        self._done = False  # Whether or not to go to the next move after the action is performed 

    def next_move(self) -> None:
        self._done = True
    
    def is_done(self) -> bool:
        return self._done

    def add_country_to_be_selected(self, country: 'Country') -> None:
        self._select_country = country

    def add_card_to_be_activated(self, card_set: str) -> None:
        self._activate_cards = card_set

    def add_country_to_be_reinforced(self, country: 'Country', units: int) -> None:
        self._reinforce_country = (country, units)

    def add_country_to_be_attacked(self, defender: 'Player', source_country: 'Country', target_country: 'Country', units: int) -> None:
        self._attack_country = (defender, source_country, target_country, units)
    
    def add_units_to_be_relocated(self, source_country: 'Country', target_country: 'Country', units: int) -> None:
        self._relocate_units = (source_country, target_country, units)
    
    def set_state_extra_card(self, draw: bool) -> None:
        self._draw_card = draw    
    
    def get_country_to_be_selected(self) -> 'Country':
        return self._select_country

    def get_card_to_be_activated(self) -> tuple:
        return self._activate_cards

    def get_country_to_be_reinforced(self) ->  tuple:
        return self._reinforce_country

    def get_country_to_be_attacked(self) -> tuple:
        return self._attack_country
    
    def get_units_to_be_relocated(self) -> tuple:
        return self._relocate_units
    
    def get_state_extra_card(self) -> bool:
        return self._draw_card 
import numpy as np
import pandas as pd

COLORS = ['red', 'blue', 'green']

CONTINENTS = ['South America', 'North America', 'Europe', 'Africa', 'Asia', 'Oceania']

COUNTRIES = [
    # COUNTRY NAME -- CONTINENT NAME -- LINKS TO OTHER COUNTRIES
    ('Central America', CONTINENTS[1], ['Venezuela']),
    ('Venezuela', CONTINENTS[0], ['Central America', 'Peru', 'Brazil']),
    ('Peru', CONTINENTS[0], ['Venezuela', 'Brazil', 'Argentina']),
    ('Brazil', CONTINENTS[0], ['Venezuela', 'Peru', 'Argentina', 'North Africa']),
    ('Argentina', CONTINENTS[0], ['Peru', 'Brazil']),
    ('North Africa', CONTINENTS[3], ['Brazil']),
]

# Boolean matrix of links between countries
country_labels = [country for country, _, _ in COUNTRIES]
n_countries = len(country_labels)
LINKED_COUNTRIES_MATRIX = np.zeros((n_countries, n_countries), dtype=bool)
LINKED_COUNTRIES_MATRIX = pd.DataFrame(LINKED_COUNTRIES_MATRIX, columns=country_labels, index=country_labels)
for country, continent, linked_countries in COUNTRIES:
    for country2 in linked_countries:
        LINKED_COUNTRIES_MATRIX.loc[country, country2] = True

# Available agents that can be chosen as BOTs
AVAILABLE_AGENTS = ['Fettbert']

# Available player moves
MOVES = [
    0,  # '0_preselect_countries',  # only before first round
    1,  # '1_get_reinforcements',
    2,  # '2_activate_reinforcement_cards',
    3,  # '3_reinforce_countries'
    4,  # '4_attack_countries'
    5,  # '5_relocate_troops'
    6,  # '6_draw_reinforcement_card'
    7,  # '7_END_OF_TURN'
]
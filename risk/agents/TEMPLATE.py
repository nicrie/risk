import numpy as np

from itertools import product


from ..action import Action
from .agent import Agent

class TemplateAgent(Agent):
    '''Template class to be copied and modified
    
    May the best BOT win!
    
    '''
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def act(self, state) -> Action:
        return super().act(state)

    def _move0(self, state: dict) -> Action:
        '''DEFINE HOW TO CHOOSE COUNTRIES AT THE BEGINNING
        
        '''
        pass
    
    def _move1(self, state: dict) -> Action:
        '''DEFINE WHEN/HOW TO ACTIVATE REINFORCEMENT CARDS
        
        NOTE: reinforcement cards are not yet implemented
        '''
        action = Action()
        return action
    
    def _move2(self, state: dict) -> Action:
        '''DEFINE HOW TO REINFORCE THE COUNTRIES
        
        '''
        pass
    
    def _move3(self, state: dict) -> Action:
        '''DEFINE HOW TO ATTACK COUNTRIES
        
        '''
        pass
    
    def _move4(self, state: dict) -> Action:
        '''DEFINE HOW TO RELOCATE YOUR UNITS
        
        Current implementation only allows to move units only from one country to a neighboring country.
        However, you can make indefinitely many moves.
        '''
        action = Action()
        return action
    
    def _move5(self, state: dict) -> Action:
        '''Just copy the following lines, do not change them

        NOTE: reinforcement cards are  not implemented yet
        
        NOTE: Current implementation still requires these lines of code, but they are actually not necessary.
        Remove them in the future
        '''
        action = Action()
        return action

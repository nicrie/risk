from abc import ABC, abstractmethod

from ..action import Action

class Agent(ABC):  
    '''Abstract class defining Agent structure.
    
    '''
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def act(self, state: dict) -> Action:
        current_move = state.get_player(self.name).get_current_move()

        # 0. Select countries (only at the beginning)
        if current_move == 0:
            action = self._move0(state)
        # 1. Activate reinforcement cards for additional reinforcements
        elif current_move == 1:
            action = self._move1(state)
        # 2. Reinforce countries
        elif current_move == 2:
            action = self._move2(state)
        # 3. Attack countries
        elif current_move == 3:
            action = self._move3(state)
        # 4. Relocate troops
        elif current_move == 4:
            action = self._move4(state)
        # 5. Draw reinforcement card
        elif current_move == 5:
            action = self._move5(state)
        else:
            raise ValueError('{:} is not a valid move counter'.format(current_move))
        return action

  
    @abstractmethod
    def _move0(self, state: dict) -> Action:
        '''
        0. SELECT COUNTRIES (ONLY AT THE BEGINNING)
        
        TO BE IMPLEMENTED
        '''
        pass


    @abstractmethod
    def _move1(self, state: dict) -> Action:
        '''
        1. ACTIVATE REINFORCEMENT CARDS
        
        TO BE IMPLEMENTED
        '''
        pass

    @abstractmethod
    def _move2(self, state: dict) -> Action:
        '''
        2. REINFORCE COUNTRIES
        
        TO BE IMPLEMENTED
        '''
        pass

    @abstractmethod
    def _move3(self, state: dict) -> Action:
        '''
        3. ATTACK COUNTRIES
        
        TO BE IMPLEMENTED
        '''
        pass
    
    @abstractmethod
    def _move4(self, state: dict) -> Action:
        '''
        4. RELOCATE TROOPS
        
        TO BE IMPLEMENTED
        '''
        pass
    
    @abstractmethod
    def _move5(self, state: dict) -> Action:
        '''
        5. DRAW REINFORCEMENT CARD
        
        TO BE IMPLEMENTED
        '''
        pass

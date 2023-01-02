import time

from .board import Board
from .player import Player
from .agents.utils import get_agent

class Risk():
    def __init__(
            self,
            names: list[str],
            agents: list[str],
            colors: list[str] = None,
            n_start_units: int = 20,
            sleep: int = 0
    ) -> None:
        '''Create board enviroment and agents.
        
        '''
        self._waiting_time = sleep

        print('~'*80 + '\n' + '~'*80 + '\n')
        print(' '*30 + 'WELCOME TO RISK!')
        print('\n' + '~'*80 + '\n' + '~'*80 + '\n')
        time.sleep(self._waiting_time)

        self.board = Board(names, colors, n_start_units=n_start_units)
        self.agents = [get_agent(agent, name) for name, agent in zip(names, agents)]

        print('PLAYERS:')
        [print('{:} ({:})'.format(name, agent)) for name, agent in zip(names, agents)]
        time.sleep(self._waiting_time)

    def distribute_starting_countries(self) -> None:
        print('\n\n' + '='*80)
        print('Selection of starting countries & troops')
        print('='*80 + '\n')
        time.sleep(self._waiting_time)

        has_available_units = self.board.has_available_units()
        while(has_available_units):
            for agent in self.agents:
                current_state = self.board.get_state()
                action = agent.act(state=current_state)
                self.board.get_player(agent.name).act(action)
                time.sleep(self._waiting_time)
                
            # Update number of available untis   
            has_available_units = self.board.has_available_units()
        

    def play_round(self) -> None:
        self.board.next_round()
        print('\n' + '='*80)
        print('Start ROUND {:}!'.format(self.board.get_round()))
        print('='*80 + '\n' + '\n')

        for agent in self.agents:
            MAX_MOVE = 6
            current_move = self.board.get_player(agent.name).get_current_move()
            while(current_move < MAX_MOVE):
                # Get current state of board
                current_state = self.board.get_state()
                # Pass state to agent
                action = agent.act(state=current_state)
                # Perform action
                self.board.get_player(agent.name).act(action)
                # Update condition to win
                self.board.update_win_condition()
                if self.board.has_winner():
                    print('OMG well done! GAME OVER!! <3 <3 <3 <3')
                    exit(-1)
                # Update move
                current_move = self.board.get_player(agent.name).get_current_move()
                time.sleep(self._waiting_time)
            self.board.get_player(agent.name).next_move()
        
        print('-'*80 + '\nROUND {:} SUMMARY'.format(self.board.get_round()) + '\n' + '-'*80)
        self.show_stats()
    
    def show_stats(self) -> None:
        for player in self.board.players:
            player.show_stats()
            time.sleep(self._waiting_time)
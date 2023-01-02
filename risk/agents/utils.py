from .fettbert import Fettbert
from .nadine import Nadine

def get_agent(agent_name, player_name):
    '''Get agent instance when provided with agent name
    
    '''
    if agent_name == 'Fettbert':
        agent = Fettbert(player_name)
    
    elif agent_name == 'Nadine':
        agent = Nadine(player_name)
    
    # elif agent_name == '<INSERT NEW AGENT>'
    #     agent = <INSERT NEW AGENT>

    else:
        raise ValueError('agent {:} does not exist'.format(agent_name))
    
    return agent
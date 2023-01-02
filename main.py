from risk import Risk

if __name__ == "__main__":

    risk = Risk(
        names=['Marco', 'Max', 'Hansi'],
        agents=['Fettbert', 'Nadine', 'Fettbert'],
        n_start_units=5,
        sleep=.1,  # waiting time between player moves (in seconds)
    )

    risk.distribute_starting_countries()
    risk.show_stats()
    
    while(not risk.board.has_winner()):
        risk.play_round()




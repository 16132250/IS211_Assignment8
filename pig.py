import random
import argparse
import time

parser = argparse.ArgumentParser()
# parser.add_argument("--numPlayer", type=int, default=2)
parser.add_argument("--player1", type=str, default="human")
parser.add_argument("--player2", type=str, default="computer")
parser.add_argument("--timed", action="store_true")
args = parser.parse_args()

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turn_score = 0

def dice_roll(Player):
    roll = random.randint(1,6)
    # print(f"{Player.name} rolled a {roll}")
    return roll

class HumanPlayer(Player):
    def play_or_stay(self):
        choice = input(f"  Enter 'r' to roll or 'h' to hold: ")

        while choice not in ['r', 'h']:
            print("    !! Invalid input. Please enter 'r' to roll or 'h' to hold.")
            choice = input(f"  Enter 'r' to roll or 'h' to hold: ")
        return choice

class ComputerPlayer(Player):
    def play_or_stay(self):
        x = self.score
        hold_threshold = min(25, 100 - x)
        if self.turn_score >= hold_threshold:
            time.sleep(1)
            return 'h'
        else:
            time.sleep(1)
            return 'r'

class PlayerFactory:
    def get_player(self, name):
        if name.lower() == "human":
            return HumanPlayer(name)
        elif name.lower() == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type")

class TimedGameProxy(PlayerFactory):
    def __init__(self):
        self.start_time = time.time()
        self.factory = PlayerFactory()

    def get_player(self, name):
        if time.time() - self.start_time > 60:
            print("Game over: time limit exceeded")
            exit()
        return self.factory.get_player(name)

if __name__ == "__main__":
    random.seed(0)
    if args.timed:
        player_factory = TimedGameProxy()
    else:
        player_factory = PlayerFactory()
    players = [player_factory.get_player(args.player1),
               player_factory.get_player(args.player2)]
    winning_score = 100
    winner = False
    start_time = time.time()
    elapsed_time = 0


    while not winner:
        elapsed_time = time.time() - start_time
        for player in players:
            print(f"{player.name}'s turn")
            player.turn_score = 0
            while True and elapsed_time < 60:
                choice = player.play_or_stay()
                if choice == 'h':
                    elapsed_time = time.time() - start_time
                    # print(f'if h {elapsed_time}')
                    player.score += player.turn_score
                    if player.score >= winning_score:
                        winner = True
                        print(f"{player.name} is the winner!")
                    break
                elapsed_time = time.time() - start_time
                # print(elapsed_time)
                roll = dice_roll(player)
                if roll == 1:
                    elapsed_time = time.time() - start_time
                    # print(elapsed_time)
                    print(f"    {player.name} rolled a 1 and now they\'re done")
                    player.turn_score = 0
                    break
                else:
                    elapsed_time = time.time() - start_time
                    # print(elapsed_time)
                    player.turn_score += roll
                    # player.score += roll
                    print(f"    You rolled {roll}. {player.name} score: [{player.score}] "
                          f"Turn score: [{player.turn_score}]")
                    if player.score + player.turn_score >= winning_score:
                        winner = True
                        print(f"{player.name} is the winner!")
                        break
            if winner:
                break

        if elapsed_time >= 60:
            print("Time is up! The game is over.")
            for player in players:
                print(f"{player.name}: {player.score}")
            break
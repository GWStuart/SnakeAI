from argparse import ArgumentParser, RawDescriptionHelpFormatter
from gameLogic import Game
# from bot1 import Bot1
from bot2 import Bot2
import random
import time

parser = ArgumentParser(prog="render", description="Used to test snake bots", formatter_class=RawDescriptionHelpFormatter)

# Get command line arguments
parser.add_argument("-o", "--output", help="The file to save the output to")
args = parser.parse_args()

if args.output:
    save_file = args.output
else:
    save_file = "game_output"

XCELLS, YCELLS = 80, 60
# XCELLS, YCELLS = 16, 12
PRINT_FREQUENCY = 5  # after how many apples should a log message be printed

seed = random.randint(0, 2**32 - 1)
random.seed(seed)

game = Game(XCELLS, YCELLS)
bot = Bot2(XCELLS, YCELLS)

moves = []  # keep track of all the moves made

print("\nStarting Simulation")

start_time = time.time()
while not game.isGameOver():
    move = bot.makeMove(game.getSnakeBody(), game.getApplePosition())

    moves.append(move)

    new_apple = game.moveSnake(move)

    if new_apple:
        if game.getScore() % PRINT_FREQUENCY == 0:
            print(f"Score: {game.getScore()}")

print("Simulation Finished\n")
print(f"Final score was: {game.getScore()}")
run_time = time.time() - start_time
print(f"Time to execute was {run_time} seconds")

# Save the data to a file
print("\nWriting results to save file")
with open(f"saves/{save_file}.snake", "w") as f:
    f.write(f"{XCELLS} {YCELLS} {seed} {len(moves)}\n")
    f.write("".join(moves))

print(f"Results stored at saves/{save_file}.snake\n")


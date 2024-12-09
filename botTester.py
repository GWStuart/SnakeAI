from gameLogic import Game
from bot1 import Bot1
import random
import time

save_file = "game3"

XCELLS, YCELLS = 80, 60
PRINT_FREQUENCY = 10  # after how many apples should a log message be printed

seed = random.randint(0, 2**32 - 1)
random.seed(seed)

game = Game(XCELLS, YCELLS)
bot = Bot1(XCELLS, YCELLS, game)

moves = []  # keep track of all the moves made

print("\nStarting Simulation")

start_time = time.time()
while not game.isGameOver():
    move = bot.makeMove()

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


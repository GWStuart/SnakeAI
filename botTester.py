from argparse import ArgumentParser, RawDescriptionHelpFormatter
from gameLogic import Game
import fileUtils
import bot1.bot1, bot2.bot2
import random
import time
import os

parser = ArgumentParser(prog="render", description="Used to test snake bots", formatter_class=RawDescriptionHelpFormatter)

# Get command line arguments
parser.add_argument("bot", help="The bot to test")
parser.add_argument("-o", "--output", help="The file to save the output to")
parser.add_argument("-x", "--xcells", help="Number of horiztonal cells in the grid")
parser.add_argument("-y", "--ycells", help="Number of vertical cells in the grid")
parser.add_argument("-s", "--size", help="Grid size. Accepts (S)mall, (M)edium or (L)arge")
args = parser.parse_args()

# Results are saved at ./saves/{save_file}
if not os.path.exists("./saves"):
    os.mkdir("./saves")

save_file = args.output if args.output else "game_output"
save_file = fileUtils.getNewFile(save_file, "snake")  # ensure new filename

if args.size:
    size = args.size.lower()
    if size == "s" or size == "small":
        XCELLS, YCELLS = 16, 12
    elif size == "m" or size == "medium":
        XCELLS, YCELLS = 64, 48
    elif size == "l" or size == "large":
        XCELLS, YCELLS = 96, 72
    else:
        print("Unrecognised size. Can be (S)mall, (M)edium, or (L)arge")
else:
    XCELLS, YCELLS = 64, 48  # default board dimensions

if args.xcells:
    XCELLS = int(args.xcells)
if args.ycells:
    YCELLS = int(args.ycells)

PRINT_FREQUENCY = 5  # after how many apples should a log message be printed

seed = random.randint(0, 2**32 - 1)
random.seed(seed)

game = Game(XCELLS, YCELLS)

match args.bot:
    case "bot1":
        bot = bot1.bot1.Bot1(XCELLS, YCELLS)
    case "bot2":
        bot = bot2.bot2.Bot2(XCELLS, YCELLS)
    case _:
        print("Unrecognised Bot")
        quit()

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
fileUtils.saveGame(save_file, XCELLS, YCELLS, seed, len(moves), moves)

print(f"Results stored at {save_file}\n")


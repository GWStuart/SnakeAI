"""
Program used to test the bots.
Specify the bot to be tested as a command line argument
"""
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from gameLogic.snake import Snake
from timeUtil import Timer
import fileUtils
import random
import os

# Import the bots to be tested
from bot1.bot1 import Bot1
from bot2.bot2 import Bot2

# Create an argument parser to detect command line arguments
parser = ArgumentParser(prog="render", description="Used to test snake bots", formatter_class=RawDescriptionHelpFormatter)

# Get command line arguments
parser.add_argument("bot", help="The bot to test")
parser.add_argument("-o", "--output", help="The file to save the output to")
parser.add_argument("-x", "--xcells", help="Number of horiztonal cells in the grid")
parser.add_argument("-y", "--ycells", help="Number of vertical cells in the grid")
parser.add_argument("-s", "--size", help="Grid size. Accepts (S)mall, (M)edium or (L)arge")
args = parser.parse_args()


# determine the location where the game data will be saved
save_file = fileUtils.getNewFile(args.output, "snake")  # ensure new filename

# determine the board size
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

# check if a custom size was specified
if args.xcells:
    XCELLS = int(args.xcells)
if args.ycells:
    YCELLS = int(args.ycells)


# define some constants
PRINT_FREQUENCY = 5  # After how many apples should a log message be printed
SEED = random.randint(0, 2**32 - 1)  # The random seed of the game
random.seed(SEED)
SNAKE_SPAWN = (2, 2)

# Initiate the snake
snake = Snake((XCELLS, YCELLS), SNAKE_SPAWN)

# Determine which bot is to be used
match args.bot:
    case "bot1":
        bot = Bot1(XCELLS, YCELLS)
    case "bot2":
        bot = Bot2(XCELLS, YCELLS)
    case _:
        print("Unrecognised Bot")
        quit()


# start the bot simultion
print("\nStarting Simulation")

timer = Timer()
timer.start()

moves = []  # keep track of all the moves made
while not snake.isGameOver():
    # invoke the makeMove() method to find the best move for the bot
    move = bot.makeMove(snake.getBody(), snake.getApplePosition())

    # record the move
    direction_string = bot.encodeDirection(move)
    moves.append(direction_string)

    # make the move
    snake.change_direction(move)
    new_apple = snake.move()

    # detect if an apple was eaten
    if new_apple:
        if snake.getScore() % PRINT_FREQUENCY == 0:
            print(f"Score: {snake.getScore()}")

print("Simulation Finished\n")
timer.stop()

print(f"Final score was: {snake.getScore()}")
print(f"Time to execute was {timer.get_elapsed_time()}")

# Save the data to a file
print("\nWriting results to save file")
fileUtils.saveGame(save_file, XCELLS, YCELLS, SEED, len(moves), moves)

print(f"Results stored at {save_file}\n")


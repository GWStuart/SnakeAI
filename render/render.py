"""
Used to render a snake game.
Converts .snake --> .mp4

Several command line options are available.
See  summary with: render -h
"""
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from sys import argv
from timeUtil import Timer
from gameLogic.snake import Snake
from gameLogic.util import decodeDirection
from render.renderLD import RenderLD
from render.renderMD import RenderMD
from render.renderHD import RenderHD
from fileUtils import getDefaultOutputFileName, getNewFile
import cv2
import random

description = """
This script is used to generate a video output file of a saved snake game
"""

parser = ArgumentParser(prog="render", description=description, formatter_class=RawDescriptionHelpFormatter)

# Get command line arguments
parser.add_argument("file", help="File path to the file to render")
parser.add_argument("-q", "--quality", default="medium", help="The quality to render output. Can be high, medium or low")
parser.add_argument("-FPS", "--fps", default="30", help="The FPS at which to render the video. Overwrites that set by the quality")
parser.add_argument("-s", "--scale", help="The scale of the video. Lower scale renders faster but is lower quality")
parser.add_argument("-nb", "--noborder", action="store_true", help="Whether to render the border or not")
parser.add_argument("-o", "--output", help="The output file without extension. Defaults to same name as the file to render")

# parse the command line arguments
args = parser.parse_args()

# Define some constants
SNAKE_SPAWN = (2, 2)
PRINT_FREQUENCY = 10  # percent inverval when an update should be printed
QUALITY = args.quality.lower() if args.quality else "medium"  # default to medium
FPS = int(args.fps)
BORDER = not args.noborder
FILE = args.file
CELL_SIZE = int(args.scale) if args.scale else None

# Try to load the file
file_name = f"{args.file}.snake" if "." not in FILE else FILE
try:
    data_file = open(file_name)
except FileNotFoundError:
    print(f"Could not find file: {file_name}")
    print("Aborting")
    quit()

# Generate the ouput file name
output_file = args.output if args.output else getDefaultOutputFileName(FILE)
output_file = getNewFile(output_file, "mp4")

# Load init data from the data file
XCELLS, YCELLS, SEED, NUM_MOVES = map(int, data_file.readline().split())
random.seed(SEED)
PRINT_INTERVAL = round(NUM_MOVES / PRINT_FREQUENCY)
snake = Snake((XCELLS, YCELLS), SNAKE_SPAWN)

# select the relevant render engine
match QUALITY:
    case "low" | "l":
        render_engine = RenderLD(output_file, snake, CELL_SIZE=CELL_SIZE, FPS=FPS, BORDER=BORDER)
    case "medium" | "m":
        render_engine = RenderMD(output_file, snake, CELL_SIZE=CELL_SIZE, FPS=FPS, BORDER=BORDER)
    case "high" | "h":
        render_engine = RenderHD(output_file, snake, CELL_SIZE=CELL_SIZE, FPS=FPS, BORDER=BORDER)
    case "_":
        print("Unrecognised quality")
        quit()

# begin the rendering process
print("\nRendering in Progress")
timer = Timer()
timer.start()

i = 0
while (move := data_file.read(1)):
    # check if log message is to be printed
    if (i % PRINT_INTERVAL == 0):
        percentage = round(i / NUM_MOVES * 100, 1)
        print(f"{percentage}% complete")

    # make the move
    move = decodeDirection(move)
    snake.change_direction(move)
    snake.move()

    # render the frame
    render_engine.render()

    i += 1

# finish the render and close the data file
render_engine.finish()
data_file.close()
timer.stop()

# Output results
print(f"\nRendering finished successfully")
print("Time to render: " + timer.get_elapsed_time() + "\n")

print(f"Saved video as {output_file}")
seconds = 1 / FPS * NUM_MOVES
print("Video duration: " + Timer.convert_time(seconds) + "\n")


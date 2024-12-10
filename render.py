from argparse import ArgumentParser, RawDescriptionHelpFormatter
from sys import argv
from gameLogic import Game
import numpy as np
import cv2
import random

description = """
This script is used to generate a video output file of a saved snake game
"""

parser = ArgumentParser(prog="render", description=description, formatter_class=RawDescriptionHelpFormatter)

# Get command line arguments
parser.add_argument("file", help="The file to render without file extension. Must be in /saves/")
parser.add_argument("-q", "--quality", default="medium", help="The quality to render output. Can be high, medium or low")
parser.add_argument("-FPS", "--fps", default="30", help="The FPS at which to render the video. Overwrites that set by the quality")
parser.add_argument("-s", "--scale", help="The scale of the video. Lower scale renders faster but is lower quality")
parser.add_argument("-nb", "--noborder", action="store_true", help="Whether to render the border or not")
parser.add_argument("-o", "--output", help="The output file without extension. Defaults to same name as the file to render")

args = parser.parse_args()

# Store command line argument outputs
file = args.file
quality = args.quality
FPS = int(args.fps)
border = not args.noborder
if args.output:
    output_file = f"saves/{args.output}.mp4"
else:
    output_file = f"saves/{file}.mp4"

if args.scale: 
    CELL_SIZE = int(args.scale)
else:
    match quality.lower():
        case "low":
            CELL_SIZE = 4
        case "medium":
            CELL_SIZE = 8
        case "high":
            CELL_SIZE = 16

# Process the data
file = open(f"saves/{file}.snake")

XCELLS, YCELLS, seed, num_moves = map(int, file.readline().split())
LENGTH, HEIGHT = XCELLS * CELL_SIZE + 2, YCELLS * CELL_SIZE + 2
random.seed(seed)

PRINT_FREQUENCY = 10  # at which percent interval to print an update
spacing = round(num_moves / PRINT_FREQUENCY)

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

match quality.lower():
    case "low":
        video = cv2.VideoWriter(f"./{output_file}", fourcc, float(FPS), (LENGTH, HEIGHT), 0)
    case "medium":
        video = cv2.VideoWriter(f"./{output_file}", fourcc, float(FPS), (LENGTH, HEIGHT))
    case "high":
        video = cv2.VideoWriter(f"./{output_file}", fourcc, float(FPS), (LENGTH, HEIGHT))

game = Game(XCELLS, YCELLS)

def renderTile(frame, x: int, y: int, colour: tuple[int, int, int]) -> None:
    cv2.rectangle(frame, (1 + x*CELL_SIZE, 1 + y*CELL_SIZE), (1 + (x+1)*CELL_SIZE, 1 + (y+1)*CELL_SIZE), colour, -1)

def renderLD() -> None:
    frame = np.zeros((HEIGHT, LENGTH), dtype=np.uint8)

    body = game.getSnakeBody()
    for part in body:
        renderTile(frame, *part, 255)

    apple = game.getApplePosition()
    renderTile(frame, *apple, 100)

    # add a white border
    if border:
        frame[:, 0] = np.array(255)
        frame[:, LENGTH - 1] = np.array(255)
        frame[0, :] = np.array(255)
        frame[HEIGHT - 1, :] = np.array(255)

    video.write(frame)

def renderMD() -> None:
    frame = np.zeros((HEIGHT, LENGTH, 3), dtype=np.uint8)

    body = game.getSnakeBody()
    for i in range(len(body) - 1):
        part = body[i]
        renderTile(frame, *part, (0, 255, 0))

    head = body[-1]
    renderTile(frame, *head, (0, 200, 0))

    apple = game.getApplePosition()
    renderTile(frame, *apple, (0, 0, 255))

    cv2.putText(frame, f"score: {game.getScore()}", (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv2.LINE_AA)

    # add a white border
    if border:
        frame[:, 0] = np.array(255)
        frame[:, LENGTH - 1] = np.array(255)
        frame[0, :] = np.array(255)
        frame[HEIGHT - 1, :] = np.array(255)

    video.write(frame)


def renderHD() -> None:
    frame = np.zeros((HEIGHT, LENGTH, 3), dtype=np.uint8)

    body = game.getSnakeBody()
    for i in range(len(body) - 1):
        part = body[i]
        renderTile(frame, *part, (0, 255, 0))

    head = body[-1]
    renderTile(frame, *head, (0, 200, 0))

    apple = game.getApplePosition()
    renderTile(frame, *apple, (0, 0, 255))

    cv2.putText(frame, f"score: {game.getScore()}", (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv2.LINE_AA)

    # add a white border
    if border:
        frame[:, 0] = np.array(255)
        frame[:, LENGTH - 1] = np.array(255)
        frame[0, :] = np.array(255)
        frame[HEIGHT - 1, :] = np.array(255)

    video.write(frame)


match quality.lower():
    case "low":
        render_func = renderLD
    case "medium":
        render_func = renderMD
    case "high":
        render_func = renderHD


print("\nRendering in Progress")

i = 0
while (move := file.read(1)):
    if (i % spacing == 0):
        percentage = round(i / num_moves * 100, 1)
        print(f"{percentage}% complete")

    game.moveSnake(move)

    if game.isGameOver():
        run = False

    render_func()
    i += 1

video.release()
file.close()

print("Rendering finished successfully\n")

print(f"Saved video as {output_file}")
seconds = 1 / FPS * num_moves
if seconds < 60:
    print(f"Duration of {seconds} seconds")
else:
    print(f"Durection of {int(seconds // 60)} min and {round(seconds % 60, 1)} seconds\n")


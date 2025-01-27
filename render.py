from argparse import ArgumentParser, RawDescriptionHelpFormatter
from sys import argv
from gameLogic import Game
import time
import numpy as np
import cv2
import random
import math
import os

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

if not os.path.exists("./saves"):
    os.mkdir("./saves")

output_file = args.output if args.output else file
output_file = getNewFile(output_file, "mp4")

# Process the data
file = open(f"saves/{file}.snake")

XCELLS, YCELLS, seed, num_moves = map(int, file.readline().split())

if args.scale: 
    CELL_SIZE = int(args.scale)
else:
    match quality.lower():
        case "low":
            CELL_SIZE = round(360 / XCELLS)  # 260 x pixels
        case "medium":
            CELL_SIZE = round(768 / XCELLS)  # 768 x pixels
        case "high":
            CELL_SIZE = round(1280 / XCELLS)  # 1280 x pixels

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
    # for i in range(len(body) - 1):
    #     renderTile(frame, *body[i], (0, 255, 0))

    # head = body[-1]
    # renderTile(frame, *head, (0, 200, 0))

    get_center = lambda part: (round((part[0] + 0.5) * CELL_SIZE), round((part[1] + 0.5) * CELL_SIZE))
    for i in range(len(body) - 1):
        cv2.line(frame, get_center(body[i]), get_center(body[i+1]), (0, 200, 0), math.ceil(0.75 * CELL_SIZE))

    apple = game.getApplePosition()
    # renderTile(frame, *apple, (0, 0, 255))
    cv2.circle(frame, get_center(apple), math.ceil(0.37 * CELL_SIZE), (0, 0, 255), -1)

    cv2.putText(frame, f"score: {game.getScore()}", (20, 20), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 1, cv2.LINE_AA)

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
start_time = time.time()

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

print(f"Rendering finished successfully")
print("Time to render: " + time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time)) + "\n")

print(f"Saved video as {output_file}")
seconds = 1 / FPS * num_moves
print("Video duration: " + time.strftime("%H:%M:%S", time.gmtime(seconds)) + "\n")


from gameLogic import Game
import numpy as np
import cv2
import random

file = input("What file would you like to render: ")
file = open(f"saves/{file}.snake")

CELL_SIZE = 10
XCELLS, YCELLS, seed = map(int, file.readline().split())
LENGTH, HEIGHT = XCELLS * CELL_SIZE, YCELLS * CELL_SIZE
random.seed(seed)

FPS = 10 

fourcc = cv2.VideoWriter_fourcc(*'MP42')
video = cv2.VideoWriter('./output.avi', fourcc, float(FPS), (LENGTH, HEIGHT))

game = Game(XCELLS, YCELLS)


def render() -> None:
    frame = np.zeros((HEIGHT, LENGTH, 3), dtype=np.uint8)

    for part in game.getSnakeBody():
        cv2.rectangle(frame, (part[0]*CELL_SIZE, part[1]*CELL_SIZE), (part[0]*CELL_SIZE+CELL_SIZE, part[1]*CELL_SIZE+CELL_SIZE), (0, 255, 0), -1)

    apple = game.getApplePosition()
    cv2.rectangle(frame, (apple[0]*CELL_SIZE, apple[1]*CELL_SIZE), (apple[0]*CELL_SIZE+CELL_SIZE, apple[1]*CELL_SIZE+CELL_SIZE), (0, 0, 255), -1)


    video.write(frame)


while (move := file.read(1)):
    game.sendKey(move)

    if not game.update():
        run = False

    render()

video.release()
file.close()

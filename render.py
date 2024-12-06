from gameLogic import Game
import numpy as np
import cv2

import random

LENGTH = 1280
HEIGHT = 720
FPS = 10 

fourcc = cv2.VideoWriter_fourcc(*'MP42')
video = cv2.VideoWriter('./output.avi', fourcc, float(FPS), (LENGTH, HEIGHT))


game = Game(LENGTH, HEIGHT)

moves = "rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrdddddddddddddddddddddddlllllllllllllllllllllddddddddddddddrrrrrrrrr"

for move in moves:
    frame = np.zeros((HEIGHT, LENGTH, 3), dtype=np.uint8)

    # x, y = random.randint(0, width), random.randint(0, height)
    # cv2.rectangle(frame, (x, y), (x+10, y+10), (0, 255, 0))

    game.sendKey(move)

    pos = game.getSnakeBody()[0]
    cv2.rectangle(frame, pos, (pos[0]+10, pos[1]+10), (0, 255, 0), -1)

    video.write(frame)

video.release()

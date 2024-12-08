from gameLogic import Game
import numpy as np
import cv2
import random

file = input("What file would you like to render: ")
file = open(f"saves/{file}.snake")

CELL_SIZE = 10
XCELLS, YCELLS, seed, num_moves = map(int, file.readline().split())
LENGTH, HEIGHT = XCELLS * CELL_SIZE, YCELLS * CELL_SIZE
random.seed(seed)

FPS = 30 
PRINT_FREQUENCY = 10  # at which percent interval to print an update
spacing = round(num_moves / PRINT_FREQUENCY)

fourcc = cv2.VideoWriter_fourcc(*'MP42')
video = cv2.VideoWriter('./output.avi', fourcc, float(FPS), (LENGTH, HEIGHT))

game = Game(XCELLS, YCELLS)


def render() -> None:
    frame = np.zeros((HEIGHT, LENGTH, 3), dtype=np.uint8)

    body = game.getSnakeBody()
    for i in range(len(body) - 1):
        part = body[i]
        cv2.rectangle(frame, (part[0]*CELL_SIZE, part[1]*CELL_SIZE), (part[0]*CELL_SIZE+CELL_SIZE, part[1]*CELL_SIZE+CELL_SIZE), (0, 255, 0), -1)

    head = body[-1]
    cv2.rectangle(frame, (head[0]*CELL_SIZE, head[1]*CELL_SIZE), (head[0]*CELL_SIZE+CELL_SIZE, head[1]*CELL_SIZE+CELL_SIZE), (0, 200, 0), -1)

    apple = game.getApplePosition()
    cv2.rectangle(frame, (apple[0]*CELL_SIZE, apple[1]*CELL_SIZE), (apple[0]*CELL_SIZE+CELL_SIZE, apple[1]*CELL_SIZE+CELL_SIZE), (0, 0, 255), -1)

    cv2.putText(frame, f"score: {game.getScore()}", (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv2.LINE_AA)

    # add a white border
    frame[:, 0] = np.array([255, 255, 255])
    frame[:, LENGTH - 1] = np.array([255, 255, 255])
    frame[0, :] = np.array([255, 255, 255])
    frame[HEIGHT - 1, :] = np.array([255, 255, 255])

    video.write(frame)

print("\nRendering in Progress")

i = 0
while (move := file.read(1)):
    if (i % spacing == 0):
        percentage = round(i / num_moves * 100, 1)
        print(f"{percentage}% complete")
    game.sendKey(move)

    if game.isGameOver():
        run = False

    render()

    i += 1


video.release()
file.close()

print("Rendering finished successfully\n")

print(f"Saved video as {'output'}.avi")
seconds = 1 / FPS * num_moves
if seconds < 60:
    print(f"Duration of {seconds} seconds")
else:
    print(f"Durection of {int(seconds // 60)} min and {round(seconds % 60, 1)} seconds")


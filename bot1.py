from gameLogic import Game
import random
import math

save_file = "game2"

seed = random.randint(0, 999999)
random.seed(seed)

XCELLS, YCELLS = 80, 60
game = Game(XCELLS, YCELLS)

directions = "lrud"

moves = []


def move_direction(x: int, y: int, direction: str):
    match direction:
        case "l":
            return (x - 1, y)
        case "r":
            return (x + 1, y)
        case "u":
            return (x, y - 1)
        case "d":
            return (x, y + 1)

while not game.isGameOver():
    apple = game.getApplePosition()

    min_direction = (directions[0], math.inf)
    for direction in directions:
        new_position = move_direction(*game.getSnakeHead(), direction)

        if new_position in game.getSnakeBody():
            continue

        dist = math.dist(apple, new_position)
        if dist < min_direction[1]:
            min_direction = (direction, dist)
        
    moves.append(min_direction[0])
    game.sendKeyFast(min_direction[0])
    game.update()


# Save the data to a file
with open(f"saves/{save_file}.snake", "w") as f:
    f.write(f"{XCELLS} {YCELLS} {seed}\n")
    f.write("".join(moves))


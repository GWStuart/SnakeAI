"""
Project demonstrating the functionality of the game as specified in the gameLogic file.
Graphics implemented using pygame.

Controls:
    use WASD or arrow keys to control the snake
"""
from gameLogic.snake import Snake
import pygame
pygame.init()

# define window dimensions, cell size and snake spawn
# these can be changed.
LENGTH, HEIGHT = 800, 600
CELL_SIZE = 20
SNAKE_SPAWN = (2, 2)

# initialise a pygame window
win = pygame.display.set_mode((LENGTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# initialise the snake
XCELLS, YCELLS = LENGTH // CELL_SIZE, HEIGHT // CELL_SIZE
snake = Snake((XCELLS, YCELLS), SNAKE_SPAWN)


"""
Renders the window based on the state of the snake
"""
def render() -> None:
    # fill the background
    win.fill((30, 30, 30))

    # draw the snake body
    for part in snake.getBody():
        pygame.draw.rect(win, (0, 255, 0), (part[0] * CELL_SIZE, part[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # draw the apple
    apple = snake.getApplePosition()
    pygame.draw.rect(win, (255, 0, 0), (apple[0] * CELL_SIZE, apple[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))


run = True
while run:
    # check for window close events of the 'q' key to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False

    # check for key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        snake.change_direction((1, 0))
    elif keys[pygame.K_a]:
        snake.change_direction((-1, 0))
    elif keys[pygame.K_w]:
        snake.change_direction((0, -1))
    elif keys[pygame.K_s]:
        snake.change_direction((0, 1))

    snake.move()

    if snake.isGameOver():
        print("GAME OVER")
        run = False

    render()

    pygame.display.update()
    clock.tick(10)


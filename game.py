"""
Project demonstrating the functionality of the game as specified in the gameLogic package.
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

# the number of times the snake should be updated per second
# i.e. number of moves per second
UPDATE_FREQUENCY = 10
FPS = 60
UPDATE_FRAME = FPS / UPDATE_FREQUENCY

# add functionality to buffer key inputs
key_buffer = []
MAX_BUFFER_SIZE = 2

# rendering options
BG_COLOUR = (30, 30, 30)
SNAKE_COLOUR = (0, 255, 0)
SNAKE_WIDTH = 14  # must be <= CELL_SIZE
APPLE_COLOUR = (255, 0, 0)

"""
Renders the window based on the state of the snake
"""
def render() -> None:
    # fill the background
    win.fill(BG_COLOUR)

    # draw the snake body
    for part in snake.getBody():
        pygame.draw.rect(win, SNAKE_COLOUR, (part[0] * CELL_SIZE, part[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # draw the apple
    apple = snake.getApplePosition()
    pygame.draw.rect(win, APPLE_COLOUR, (apple[0] * CELL_SIZE, apple[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # update the display
    pygame.display.update()


"""
Updates the snake and renders the new game
@returns True if the game is over and False otherwise
"""
def update_game():
    # check if a direction change is in the buffer
    if len(key_buffer) > 0:
        direction = key_buffer.pop(0)
        snake.change_direction(direction)

    # move the snake
    snake.move()

    # check if the snake has moved into a game over position
    if snake.isGameOver():
        return True

    # render the result
    render()


frame_count = 0
run = True
while run:
    for event in pygame.event.get():
        # check for window close events
        if event.type == pygame.QUIT:
            run = False

        # check for 'q' presses to close the window
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False

            # detect game key presses
            if len(key_buffer) < MAX_BUFFER_SIZE:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    key_buffer.append((1, 0))
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    key_buffer.append((-1, 0))
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    key_buffer.append((0, -1))
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    key_buffer.append((0, 1))

    # if sufficient time has passed then update the snake
    if frame_count == UPDATE_FRAME:
        if update_game():
            run = False

        # reset the frame counter
        frame_count = 0

    frame_count += 1
    clock.tick(FPS)


from gameLogic import Game
import pygame
pygame.init()

LENGTH, HEIGHT = 800, 600
CELL_SIZE = 20
XCELLS, YCELLS = LENGTH / CELL_SIZE, HEIGHT / CELL_SIZE

win = pygame.display.set_mode((LENGTH, HEIGHT))
pygame.display.set_caption("Snake Game")

game = Game(XCELLS, YCELLS)
snake_direction = "r"  # default snake direction
clock = pygame.time.Clock()

def render(game: Game) -> None:
    win.fill((0, 0, 0))

    for part in game.getSnakeBody():
        pygame.draw.rect(win, (0, 255, 0), (part[0] * CELL_SIZE, part[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    apple = game.getApplePosition()
    pygame.draw.rect(win, (255, 0, 0), (apple[0] * CELL_SIZE, apple[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        snake_direction = (1, 0)
    elif keys[pygame.K_a]:
        snake_direction = (-1, 0) 
    elif keys[pygame.K_w]:
        snake_direction = (0, -1)
    elif keys[pygame.K_s]:
        snake_direction = (0, 1) 

    game.moveSnake(snake_direction)

    if game.isGameOver():
        print("GAME OVER")
        run = False

    render(game)

    pygame.display.update()
    clock.tick(10)


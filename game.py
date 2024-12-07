from gameLogic import Game
import pygame
pygame.init()

LENGTH, HEIGHT = 800, 600
CELL_SIZE = 10
XCELLS, YCELLS = LENGTH / CELL_SIZE, HEIGHT / CELL_SIZE

win = pygame.display.set_mode((LENGTH, HEIGHT))
pygame.display.set_caption("Snake Game")

snake_direction = "r"  # the starting snake direction

game = Game(XCELLS, YCELLS)
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
        game.sendKey("r")
        snake_direction = "r"
    elif keys[pygame.K_a]:
        game.sendKey("l")
        snake_direction = "l"
    elif keys[pygame.K_w]:
        game.sendKey("u")
        snake_direction = "u"
    elif keys[pygame.K_s]:
        game.sendKey("d")
        snake_direction = "d"
    else:
        game.sendKey(snake_direction)

    if not game.update():
        print("GAME OVER")
        run = False

    render(game)

    pygame.display.update()
    clock.tick(10)


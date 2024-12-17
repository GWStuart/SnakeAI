import pygame
import timeit
from bot2 import Bot2
pygame.init()

LENGTH, WIDTH = 800, 600
win = pygame.display.set_mode((LENGTH, WIDTH))
pygame.display.set_caption("Bot Simulator")

CELL_SIZE = 50
XCELLS, YCELLS = LENGTH // CELL_SIZE, WIDTH // CELL_SIZE

clock = pygame.time.Clock()

snake_sim = []  # holds the simulated snake
obstacles = []
apple = None

highlights = []

timeout = {"obstacles": False, "highlights": False}  # used to determine if a block type is active

bot = Bot2(XCELLS, YCELLS)


def render():
    win.fill((0, 0, 0))

    for tile in highlights:
        colour = (200, 30, 150)
        pygame.draw.rect(win, colour, (tile[0]*CELL_SIZE, tile[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for tile in obstacles:
        colour1 = (0, 220, 0)
        colour2 = (0, 0, 0)  # (61, 61, 61)
        pygame.draw.rect(win, colour1, (tile[0]*CELL_SIZE, tile[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.line(win, colour2, (tile[0]*CELL_SIZE, tile[1]*CELL_SIZE), ((tile[0]+1)*CELL_SIZE, (tile[1]+1)*CELL_SIZE))
        pygame.draw.line(win, colour2, (tile[0]*CELL_SIZE, (tile[1]+1)*CELL_SIZE), ((tile[0]+1)*CELL_SIZE, tile[1]*CELL_SIZE))

    for tile in snake_sim:
        pygame.draw.rect(win, (0, 220, 0), (tile[0]*CELL_SIZE, tile[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    if len(snake_sim) > 1:
        pygame.draw.lines(win, (255, 255, 255), False, list(map(lambda x: ((x[0]+0.5)*CELL_SIZE, (x[1]+0.5)*CELL_SIZE), snake_sim)), 1)
    
    if apple:
        pygame.draw.rect(win, (255, 0, 0), (apple[0]*CELL_SIZE, apple[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.update()

"""
Pretty Efficient flood fill algorithm
In future some further optimisations could be perform using set caching and potentially preallocated boolean arrays
"""
def floodfill(x, y) -> set[tuple[int, int]]:
    snake_set = set(obstacles)
    
    if (x, y) in snake_set:
        return set()

    filled = set()

    stack = [(x, y)]
    while stack:
        x, y = stack.pop()
        
        if (x, y) in filled:
            continue

        filled.add((x, y))

        if x > 0 and (x - 1, y) not in snake_set and (x - 1, y) not in filled:
            stack.append((x - 1, y))
        if x < XCELLS - 1 and (x + 1, y) not in snake_set and (x + 1, y) not in filled:
            stack.append((x + 1, y))
        if y > 0 and (x, y - 1) not in snake_set and (x, y - 1) not in filled:
            stack.append((x, y - 1))
        if y < YCELLS - 1 and (x, y + 1) not in snake_set and (x, y + 1) not in filled:
            stack.append((x, y + 1))

    return filled


def get_mouse_cell() -> tuple[int, int]:
    mouse = pygame.mouse.get_pos()
    return mouse[0] // CELL_SIZE, mouse[1] // CELL_SIZE

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            timeout = {"obstacles": False, "highlights": False}  # used to determine if a block type is active
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # exits the simulation
                run = False
            if event.key == pygame.K_1:  # peforms a floodfill and highlights the cells that were reached
                if highlights:
                    highlights = []
                else:
                    highlights = list(floodfill(*get_mouse_cell()))
            if event.key == pygame.K_c:  # clear the screen
                snake_sim = []
                obstacles = []
                apple = None
                highlights = []
            if event.key == pygame.K_ESCAPE:  # only clear snake sim and highlights
                if snake_sim:
                    snake_sim = [snake_sim[0]]  # preserve snake head
                highlights = []
            if event.key == pygame.K_a:  # adds an apple
                mouse = get_mouse_cell()
                if mouse == apple:
                    apple = None
                else:
                    apple = mouse
            if event.key == pygame.K_s:  # spawn the snake
                snake_sim = [get_mouse_cell()]
            if event.key == pygame.K_u:  # undo last move
                if len(snake_sim) > 1:
                    snake_sim.pop()
            if event.key == pygame.K_SPACE:  # move the snake
                if snake_sim:
                    if not apple:
                        apple = (0, 0)
                    move = bot.makeMove(obstacles + snake_sim, apple)
                    snake_sim.append(bot.moveDirection(snake_sim, move))

    pressed = pygame.mouse.get_pressed(3)
    if pressed[0]:  # add obstacles with left click
        tile = get_mouse_cell()
        if not timeout["obstacles"] or timeout["obstacles"] != tile:
            timeout["obstacles"] = tile
            if tile in obstacles:
                obstacles.remove(tile)
            else:
                obstacles.append(tile)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_h] or pressed[1]:  # add highlights with h key or right click
        tile = get_mouse_cell()
        if not timeout["highlights"] or timeout["highlights"] != tile:
            timeout["highlights"] = tile
            if tile in highlights:
                highlights.remove(tile)
            else:
                highlights.append(tile)

    render()
    clock.tick(60)


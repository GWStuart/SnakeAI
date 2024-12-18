from gameLogic import Game
import math

class Bot:
    directions = "lrud"  # left, right, up and down
    direction_dict = {(1, 0): "r", (-1, 0): "l", (0, -1): "u", (0, 1): "d"}

    def __init__(self, XCELLS: int, YCELLS: int):
        self.XCELLS = XCELLS
        self.YCELLS = YCELLS

        self.flood_cells = dict() 

    """
    Make a snake move based on the provided information
    @param snake the snake's body with the head as the last element
    @param apple the cell position of the apple
    @returns a string representing the move as a snake direction
    """
    def makeMove(self, snake: list[tuple[int, int]], apple: tuple[int, int]) -> str:
        pass

    """
    Used to get the direction associated with a given direct move
    @returns the direction string representing the given move
    """
    def getMoveDirection(self, snake: list[tuple[int, int]], newHead: tuple[int, int]):
        head = snake[-1]
        change = (newHead[0] - head[0], newHead[1] - head[1])
        return Bot.direction_dict[change]

    """
    Returns all valid cells that the snake could get to
    Autoamtically filters out moves that result in a game over
    @returns four moves corresponding to the 4 directions are returned
    """
    def getMoves(self, snake: list[tuple[int, int]]) -> list[tuple[int, int]]:
        result = []
        for direction in Bot.directions:
            newHead = self.moveDirection(snake, direction)
            if self.isValidMove(snake, newHead):
                result.append(newHead)
        return result

    """
    The head position if the snake is moved in the given direction
    @returns the new head position the snake would be if it moved in the given direction
    @requires that the given direction is valid
    """
    def moveDirection(self, snake: list[tuple[int, int]], direction: str) -> tuple[int, int]:
        head = snake[-1]
        match direction:
            case "l":
                return (head[0] - 1, head[1])
            case "r":
                return (head[0] + 1, head[1])
            case "u":
                return (head[0], head[1] - 1)
            case "d":
                return (head[0], head[1] + 1)

    """
    Determine if moving to the given cell results in a valid move.
    A valid move is defined as one where the snake is still alive
    @requires that the provided cells in snake are all already valid
    @returns True if the move is valid and False otherwise
    """
    def isValidMove(self, snake: list[tuple[int, int]], newHead: tuple[int, int]):
        if newHead in snake:
            return False
        return 0 <= newHead[0] < self.XCELLS and 0 <= newHead[1] < self.YCELLS

    """
    A fast search to quickly determine if there may be a path connecting two points
    @returns True if there is definitly a path connecting the two points. False if inconclusive
    @requires that the (startx, starty) and (endx, endy) are valid tiles
    """
    def fast_search(self, snake_set, startx, starty, endx, endy) -> bool:
        x, y = startx, starty
        stack = {((x, y), None)}
        checked = set()
    
        for i in range(5):  # can tweak this number
            result = min(stack, key=lambda x: x[1])
            stack.remove(result)
            x, y = result[0][0], result[0][1]
            checked.add((x, y))
    
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                newx, newy = x + dx, y + dy
                if (newx, newy) not in snake_set and (newx, newy) not in checked and (newx, newy) not in stack:
                    if newx == endx and newy == endy:
                        return True
                    stack.add(((newx, newy), math.dist((newx, newy), (endx, endy))))

            if not stack:
                return False

        return False

    """
    Pretty Efficient flood fill algorithm
    In future some further optimisations could be perform using set caching and potentially preallocated boolean arrays
    @param the x and y position to peform the floodfill
    @param additions: extra cells to include as the snake body 
    @requires that the x, y position is empty
    @returns the number of cells reached by the floodfill
    """
    def BACKUP(self, x, y, snake: list[tuple[int, int]]) -> int:
        snake_set = set(snake)

        if self.flood_cells:
            endx, endy = list(self.flood_cells.keys())[0]
            if self.fast_search(snake_set, x, y, endx, endy): 
                return self.flood_cells[(endx, endy)]

        startx, starty = x, y

        filled = set()
        stack = {(x, y)}

        while stack:
            x, y = stack.pop()
            filled.add((x, y))
    
            if x > 0 and (x - 1, y) not in snake_set and (x - 1, y) not in filled:
                stack.add((x - 1, y))
            if x < self.XCELLS - 1 and (x + 1, y) not in snake_set and (x + 1, y) not in filled:
                stack.add((x + 1, y))
            if y > 0 and (x, y - 1) not in snake_set and (x, y - 1) not in filled:
                stack.add((x, y - 1))
            if y < self.YCELLS - 1 and (x, y + 1) not in snake_set and (x, y + 1) not in filled:
                stack.add((x, y + 1))
    
        result = len(filled)
        self.flood_cells[(startx, starty)] = result
        return result

    def floodfill(self, x, y, snake: list[tuple[int, int]]) -> int:
        snake_set = set(snake)

        if self.flood_cells:
            endx, endy = list(self.flood_cells.keys())[0]
            if self.fast_search(snake_set, x, y, endx, endy): 
                return self.flood_cells[(endx, endy)]

        startx, starty = x, y
        
        filled = set()
        continue_search = True

        i = 0
    
        stack = {(x, y)}
        while stack:
            x, y = stack.pop()
    
            filled.add((x, y))
    
            if x > 0 and (x - 1, y) not in snake_set and (x - 1, y) not in filled:
                if continue_search and (x - 1, y) in self.flood_cells:
                    result = self.flood_cells[(x - 1, y)]
                    self.flood_cells[(startx, starty)] = result
                    return result
                stack.add((x - 1, y))
            if x < self.XCELLS - 1 and (x + 1, y) not in snake_set and (x + 1, y) not in filled:
                if continue_search and (x + 1, y) in self.flood_cells:
                    result = self.flood_cells[(x + 1, y)]
                    self.flood_cells[(startx, starty)] = result
                    return result
                stack.add((x + 1, y))
            if y > 0 and (x, y - 1) not in snake_set and (x, y - 1) not in filled:
                if continue_search and (x, y - 1) in self.flood_cells:
                    result = self.flood_cells[(x, y - 1)]
                    self.flood_cells[(startx, starty)] = result
                    return result
                stack.add((x, y - 1))
            if y < self.YCELLS - 1 and (x, y + 1) not in snake_set and (x, y + 1) not in filled:
                if continue_search and (x, y + 1) in self.flood_cells:
                    result = self.flood_cells[(x, y + 1)]
                    self.flood_cells[(startx, starty)] = result
                    return result
                stack.add((x, y + 1))

            if continue_search:
                i += 1
                if i > 2:  # can tweak this number 200
                    continue_search = False
    
        result = len(filled)
        self.flood_cells[(startx, starty)] = result
        return result

    """
    Multi floodfill
    """
    def trapped_squares(self, snake: list[tuple[int, int]], cells: list[tuple[int, int]]) -> list[int]:
        snake_set = set(snake)
        result = [None] * len(cells)
        available_squares = self.XCELLS * self.YCELLS - len(snake_set)

        for i, cell in enumerate(cells):
            if result[i]:
                continue

            indexes = [i]
            filled = set()

            stack = {cell}
            REMOVE_LATER = False
            while stack:
                x, y = stack.pop()

                if REMOVE_LATER and (x, y) in cells:
                    indexes.append(cells.index((x, y)))

                filled.add((x, y))
        
                if x > 0 and (x - 1, y) not in snake_set and (x - 1, y) not in filled:
                    stack.add((x - 1, y))
                if x < self.XCELLS - 1 and (x + 1, y) not in snake_set and (x + 1, y) not in filled:
                    stack.add((x + 1, y))
                if y > 0 and (x, y - 1) not in snake_set and (x, y - 1) not in filled:
                    stack.add((x, y - 1))
                if y < self.YCELLS - 1 and (x, y + 1) not in snake_set and (x, y + 1) not in filled:
                    stack.add((x, y + 1))

                REMOVE_LATER = True
        
            for a in indexes:
                result[a] = available_squares - len(filled)
       
        return result

    """
    Tidys up a few things that should be done after ending a move
    """
    def endMove(self):
        self.flood_cells = dict()


import math

class Bot:
    DIRECTIONS = "lrud"  # left, right, up and down
    DIRECTION_DICT = {(1, 0): "r", (-1, 0): "l", (0, -1): "u", (0, 1): "d"}

    def __init__(self, XCELLS: int, YCELLS: int):
        self.XCELLS = XCELLS
        self.YCELLS = YCELLS

    """
    Make a snake move based on the provided information.
    This method holds the main decision making of the bot.
    @param snake the snake's body with the head as the last element
    @param apple the cell position of the apple
    @returns a string representing the move as a snake direction
    """
    def makeMove(self, snake: list[tuple[int, int]], apple: tuple[int, int]) -> str:
        # this method is implemented by the subclasses
        pass

    """
    Used to get the direction associated with a given direct move
    @returns the direction tuple representing the given move
    """
    def getMoveDirection(self, snake: list[tuple[int, int]], newHead: tuple[int, int]) -> tuple[int, int]:
        head = snake[-1]
        change = (newHead[0] - head[0], newHead[1] - head[1])
        return change

    """
    Returns a direction encoded as its string representation
    """
    def encodeDirection(self, direction) -> str:
        return self.DIRECTION_DICT[direction]

    """
    Returns all valid cells that the snake could get to
    Autoamtically filters out moves that result in a game over
    @returns four moves corresponding to the 4 directions are returned
    """
    def getMoves(self, snake: list[tuple[int, int]]) -> list[tuple[int, int]]:
        result = []
        for direction in Bot.DIRECTIONS:
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


from gameLogic import Game

class Bot:
    directions = "lrud"  # left, right, up and down
    direction_dict = {(1, 0): "r", (-1, 0): "l", (0, -1): "u", (0, 1): "d"}

    def __init__(self, XCELLS: int, YCELLS: int, game: Game):
        self.XCELLS = XCELLS
        self.YCELLS = YCELLS
        self.game = game

    """
    Make a move based on the given game
    @returns the move as a snake direction
    """
    def makeMove(self) -> str:
        pass

    """
    Used to get the direction associated with a given direct move
    @returns the direction string representing the given move
    """
    def getMoveDirection(self, newHead: tuple[int, int]):
        head = self.game.getSnakeHead()
        change = (newHead[0] - head[0], newHead[1] - head[1])
        return Bot.direction_dict[change]

    """
    Returns all valid cells that the snake could get to
    Autoamtically filters out moves that result in a game over
    @returns four moves corresponding to the 4 directions are returned
    """
    def getMoves(self) -> list[tuple[int, int]]:
        result = []
        for direction in Bot.directions:
            newHead = self.moveDirection(direction)
            if self.isValidMove(newHead):
                result.append(newHead)
        return result

    """
    The head position if the snake is moved in the given direction
    @returns the new head position the snake would be if it moved in the given direction
    @requires that the given direction is valid
    """
    def moveDirection(self, direction: str) -> tuple[int, int]:
        head = self.game.getSnakeHead()
        match direction:
            case "l":
                return (head[0] - 1, head[1])
            case "r":
                return (head[0] + 1, head[1])
            case "u":
                return (head[0], head[1] - 1)
            case "d":
                return (head[0], head[1] + 1)

    def isValidMove(self, newHead: tuple[int, int]):
        if newHead in self.game.getSnakeBody():
            return False
        return 0 <= newHead[0] < self.XCELLS and 0 <= newHead[1] < self.YCELLS


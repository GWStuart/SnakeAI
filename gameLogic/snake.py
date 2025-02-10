"""
Implements the Snake class that is used to represent snakes in the game.
This class should be used as a reference for the behaviour of the snake 
and all snake bots will be tested using a snake that is instantiated 
with this class
"""
import random

class Snake:
    SNAKE_SPAWN_POSITION = (2, 2)

    def __init__(self, DIMENSIONS: tuple[int, int], SPAWN_POSITION: tuple[int, int], direction: tuple[int, int]=(1, 0)):
        self.XCELLS, self.YCELLS = DIMENSIONS
        self.SPAWN_POSITION = SPAWN_POSITION
        self.direction = direction

        self.headX, self.headY = self.SPAWN_POSITION
        self.body = [(self.headX, self.headY)]

        self.apple = self.getRandomCell()
        self.score = 0

    """
    Returns a random position on the grid that the snake body dodes not occupy
    """
    def getRandomCell(self) -> tuple[int, int]:
        x, y = random.randint(0, self.XCELLS - 1), random.randint(0, self.YCELLS - 1)
        while (x, y) in self.body:
            x, y = random.randint(0, self.XCELLS - 1), random.randint(0, self.YCELLS - 1)
        return (x, y)

    """
    Updates the snake direction so that it makes a right left
    """
    def turn_left(self):
        self.direction = (-self.direction[1], self.direction[0])

    """
    Updates the snake direction so that it makes a right turn
    """
    def turn_right(self):
        self.direction = (self.direction[1], -self.direction[0])

    """
    Changes the snake's direction to the speccified value.

    Directions should be one of: (1, 0), (-1, 0), (0, 1), (0, -1)
    representing right, left, up, down respectively
    """
    def change_direction(self, direction: tuple[int, int]):
        self.direction = direction

    """
    Moves the snake in the direction that they are currently facing 

    Note that the move will be peformed even if it results in a game over state.
    Check whether the snake is in a game over state with the snake.isGameOver() method

    @returns True if the move results in an eaten apple and False otherwise
    """
    def move(self) -> bool:
        # move the snakes head
        self.headX += self.direction[0]
        self.headY += self.direction[1]

        # add the new head position to the body
        self.body.append((self.headX, self.headY))

        # Check if the snake's head is on an apple
        if (self.headX, self.headY) == self.apple:
            self.score += 1
            self.apple = self.getRandomCell()
            return True
        else:
            self.body.pop(0)  # decrease the snake's length
            return False

    """
    Method used to return the snake body
    NOTE: it does not return a copy! It returns the actual snake body
    """
    def getBody(self) -> list[tuple[int]]:
        return self.body

    """
    Method used to return the apple's position
    """
    def getApplePosition(self) -> tuple[int, int]:
        return self.apple

    """
    Returns the current score of the game
    """
    def getScore(self) -> int:
        return self.score

    """
    Returns the position of the snake's head
    """
    def getHead(self) -> tuple[int, int]:
        return (self.headX, self.headY)

    """
    Get the dimensions of the board as a tuple of (XCElLS, YCELLS)
    """
    def getDimensions(self) -> tuple[int, int]:
        return (self.XCELLS, self.YCELLS)
    
    """
    Returns the current direction of the snake.

    This will either be the direction of the snake's last move,
    or a new direction if a method was used to change the snake's direction.
    In this case that new direction will hence specify where the snake is going to move to 
    the next time that the snake.move() method is called
    """
    def getDirection(self) -> tuple[int, int]:
        return self.direction

    """
    Checks if the snake is in a game over position
    @requires that the snake was in valid position in its previous state
    @returns True if the game is over and False otherwise
    """
    def isGameOver(self) -> bool:
        # Check if the head has gone off the grid
        if self.headX < 0 or self.headX > self.XCELLS - 1 or self.headY < 0 or self.headY > self.YCELLS - 1:
            return True

        # Check if the head is within the body
        if self.body[-1] in self.body[:-1]:
            return True

        return False


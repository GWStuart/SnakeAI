from abstractBot import Bot
import math

class Bot1(Bot):
    def makeMove(self):
        apple = self.game.getApplePosition()

        moves = self.getMoves()

        if len(moves) == 0:
            return "l"  # the game has been lost

        distances = map(lambda x: math.dist(x, apple), moves)
        move = min(zip(distances, moves), key=lambda x: x[0])[1]

        return self.getMoveDirection(move)


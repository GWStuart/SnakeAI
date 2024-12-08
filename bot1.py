from abstractBot import Bot
import math

class Bot2(Bot):
    def makeMove(self):
        apple = self.game.getApplePosition()

        moves = self.getMoves()
        valid_moves = list(filter(self.isValidMove, moves))

        if len(valid_moves) == 0:
            return "l"  # the game has been lost

        distances = list(map(lambda x: math.dist(x, apple), valid_moves))
        move = min(zip(distances, valid_moves), key=lambda x: x[0])[1]

        return self.getMoveDirection(move)


from abstractBot import Bot
import math

class Bot2(Bot):
    def makeMove(self, snake: list[tuple[int, int]], apple: tuple[int, int]):
        moves = self.getMoves(snake)

        if len(moves) == 0:
            return "l"  # the game has been lost

        trapped = self.trapped_squares_quick(snake, moves)
       
        score = []
        for move, trapped in zip(moves, trapped):
            distance = math.dist(move, apple)
            score.append(trapped * 300 + distance)

        move = min(zip(score, moves), key=lambda x: x[0])[1]

        return self.getMoveDirection(snake, move)


from abstractBot import Bot
import math

class Bot2(Bot):
    def makeMoveDirect(self, snake: list[tuple[int, int]], apple: tuple[int, int]):
        moves = self.getMoves()

        if len(moves) == 0:
            return "l"  # the game has been lost

        available_squares = self.XCELLS * self.YCELLS - len(snake)

        score = []
        for move in moves:
            trapped_squares = available_squares - self.floodfill(*move, set())
            distance = math.dist(move, apple)
            score.append(trapped_squares * 300 + distance)

        move = min(zip(score, moves), key=lambda x: x[0])[1]
        return self.getMoveDirection(move)


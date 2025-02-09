from abstractBot import Bot
import math

class Bot2(Bot):
    """
    Calculates the number of trapped squares for the given snake when starting from the specified cells

    NOTE: this algorithm will return zeros if all cells are mutually accessible. This might not always be what you want

    @param snake, the snake body
    @param cells, the cells to start checking for trapped cells relative to
    @returns a list representing the number of trapped squares for each cell in order
    """
    def trapped_squares_quick(self, snake: list[tuple[int, int]], cells: list[tuple[int, int]]):
        snake_set = set(snake)
        available_squares = self.XCELLS * self.YCELLS - len(snake)

        cell_indices = {cell: i for i, cell in enumerate(cells)}

        result = [0] * len(cells)
        for i, cell in enumerate(cells):
            if result[i]:
                continue

            indexes = set()
            filled = set()
            uncovered = len(cells)

            stack = {cell}
            while stack:
                x, y = stack.pop()

                if (x, y) in cells:
                    indexes.add(cell_indices.get((x, y)))
                    uncovered -= 1
                    if uncovered == 0:  # MIGHT WANT TO REMOVE IN FUTURE
                        return result

                filled.add((x, y))
        
                if x > 0 and (x - 1, y) not in snake_set and (x - 1, y) not in filled:
                    stack.add((x - 1, y))
                if x < self.XCELLS - 1 and (x + 1, y) not in snake_set and (x + 1, y) not in filled:
                    stack.add((x + 1, y))
                if y > 0 and (x, y - 1) not in snake_set and (x, y - 1) not in filled:
                    stack.add((x, y - 1))
                if y < self.YCELLS - 1 and (x, y + 1) not in snake_set and (x, y + 1) not in filled:
                    stack.add((x, y + 1))
        
            trapped = available_squares - len(filled)
            for idx in indexes:
                result[idx] = trapped
       
        return result

    """
    Determine the move that this bot will take at a given position
    """
    def makeMove(self, snake: list[tuple[int, int]], apple: tuple[int, int]):
        moves = self.getMoves(snake)

        if len(moves) == 0:
            return (1, 0)  # the game has been lost

        trapped = self.trapped_squares_quick(snake, moves)
       
        score = []
        for move, trapped in zip(moves, trapped):
            distance = math.dist(move, apple)
            score.append(trapped * 300 + distance)

        move = min(zip(score, moves), key=lambda x: x[0])[1]

        return self.getMoveDirection(snake, move)


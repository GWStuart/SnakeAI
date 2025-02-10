"""
Used to generate medium quality renders.
"""
from render.util import AbstractRender
import numpy as np
import cv2


class RenderMD(AbstractRender):
    DESIRED_SCREEN_WIDTH = 768

    """
    Render a grid tile the given colour
    @param frame the frame on which to render the tile
    @param x the x position of the tile
    @param y the y position of the tile
    @param colour an rgb tuple representing the colour of the tile
    """
    def renderTile(self, frame, x: int, y: int, colour: tuple[int, int, int]) -> None:
        cv2.rectangle(frame, (1 + x*self.CELL_SIZE, 1 + y*self.CELL_SIZE), (1 + (x+1)*self.CELL_SIZE, 1 + (y+1)*self.CELL_SIZE), colour, -1)

    """
    Render the frame based on the current state of the game
    """
    def render(self) -> None:
        frame = np.zeros((self.HEIGHT, self.LENGTH, 3), dtype=np.uint8)

        # render the snake body
        body = self.snake.getBody()
        for i in range(len(body) - 1):
            part = body[i]
            self.renderTile(frame, *part, (0, 255, 0))

        # render the snake head
        head = body[-1]
        self.renderTile(frame, *head, (0, 200, 0))

        # render the apple
        apple = self.snake.getApplePosition()
        self.renderTile(frame, *apple, (0, 0, 255))

        # render the score
        score = self.snake.getScore()
        cv2.putText(frame, f"score: {score}", (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv2.LINE_AA)

        # add a white border
        self.draw_border(frame)

        self.video.write(frame)

"""
Used to generate low quality renders.

These renders are the fastest to generate.

This is achieved with:
    - smaller output dimensions
    - black and white render
"""
from render.util import AbstractRender
import numpy as np
import cv2


class RenderLD(AbstractRender):
    """
    Use a custom video writer to generate low quality videos in black and white
    """
    def generateVideoWriter(self):
        return cv2.VideoWriter(f"./{self.OUTPUT_FILE}", self.FOURCC, float(self.FPS), (self.LENGTH, self.HEIGHT), 0)

    """
    Render a grid tile the given colour
    @param frame the frame on which to render the tile
    @param x the x position of the tile
    @param y the y position of the tile
    @param colour an rgb tuple representing the colour of the tile
    """
    # note it is not actually RGB right now because I am working wtih gray scale
    def renderTile(self, frame, x: int, y: int, colour: tuple[int, int, int]) -> None:
        cv2.rectangle(frame, (1 + x*self.CELL_SIZE, 1 + y*self.CELL_SIZE), (1 + (x+1)*self.CELL_SIZE, 1 + (y+1)*self.CELL_SIZE), colour, -1)

    """
    Render the frame based on the current state of the game
    """
    def render(self) -> None:
        frame = np.zeros((self.HEIGHT, self.LENGTH), dtype=np.uint8)

        body = self.snake.getBody()
        for part in body:
            self.renderTile(frame, *part, 255)

        apple = self.snake.getApplePosition()
        self.renderTile(frame, *apple, 100)

        # add a white border
        if self.BORDER:
            frame[:, 0] = np.array(255)
            frame[:, self.LENGTH - 1] = np.array(255)
            frame[0, :] = np.array(255)
            frame[self.HEIGHT - 1, :] = np.array(255)

        self.video.write(frame)


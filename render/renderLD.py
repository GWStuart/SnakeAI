"""
Used to generate low quality renders.

These renders are the fastest to generate.

This is achieved with:
    - smaller output dimensions
    - black and white render
"""
import numpy as np
import cv2


class render_LD:
    FOURCC = cv2.VideoWriter_fourcc(*"mp4v")

    """
    Initialises the low quality render
    @param output_file the file where the video should be saved
    @param snake the snake object representing the game
    @param CEll_SIZE the size in pixels of each cell in the grid
    @param FPS the fps at which to render the game (affects playback speed)
    """
    def __init__(self, output_file, snake, CELL_SIZE=None, FPS=30, BORDER=True):
        self.snake = snake
        self.FPS = FPS
        self.BORDER = BORDER

        # calculate the cell size for a low quality render
        XCELLS, YCELLS = snake.getDimensions()
        if CELL_SIZE:
            self.CELL_SIZE = CELL_SIZE
        else:
            self.CELL_SIZE = round(360 / XCELLS)

        # Determine the output dimensions
        self.LENGTH = XCELLS * self.CELL_SIZE + 2
        self.HEIGHT = YCELLS * self.CELL_SIZE + 2

        # Generate the video writer
        self.video = cv2.VideoWriter(f"./{output_file}", self.FOURCC, float(self.FPS), (self.LENGTH, self.HEIGHT), 0)

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

    """
    Method that should be run when the rendering if finished.
    Releases the video object
    """
    def finish(self) -> None:
        self.video.release()

"""
Used to generate medium quality renders.
"""
import numpy as np
import cv2


class render_MD:
    FOURCC = cv2.VideoWriter_fourcc(*"mp4v")

    """
    Initialises the medium quality render
    @param output_file the file where the video should be saved
    @param snake the snake object representing the game
    @param CEll_SIZE the size in pixels of each cell in the grid
    @param FPS the fps at which to render the game (affects playback speed)
    """
    def __init__(self, output_file, snake, CELL_SIZE=None, FPS=30, BORDER=True):
        self.snake = snake
        self.FPS = FPS
        self.BORDER = BORDER

        # calculate the cell size for a high quality render
        XCELLS, YCELLS = snake.getDimensions()
        if CELL_SIZE:
            self.CELL_SIZE = CELL_SIZE
        else:
            self.CELL_SIZE = round(768 / XCELLS)

        # Determine the output dimensions
        self.LENGTH = XCELLS * self.CELL_SIZE + 2
        self.HEIGHT = YCELLS * self.CELL_SIZE + 2

        # Generate the video writer
        self.video = cv2.VideoWriter(f"./{output_file}", self.FOURCC, float(self.FPS), (self.LENGTH, self.HEIGHT))

    def renderTile(self, frame, x: int, y: int, colour: tuple[int, int, int]) -> None:
        cv2.rectangle(frame, (1 + x*self.CELL_SIZE, 1 + y*self.CELL_SIZE), (1 + (x+1)*self.CELL_SIZE, 1 + (y+1)*self.CELL_SIZE), colour, -1)

    """
    Render the frame based on the current state of the game
    """
    def render(self) -> None:
        frame = np.zeros((self.HEIGHT, self.LENGTH, 3), dtype=np.uint8)

        body = self.snake.getBody()
        for i in range(len(body) - 1):
            part = body[i]
            self.renderTile(frame, *part, (0, 255, 0))

        head = body[-1]
        self.renderTile(frame, *head, (0, 200, 0))

        apple = self.snake.getApplePosition()
        self.renderTile(frame, *apple, (0, 0, 255))

        score = self.snake.getScore()
        cv2.putText(frame, f"score: {score}", (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv2.LINE_AA)

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

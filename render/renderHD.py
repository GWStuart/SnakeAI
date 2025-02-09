"""
Used to generate high quality renders.

These renders take the longest to process
"""
import numpy as np
import cv2


class render_HD:
    FOURCC = cv2.VideoWriter_fourcc(*"mp4v")

    """
    Initialises the high quality render
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
            self.CELL_SIZE = round(1280 / XCELLS)

        # Determine the output dimensions
        self.LENGTH = XCELLS * self.CELL_SIZE + 2
        self.HEIGHT = YCELLS * self.CELL_SIZE + 2

        # Generate the video writer
        self.video = cv2.VideoWriter(f"./{output_file}", self.FOURCC, float(self.FPS), (self.LENGTH, self.HEIGHT), 0)


    """
    Render the frame based on the current state of the game
    """
    def render(self) -> None:
        frame = np.zeros((self.HEIGHT, self.LENGTH, 3), dtype=np.uint8)

        # draw the snake body
        body = self.snake.getBody()
        get_center = lambda part: (round((part[0] + 0.5) * self.CELL_SIZE), round((part[1] + 0.5) * self.CELL_SIZE))
        for i in range(len(body) - 1):
            cv2.line(frame, get_center(body[i]), get_center(body[i+1]), (0, 200, 0), math.ceil(0.75 * self.CELL_SIZE))

        # add eyes to the snake
        if len(body) > 1:
            head = get_center(body[-1])
            eye_distance = round(self.CELL_SIZE/6)
            head_offset = round(self.CELL_SIZE/6)
            if last_move == "l":
                head = (head[0] - head_offset, head[1])
                cv2.circle(frame, (head[0], head[1] + eye_distance), math.ceil(0.1 * self.CELL_SIZE), (0, 100, 0), -1)
                cv2.circle(frame, (head[0], head[1] - eye_distance), math.ceil(0.1 * self.CELL_SIZE), (0, 100, 0), -1)
            if last_move == "r":
                head = (head[0] + head_offset, head[1])
                cv2.circle(frame, (head[0], head[1] + eye_distance), math.ceil(0.1 * self.CELL_SIZE), (0, 100, 0), -1)
                cv2.circle(frame, (head[0], head[1] - eye_distance), math.ceil(0.1 * self.CELL_SIZE), (0, 100, 0), -1)
            if last_move == "u":
                head = (head[0], head[1] - head_offset)
                cv2.circle(frame, (head[0] + eye_distance, head[1]), math.ceil(0.1 * self.CELL_SIZE), (0, 100, 0), -1)
                cv2.circle(frame, (head[0] - eye_distance, head[1]), math.ceil(0.1 * self.CELL_SIZE), (0, 100, 0), -1)
            if last_move == "d":
                head = (head[0], head[1] + head_offset)
                cv2.circle(frame, (head[0] + eye_distance, head[1]), math.ceil(0.1 * self.CELL_SIZE), (0, 100, 0), -1)
                cv2.circle(frame, (head[0] - eye_distance, head[1]), math.ceil(0.1 * self.CELL_SIZE), (0, 100, 0), -1)

        # render the apple
        apple = self.snake.getApplePosition()
        cv2.circle(frame, get_center(apple), math.ceil(0.37 * self.CELL_SIZE), (0, 0, 255), -1)

        # display the score
        cv2.putText(frame, f"score: {game.getScore()}", (20, 40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 1, cv2.LINE_AA)

        # add a white border
        if self.BORDER:
            frame[:, 0] = np.array(255)
            frame[:, self.LENGTH - 1] = np.array(255)
            frame[0, :] = np.array(255)
            frame[self.HEIGHT - 1, :] = np.array(255)

        # write the frame to the video
        self.video.write(frame)

    """
    Method that should be run when the rendering if finished.
    Releases the video object
    """
    def finish(self) -> None:
        self.video.release()

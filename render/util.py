import cv2


"""
Abstract class for the render objects
"""
class AbstractRender:
    FOURCC = cv2.VideoWriter_fourcc(*"mp4v")
    DESIRED_SCREEN_WIDTH = 360

    """
    Initialises the abstract render
    @param output_file the file where the video should be saved (assumes it doesn't already exist)
    @param snake the snake object representing the game
    @param CEll_SIZE the size in pixels of each cell in the grid
    @param FPS the fps at which to render the game (affects playback speed)
    """
    def __init__(self, OUTPUT_FILE, snake, CELL_SIZE=None, FPS=30, BORDER=True):
        self.OUTPUT_FILE = OUTPUT_FILE
        self.snake = snake
        self.FPS = FPS
        self.BORDER = BORDER

        # calculate the cell size for a low quality render
        XCELLS, YCELLS = snake.getDimensions()
        if CELL_SIZE:
            self.CELL_SIZE = CELL_SIZE
        else:
            self.CELL_SIZE = round(self.DESIRED_SCREEN_WIDTH / XCELLS)

        # Determine the output dimensions
        self.LENGTH = XCELLS * self.CELL_SIZE + 2
        self.HEIGHT = YCELLS * self.CELL_SIZE + 2

        # Generate the video writer
        self.video = self.generateVideoWriter()

    """
    The video writer to be used
    """
    def generateVideoWriter(self):
        return cv2.VideoWriter(f"./{self.OUTPUT_FILE}", self.FOURCC, float(self.FPS), (self.LENGTH, self.HEIGHT))

    """
    Render a frame based on the state of the game
    """
    def render(self) -> None:
        # this method is implemented by the subclasses
        pass

    """
    Method that should be run when the rendering if finished.
    Releases the video object
    """
    def finish(self) -> None:
        self.video.release()


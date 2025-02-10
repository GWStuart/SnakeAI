"""
Used to generate high quality renders.

These renders take the longest to process
"""
from render.util import AbstractRender
import numpy as np
import cv2
import math


class RenderHD(AbstractRender):
    DESIRED_SCREEN_WIDTH = 1280

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
            
            last_move = self.snake.getDirection()
            if last_move == (-1, 0):
                head = (head[0] - head_offset, head[1])
                cv2.circle(frame, (head[0], head[1] + eye_distance), math.ceil(0.1 * self.CELL_SIZE), (0, 100, 0), -1)
                cv2.circle(frame, (head[0], head[1] - eye_distance), math.ceil(0.1 * self.CELL_SIZE), (0, 100, 0), -1)
            elif last_move == (1, 0):
                head = (head[0] + head_offset, head[1])
                cv2.circle(frame, (head[0], head[1] + eye_distance), math.ceil(0.1 * self.CELL_SIZE), (0, 100, 0), -1)
                cv2.circle(frame, (head[0], head[1] - eye_distance), math.ceil(0.1 * self.CELL_SIZE), (0, 100, 0), -1)
            elif last_move == (0, -1):
                head = (head[0], head[1] - head_offset)
                cv2.circle(frame, (head[0] + eye_distance, head[1]), math.ceil(0.1 * self.CELL_SIZE), (0, 100, 0), -1)
                cv2.circle(frame, (head[0] - eye_distance, head[1]), math.ceil(0.1 * self.CELL_SIZE), (0, 100, 0), -1)
            elif last_move == (0, 1):
                head = (head[0], head[1] + head_offset)
                cv2.circle(frame, (head[0] + eye_distance, head[1]), math.ceil(0.1 * self.CELL_SIZE), (0, 100, 0), -1)
                cv2.circle(frame, (head[0] - eye_distance, head[1]), math.ceil(0.1 * self.CELL_SIZE), (0, 100, 0), -1)

        # render the apple
        apple = self.snake.getApplePosition()
        cv2.circle(frame, get_center(apple), math.ceil(0.37 * self.CELL_SIZE), (0, 0, 255), -1)

        # display the score
        score = self.snake.getScore()
        cv2.putText(frame, f"score: {score}", (20, 40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 1, cv2.LINE_AA)

        # add a white border
        self.draw_border(frame)

        # write the frame to the video
        self.video.write(frame)


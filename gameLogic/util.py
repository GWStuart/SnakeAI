"""
A few useful function to be used in combination with the Snake class
"""

DIRECTION_ENCODE = {(1, 0): "r", (-1, 0): "l", (0, -1): "u", (0, 1): "d"}
DIRECTION_DECODE = {"r": (1, 0), "l": (-1, 0), "u": (0, -1), "d": (0, 1)}


"""
Converts a direction tuple to its string representation
@param direction the direction tuple
"""
def encodeDirection(direction: tuple[int, int]) -> str:
    return DIRECTION_ENCODE[direction]

"""
Converts a direction string to its tuple representation
@param direction the direction string
"""
def decodeDirection(direction: str) -> tuple[int, int]:
    return DIRECTION_DECODE[direction]


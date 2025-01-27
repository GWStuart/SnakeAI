import os

"""
Finds a valid filename that does not exist in the /saves directory
Will start with the specified file name and append duplicate counts if the file already exists.
"""
def getNewFile(filename: str, extension: str) -> str:
    path = f"saves/{filename}.{extension}"
    if not os.path.exists(path):
        return path

    n = 2
    path = f"saves/{filename}{n}.{extension}"
    while os.path.exists(path):
        n += 1
        path = f"saves/{filename}{n}.{extension}"

    return path

def saveGame(filename, XCELLS, YCELLS, seed, num_moves, moves):
    with open(filename, "w") as f:
        f.write(f"{XCELLS} {YCELLS} {seed} {num_moves}\n")
        f.write("".join(moves))

"""
Handles file operations

Snake games are stored at:       saves/games
Snake mp4 renders are stored at: saves/renders
"""
import os

DEFAULT_FILE_NAME = "output"
SAVES_LOCATION = "saves"
GAME_SAVE_LOCATION = f"{SAVES_LOCATION}/games"
RENDER_SAVE_LOCATION = f"{SAVES_LOCATION}/renders"

"""
Ensures that the relevant save directories exist
"""
def createSaveDirectory():
    if not os.path.exists("./saves"):
        os.mkdir("./saves")

    if not os.path.exists("./saves/games"):
        os.mkdir("./saves/games")

    if not os.path.exists("./saves/renders"):
        os.mkdir("./saves/renders")

"""
Returns the default output file name for a given input file name
"""
def getDefaultOutputFileName(input_file_name: str) -> str:
    # replace the file extension
    file = input_file_name.partition(".")[0]

    # remove file location
    file = file[-file[::-1].index("/"):]

    # return the default output location
    return f"{RENDER_SAVE_LOCATION}/{file}"


"""
Finds a valid filename that does not exist in the /saves directory
Will start with the specified file name and append duplicate counts if the file already exists.
"""
def getNewFile(filename: str, extension: str) -> str:
    # check that a filename was specified
    if not filename:
        if extension == "snake":
            filename = f"{GAME_SAVE_LOCATION}/{DEFAULT_FILE_NAME}"
        elif extension == "mp4":
            filename = f"{RENDER_SAVE_LOCATION}/{DEFAULT_FILE_NAME}"
        else:
            filename = f"{SAVES_LOCATION}/{DEFAULT_FILE_NAME}"

    # Ensure that the saves directory exists
    createSaveDirectory()
    
    # determine the full file path
    path = f"{filename}.{extension}"

    # check that the file path does not already exist
    if not os.path.exists(path):
        return path

    # increment file number if the given file already exists
    n = 2
    path = f"{filename}{n}.{extension}"
    while os.path.exists(path):
        n += 1
        path = f"{filename}{n}.{extension}"

    # return the final modified path
    return path


"""
Saves a snake game
"""
def saveGame(filename, XCELLS, YCELLS, seed, num_moves, moves):
    with open(filename, "w") as f:
        f.write(f"{XCELLS} {YCELLS} {seed} {num_moves}\n")
        f.write("".join(moves))

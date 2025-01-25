# SnakeAI
Simple Snake Game AI

# How to Use
First install the python dependencies.
I would recommend doing this in a virtual environment
- `python -m pip install -r requirements.txt`

The AI bots are defined in files named `botx.py` where `x` is a number.
There are currently two bots (i.e. `bot1.py` and `bot2.py` but more are being developed)

The `botTester.py` program is used to test the AI bots.
The bot you wish to test must be chosen from within the file and executing the file will simulate a snake game and record all moves made.
The resulting game is stored at `saves/output.snake` (or a custom location if specified with the `-o` tag).

To render a saved game use the `render.py` file.
This file allows many customisations including:
- render quality
- FPS
- scale
The output will be an mp4 file.

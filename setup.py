# 'python3 setup.py bdist_mac' or 'bdist_msi' on windows

application_title = "Maze Game" 
main_python_file = "koodi.py" 

import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

packages = ["pygame", "os", "time", "random", "math", "time", "sys", "string"]
#includes = ["gameinfo"]
include_files = ["Elevator_music.ogg", "Pat_and_Mat_intro.ogg", "RedCheck.png","MazeIcon1.png"]
# includes = []

excludes = ["Savegames", "highscores.ma", ".DS_Store", "testIO", "testmatrixalgorithm", ".pyc"]


setup(
        name = application_title,
        version = "1.0",
        description = "Maze game cx_Freezed",
        options = {"build_exe" : {"includes" : packages, "excludes" : excludes, "include_files" : include_files}},
        executables = [Executable(main_python_file, base = base)]
        )
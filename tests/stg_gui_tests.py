from nose.tools import *
import inspect
import os
import stg_gui


def setup():
    print "SETUP!"


def teardown():
    print "TEAR DOWN!"


def test_screenplay_modules_for_associated_directories():
    py_ext, module_ext, slash = ".py", "_stg", "\\"
    game_list, dir_list = [], []

    current_dir = os.path.dirname(inspect.getabsfile(inspect.currentframe()))
    screenplay_dir = os.path.join(current_dir.replace('\\tests', ''), 'storythegame', 'screenplays')

    for game_file in os.listdir(screenplay_dir):
        file_path = os.path.join(screenplay_dir, game_file)

        if os.path.isfile(file_path) and game_file.endswith(py_ext) and not game_file.startswith("__init__"):
            game_list.append(game_file[:-len(py_ext + module_ext)])

        if os.path.isdir(file_path):
            split_path = file_path.split(slash)
            dir_list.append(split_path[-1])

    print "game list: ", game_list, " and dir list: ", dir_list
    assert game_list == dir_list

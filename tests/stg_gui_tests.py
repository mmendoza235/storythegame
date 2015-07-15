from nose.tools import *
import inspect
import os

import custom_test_util as ctu
import stg_gui


def setup():
    ctu.output_divider(setup.__name__, 'SETTING UP!')

    global py_ext, module_ext, slash, screenplay_dir
    py_ext, module_ext, slash = ".py", "_stg", "\\"

    current_dir = os.path.dirname(inspect.getabsfile(inspect.currentframe()))
    screenplay_dir = os.path.join(current_dir.replace('\\tests', ''), 'storythegame', 'screenplays')

    ctu.output_divider(setup.__name__, 'DONE SETTING UP!')


def teardown():
    ctu.output_divider(teardown.__name__, 'TEARING DOWN!')

    global py_ext, module_ext, slash, screenplay_dir
    del py_ext, module_ext, slash, screenplay_dir

    ctu.output_divider(teardown.__name__, 'DONE TEARING DOWN!')


def test_screenplay_modules_for_associated_directories():
    ctu.output_divider(test_screenplay_modules_for_associated_directories.__name__, 'START')

    game_list, dir_list = [], []

    for game_file in os.listdir(screenplay_dir):
        file_path = os.path.join(screenplay_dir, game_file)

        if os.path.isfile(file_path) and game_file.endswith(py_ext) and not game_file.startswith("__init__"):
            game_list.append(game_file[:-len(py_ext + module_ext)])

        if os.path.isdir(file_path):
            split_path = file_path.split(slash)
            dir_list.append(split_path[-1])

    print "game list: ", game_list, " and dir list: ", dir_list
    assert_equal(game_list, dir_list)

    ctu.output_divider(test_screenplay_modules_for_associated_directories.__name__, 'FINISH')

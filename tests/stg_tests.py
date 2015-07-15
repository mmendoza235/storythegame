from nose.tools import *
import inspect
import os

import custom_test_util as ctu
import storythegame.stg as stg


def setup():
    ctu.output_divider(setup.__name__, 'SETTING UP!')
    global screenplay_dir

    current_dir = os.path.dirname(inspect.getabsfile(inspect.currentframe()))
    screenplay_dir = os.path.join(current_dir.replace('\\tests', ''), 'storythegame', 'screenplays')

    global screenplay_map

    screenplay_map = []

    treasureRoom = stg.ComparisonStory("treasureRoom", 10000)
    treasureRoom.story_item = 'sword'

    screenplay_map.append(stg.BaseStory("gameStart"))
    screenplay_map.append(stg.BaseStory("bearRoom"))
    screenplay_map.append(stg.BaseStory("insaneRoom"))
    screenplay_map.append(stg.BaseStory("fancyHallway"))
    screenplay_map.append(stg.WhileStory("bearGrills"))
    screenplay_map.append(stg.BaseStory("darkCavern"))
    screenplay_map.append(stg.BaseStory("strangeLight"))
    screenplay_map.append(treasureRoom)
    screenplay_map.append(stg.BaseStory("unknownDoor"))
    screenplay_map.append(stg.BaseStory("trapDoor"))

    ctu.output_divider(setup.__name__, 'DONE SETTING UP!')


def teardown():
    ctu.output_divider(teardown.__name__, 'TEARING DOWN!')

    global screenplay_dir, screenplay_map
    del screenplay_dir, screenplay_map

    ctu.output_divider(teardown.__name__, 'DONE TEARING DOWN!')


def test_verify_default_story_path():
    ctu.output_divider(test_verify_default_story_path.__name__, 'START')

    stg_story_path = stg.story_path
    test_story_path = os.path.join(screenplay_dir, 'default\\')

    print "stg story path: ", stg_story_path
    print "test story path: ", test_story_path

    assert_equal(stg_story_path, test_story_path)

    ctu.output_divider(test_verify_default_story_path.__name__, 'FINISH')


def test_mapping_class():
    ctu.output_divider(test_mapping_class.__name__, 'START')

    for num in range(len(screenplay_map)):
        assert_equal(stg.StoryMap().map[screenplay_map[num].room_name], screenplay_map[num])

    ctu.output_divider(test_mapping_class.__name__, 'FINISH')


def test_default_screenplay_files_for_content():
    ctu.output_divider(test_default_screenplay_files_for_content.__name__, 'START')

    for num in range(len(screenplay_map)):
        screenplay_script = screenplay_map[num].import_story()

        print "Screenplay script for room ", screenplay_map[num].room_name
        print screenplay_script, "\n"

        assert screenplay_script
        assert_is_instance(screenplay_script, list)

    ctu.output_divider(test_default_screenplay_files_for_content.__name__, 'FINISH')

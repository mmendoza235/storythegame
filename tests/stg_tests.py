from nose.tools import *
import inspect
import os

import custom_test_util as ctu
import storythegame.stg as stg


def simulate_user_entry(answer):
    """
    Helper function to simulate user entry and return necessary variables
    """
    sceneInstance = stg.StoryMap().map[stg.current_scene]
    choice = sceneInstance.user_choice(answer)
    sceneInstance.story_reduce(answer, choice, stg.gui_script)

    return choice


def setup():
    ctu.output_divider(setup.__name__, 'SETTING UP!')

    stg.game_mode = "TEST"

    global screenplay_dir

    current_dir = os.path.dirname(inspect.getabsfile(inspect.currentframe()))
    screenplay_dir = os.path.join(current_dir.replace('\\tests', ''), 'storythegame', 'screenplays')

    global screenplay_map

    screenplay_map = []

    treasureRoom = stg.ComparisonStory("treasureRoom", 10000)
    treasureRoom.story_item = 'sword'

    screenplay_map.append(stg.BaseStory("gameStart"))       # index: 0
    screenplay_map.append(stg.BaseStory("bearRoom"))        # index: 1
    screenplay_map.append(stg.BaseStory("insaneRoom"))      # index: 2
    screenplay_map.append(stg.BaseStory("fancyHallway"))    # index: 3
    screenplay_map.append(stg.WhileStory("bearGrills"))     # index: 4
    screenplay_map.append(stg.BaseStory("darkCavern"))      # index: 5
    screenplay_map.append(stg.BaseStory("strangeLight"))    # index: 6
    screenplay_map.append(treasureRoom)                     # index: 7
    screenplay_map.append(stg.BaseStory("unknownDoor"))     # index: 8
    screenplay_map.append(stg.BaseStory("trapDoor"))        # index: 9

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


def test_default_story_playthrough():
    ctu.output_divider(test_default_story_playthrough.__name__, 'START')

    user_input = {
        'Final room, no sword, all treasure': [['1', 'bearRoom'], ['3', 'bearGrills'], ['1', 'darkCavern'], ['3', 'strangeLight'], ['1', 'treasureRoom'], ['10000', '']],
        'Final room, sword, all treasure': [['3', 'fancyHallway'], ['1', 'unknownDoor'], ['2', 'darkCavern'], ['3', 'strangeLight'], ['1', 'treasureRoom'], ['10000', '']],
        'Final room, sword, too little treasure': [['3', 'fancyHallway'], ['1', 'unknownDoor'], ['2', 'darkCavern'], ['3', 'strangeLight'], ['1', 'treasureRoom'], ['10', '']]
    }

    for key, value in user_input.iteritems():
        ctu.output_divider('Testing scenario', key)

        # gameStart screenplay
        screenplay_map[0].story_intro()

        for num in range(len(value)):
            choice = simulate_user_entry(value[num][0])

            assert_equal(stg.current_scene, value[num][1])

    ctu.output_divider(test_default_story_playthrough.__name__, 'FINISH')


def test_while_story():
    ctu.output_divider(test_while_story.__name__, 'START')

    user_input = [
        ['toast', 'bearGrills'], ['no!', 'bearGrills'], ['wrong!', 'bearGrills'], ['invalid answer', 'bearGrills'], ['2', '']
    ]

    # bearGrills screenplay
    screenplay_map[4].story_intro()

    for num in range(len(user_input)):
        choice = simulate_user_entry(user_input[num][0])

        assert_equal(stg.current_scene, user_input[num][1])

    ctu.output_divider(test_while_story.__name__, 'FINISH')


def test_valid_user_input():
    ctu.output_divider(test_valid_user_input.__name__, 'START')

    user_input = {
        'BaseStory test (gameStart)': [['oNe', '1. '], ['ONE', '1. '], ['   one  ', '1. '], [' on e ', 'ELSE: '], ['1. ', 'ELSE: '], ['won', 'ELSE: '], ['toast', 'ELSE: '], ['10000', 'ELSE: '], ['1', '1. '], ['0', 'ELSE: ']],
        'WhileStory test (bearGrills)': [['oNe', '1. '], ['ONE', '1. '], ['   one  ', '1. '], [' on e ', 'ELSE: '], ['1. ', 'ELSE: '], ['won', 'ELSE: '], ['toast', 'ELSE: '], ['10000', 'ELSE: '], ['1', '1. '], ['0', 'ELSE: ']],
        'CompareStory test (treasureRoom)': [['oNe', 'ELSE: '], ['ONE', 'ELSE: '], ['   one  ', 'ELSE: '], [' on e ', 'ELSE: '], ['1. ', 'ELSE: '], ['won', 'ELSE: '], ['toast', 'ELSE: '], ['10000', '1. '], ['1', '2. '], ['0', '3. ']]
    }

    class_dict = {
        'BaseStory test (gameStart)': screenplay_map[0],
        'WhileStory test (bearGrills)': screenplay_map[4],
        'CompareStory test (treasureRoom)': screenplay_map[7]
    }

    for key, value in user_input.iteritems():
        ctu.output_divider(key, 'Starting Test')

        for num in range(len(value)):
            subtitle = "User input test: %r" % value[num][0]
            ctu.output_divider(key, subtitle)

            class_dict[key].story_intro()
            choice = simulate_user_entry(value[num][0])

            assert_equal(choice, value[num][1])

        ctu.output_divider(key, 'Finished Test')

    ctu.output_divider(test_valid_user_input.__name__, 'FINISH')

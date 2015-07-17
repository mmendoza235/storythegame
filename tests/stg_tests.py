from nose.tools import *
import inspect
import os

import custom_test_util as ctu
import storythegame.stg as stg


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
            sceneInstance = stg.StoryMap().map[stg.current_scene]
            answer = value[num][0]
            choice = sceneInstance.user_choice(answer)
            sceneInstance.story_reduce(answer, choice, stg.gui_script)

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
        sceneInstance = stg.StoryMap().map[stg.current_scene]
        answer = user_input[num][0]
        choice = sceneInstance.user_choice(answer)
        sceneInstance.story_reduce(answer, choice, stg.gui_script)

        assert_equal(stg.current_scene, user_input[num][1])

    ctu.output_divider(test_while_story.__name__, 'FINISH')


def test_valid_user_input():
    ctu.output_divider(test_valid_user_input.__name__, 'START')

    user_input = {
        'BaseStory test (gameStart)': [['oNe', 'bearRoom'], ['ONE', 'bearRoom'], ['   one  ', 'bearRoom'], [' on e ', ''], ['1. ', ''], ['won', ''], ['toast', ''], ['10000', '']],
        'WhileStory test (bearGrills)': [['oNe', 'darkCavern'], ['ONE', 'darkCavern'], ['   one  ', 'darkCavern'], [' on e ', 'bearGrills'], ['1. ', 'bearGrills'], ['won', 'bearGrills'], ['toast', 'bearGrills'], ['10000', 'bearGrills']],
        'CompareStory test (treasureRoom)': [['oNe', ''], ['ONE', ''], ['   one  ', ''], [' on e ', ''], ['1. ', ''], ['won', ''], ['toast', ''], ['10000', '']]
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
            sceneInstance = stg.StoryMap().map[stg.current_scene]
            answer = value[num][0]
            choice = sceneInstance.user_choice(answer)
            sceneInstance.story_reduce(answer, choice, stg.gui_script)

            assert_equal(stg.current_scene, value[num][1])

        ctu.output_divider(key, 'Finished Test')

    ctu.output_divider(test_valid_user_input.__name__, 'FINISH')

"""
Run individual instantiated story files such as default_stg.py
and import the primary stg module as below for each customizable story
"""
from storythegame import stg, stg_util

# Always import stg and initialize the story_path here.
stg.story_path = stg_util.get_file_path("test", "screenplays")

# There will always be a gameStart instance to start the game
gameStart = stg.BaseStory("gameStart")

# gameStart.story_intro()

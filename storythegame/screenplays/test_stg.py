"""
Run individual instantiated story files such as default_stg.py
and import the primary stg module as below for each customizable story
"""
from storythegame import stg

# Always import stg and initialize the story_path here.
# There will always be a gameStart instance to start the game

# TODO: Change this hard-coded path
stg.story_path = "C:\\Users\\Miguel A Mendoza\\Desktop\\practice_code\\python\\projects\\StoryTheGame\\src\\storythegame\\screenplays\\test\\"

gameStart = stg.BaseStory("gameStart")

# gameStart.story_intro()

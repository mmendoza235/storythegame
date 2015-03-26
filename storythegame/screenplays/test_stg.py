"""
Run individual instantiated story files such as default_stg.py
and import the primary stg module as below for each customizable story
"""
import stg

# Always import stg and initialize the story_path here.
# There will always be a gameStart instance to start the game
stg.story_path = "screenplays\\test\\"

gameStart = stg.BaseStory("gameStart")

#gameStart.story_intro()
"""
Run individual instantiated story files such as default_stg.py
and import the primary stg module as below for each customizable story
"""
from storythegame import stg

# Always import stg and initialize the story_path here.
# There will always be a gameStart instance to start the game

# TODO: Change this hard-coded path
stg.story_path = "C:\\Users\\Miguel A Mendoza\\Desktop\\practice_code\\python\\projects\\StoryTheGame\\src\\storythegame\\screenplays\\default\\"

gameStart = stg.BaseStory("gameStart")
bearRoom = stg.BaseStory("bearRoom")
insaneRoom = stg.BaseStory("insaneRoom")
fancyHallway = stg.BaseStory("fancyHallway")
bearGrills = stg.WhileStory("bearGrills")
darkCavern = stg.BaseStory("darkCavern")
strangeLight = stg.BaseStory("strangeLight")
treasureRoom = stg.ComparisonStory("treasureRoom", 10000)
treasureRoom.story_item = 'sword'
unknownDoor = stg.BaseStory("unknownDoor")
trapDoor = stg.BaseStory("trapDoor")

# gameStart.story_intro()

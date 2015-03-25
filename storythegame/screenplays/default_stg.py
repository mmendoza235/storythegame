"""
Run individual instantiated story files such as default_stg.py
and import the primary stg module as below for each customizable story
"""
import stg

# Always import stg and initialize the story_path here.
# There will always be a gameStart instance to start the game
#stg.story_path = "screenplays\\default\\"

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

#gameStart.story_intro()
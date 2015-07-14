Story the Game
==============

Inspired by text based games such as Zork and Adventure, this
project takes these classic storytelling techniques with the
goal to develop an application that allows custom story creation.
By building the framework to parse each scene from text files,
anyone can create their own interactive story experience!

Features
-----------------

* Edit/customize the story on the fly. Immediately play the custom
game based on recent changes or new additions.
* Easy to use editing interface to craft each individual scene.
* Define customized items that can alter the outcome of the story.

How to Play
------------

### Story the game through python shell:

	1. Choose a story module to play from the screenplay folder.
		File format: "story_name_stg.py"
	2. Start the python shell:
		python
	3. Import the desired story module:
		from storythegame.screenplays import default_stg
	4. Run the story_intro() method on the desired scene:
		default_stg.gameStart.story_intro()

### Story the game through the gui:

	1. Run the gui file via the command line.
		python ./stg_gui.py

from stg_util import prompt, keypress
from sys import exit
import random

"""
Global vars in all caps are used to parse the screenplay files
TODO: create GUI to generate/write screenplay files
"""
ONE = "1. "
TWO = "2. "
THREE = "3. "
DOOR_CHOICES = {
	ONE: ['1', '#1', 'one'],
	TWO: ['2', '#2', 'two'],
	THREE: ['3', '#3', 'three'],
	"4. ": ['4', '#4', 'four'],
	"5. ": ['5', '#5', 'five']
}
PROMPT = "PROMPT"
GAMEOVER = "GAMEOVER: "
WINNER = "GG: "
PAUSE = "..."
CONTINUE = "CONTINUE: "
ITEM = "ITEM: "
ELSE = "ELSE: "
STOP = "STOP"
HAS_ITEM = "+++"
NO_ITEM = "---"

# Default story path defined here.
# Override in story_name.py for custom story
story_path = "screenplays\\default\\"

class IterRegistry(type):
	def __iter__(cls):
		return iter(cls._registry)

class BaseStory(object):
	"""
	The base story class for the instantiated room.
	User input logic defaults to a final else statement 
	if the user's input does not match a door choice.
	"""
	__metaclass__ = IterRegistry
	_registry = []
	
	items = []
	story_item = ''
	
	def __init__(self, room_name):
		self._registry.append(self)
		self.room_name = room_name
	
	def import_story(self):
		"""
		Import the screenplay for the specified room.
		File format is as follows: roomName.txt
		Returns list of screenplay lines.
		"""
		script = []
		
		with open(self.file_path()) as f:
		
			for line in f.readlines():
				script.append(line.strip())
		
		return script
	
	def file_path(self):
		path = story_path + self.room_name + '.txt'
		
		return path
	
	def story_intro(self, item = ''):
		"""
		Call this method to initiate the code execution for the specified room.
		Optional item parameter sets the items attribute from the last room.
		"""
		if item:
			self.items.append(item)
		
		script = self.import_story()
		
		for num in range(len(script)):
			if PROMPT in script[num]:
				self.story_prompt(script[num + 1:])
				break
			
			else:
				self.story_print(script[num])
	
	def story_prompt(self, reduced_script):
		"""
		User prompt code
		"""
		answer = prompt()
		choice = self.user_choice(answer)
		self.story_reduce(answer, choice, reduced_script)
	
	def user_choice(self, answer):
		"""
		Parse user input and return relevant dictionary index
		"""
		for key, value in DOOR_CHOICES.iteritems():
			if answer in value:
				return key
		
		# Default to the else scenario for invalid answer.
		return ELSE
	
	def story_indeces(self, choice, script_choices):
		"""
		Returns the start and stop indeces for the selected
		portion of the script.
		The number choice, i.e. '1. ', indicates the start index
		The following 'STOP' keyword indicates the stop index
		"""
		start, stop = "not set", "not set"
		
		# Don't set the stop index unless the start index
		# has been set. False or 0 conflicts with zero index of the list
		for index in range(len(script_choices)):
			if choice in script_choices[index]:
				start = index
			
			elif STOP in script_choices[index] and start != "not set":
				stop = index
				break
			
			else:
				continue
		
		return start, stop
	
	def story_reduce(self, answer, choice, script_choices):
		"""
		Reduce the script lines based on the user's choice
		"""
		start, stop = self.story_indeces(choice, script_choices)
		
		# Default to the else scenario
		# if the user's choice is not available
		if start == "not set":
			choice = ELSE
			start, stop = self.story_indeces(choice, script_choices)
		
		# Remove alternate scenarios
		# Remove choice keyword from text i.e. '1. '
		reduced_script = script_choices[start: stop]
		reduced_script[0] = reduced_script[0][len(choice):]
		
		if self.story_item:
			reduced_script = self.item_script(reduced_script)
		
		self.story_decode(answer, reduced_script)
	
	def item_script(self, reduced_script):
		"""
		Additional script modification in the event a story_item
		is used to alter the outcome of the story
		"""
		try:
			has_item_index = reduced_script.index(HAS_ITEM)
		except ValueError:
			# if HAS_ITEM keyword not present, return unaltered script
			return reduced_script
		
		no_item_index = reduced_script.index(NO_ITEM)
		
		if self.story_item in self.items:
			start, stop = no_item_index, len(reduced_script)
		
		else:
			start, stop = has_item_index, no_item_index
		
		del reduced_script[start:stop+1]
		
		if self.story_item in self.items:
			del reduced_script[has_item_index]
		
		return reduced_script
	
	def story_decode(self, answer, reduced_script):
		"""
		Parse the remaining screenplay based on:
		game over, continue and item scenarios.
		"""
		item = ""
		for line in reduced_script:
			
			if GAMEOVER in line:
				self.game_over(line[len(GAMEOVER):])
			
			elif WINNER in line:
				self.game_over(line[len(WINNER):], False)
			
			elif ITEM in line:
				item = line[len(ITEM):]
			
			elif CONTINUE in line:
				scene_name = line[len(CONTINUE):]
				StoryMap().map[scene_name].story_intro(item)
			
			else:
				self.story_print(line, answer)
	
	def story_print(self, line, answer=''):
		"""
		Modify the print execution based on the presence of:
			%	for formatted variables
			" 	for character dialogue
			... to indicate a user keypress and pause execution
		"""
		if '"' in line and '%' in line:
			# Formatted variable defaults to user input
			print "\t", line % answer
		
		elif '%' in line:
			print line % answer
		
		elif '"' in line:
			print "\t", line
		
		elif PAUSE in line:
			print line
			keypress()
		
		else:
			print line
	
	def game_over(self, reason, death=True):
		"""
		Append custom game over signature.
		"""
		if death:
			print reason, "Game Over!"
			# Stop code execution on game over scenario, stops gui as well
			#exit(0)
		else:
			print reason, "You win!"
	
class WhileStory(BaseStory):
	"""
	Updates the base story class with a modified if/else statement.
	User input continues until a valid choice advances the game.
	Prevents game from ending for an invalid choice.
	"""
	def __init__(self, room_name):
		super(WhileStory, self).__init__(room_name)
	
	def story_reduce(self, answer, choice, script_choices):
		"""
		Modified function to simulate the functionality of a while loop.
		"""
		start, stop = self.story_indeces(choice, script_choices)
		
		if start == "not set":
			choice = ELSE
			start, stop = self.story_indeces(choice, script_choices)
		
		# Remove unnecessary text
		reduced_script = script_choices[start: stop]
		reduced_script[0] = reduced_script[0][len(choice):]
		
		# While loop-like functionality
		if choice == ELSE:
			self.story_decode(answer, reduced_script)
			self.story_prompt(script_choices)
		else:
			self.story_decode(answer, reduced_script)

class ComparisonStory(BaseStory):
	"""
	Updates the base story class with comparison operators.
	compare_num attribute used in user comparison logic.
	"""
	def __init__(self, room_name, compare_num):
		super(ComparisonStory, self).__init__(room_name)
		self.compare_num = random.randint(1, compare_num)
	
	def user_choice(self, answer):
		"""
		Convert the user answer to an integer for comparison operations.
		"""
		try:
			answer = int(answer)
			choice = self.comparison(answer)
			return choice												
		
		except ValueError:
			# Default to else statement if
			# user input is not an integer
			return ELSE
	
	def story_print(self, line, answer=''):
		if '"' in line and '%' in line:
			# story_print overridden to display
			# compare_num's random integer
			print "\t", line % self.compare_num
		
		elif '%' in line:
			print line % self.compare_num
		
		elif '"' in line:
			print "\t", line
		
		elif PAUSE in line:
			print line
			keypress()
		
		else:
			print line
	
	def comparison(self, answer):
		if answer >= self.compare_num:
			choice = ONE
		
		elif answer == 0:
			choice = THREE
		
		elif answer < self.compare_num:
			choice = TWO
		
		else:
			choice = ELSE
		
		return choice

class StoryMap(object):
	"""
	Que taken from finite state machine example. This map class utilizes the
	class iteration registry class (IterRegistry) to map the roomName to
	the object/instance.
	"""
	def __init__(self):
		self.map = {}
		
		for story_object in BaseStory:
			self.map[story_object.room_name] = story_object
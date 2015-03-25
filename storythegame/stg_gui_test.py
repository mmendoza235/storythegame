import Tkinter as tk
import tkMessageBox # In Python 3.x, import tkinter.messagebox
import ttk

import stg
#import default_stg
from screenplays import default_stg

file_name = ''
import_story = "default_stg"

def active_games():
	"""
	Generates a list of the active games based on the presence
	of the story modules that create the screenplay objects.
	"""
	from os import listdir
	from os.path import isfile, join, splitext
	
	screenplay_path = "screenplays\\"
	
	game_list = []
	
	for game_file in listdir(screenplay_path):
		file_path = join(screenplay_path, game_file)
		if isfile(file_path) and game_file.endswith('.py') and not game_file.startswith('__init__'):
			game_list.append(file_path)
	
	print game_list
	
	return game_list

def select_game(game_choice):
	import importlib
	global import_story
	
	try:
		importlib.import_module(game_choice)
	except ImportError:
		print "Failed to import story module"
		return
	
	import_story = game_choice

def about_me():
	tkMessageBox.showinfo("About Me", "This is merely text.\nNo interaction whatsoever.")
	return

def save_script():
	global file_name
	if file_name:
		script_update = aboutRoom.get(1.0, tk.END)
		
		with open(file_name, 'w') as f:
			f.write(script_update)
	status_message('Script saved successfully.')
	return

def story_dict():
	"""
	Builds the dictionary for the screenplay files.
	Dictionary keyed by the roomName with the file path as the value.
	"""
	path_dict = {}
	for story_object in stg.BaseStory:
		path_dict[story_object.room_name] = story_object.file_path()
	
	return path_dict

def open_files(selection):
	global file_name
	file_name = story_dict()[selection]
	with open(file_name) as f:
		aboutRoom.delete(1.0, tk.END)
		script_line = ""
		
		for i in f:
			script_line += i
		
		aboutRoom.insert(tk.END, script_line)
	status_message("File open: " + selection + '.txt')
	return

def status_message(message):
	statusLabel.configure(text=message)
	return

def insert_event(event):
	aboutRoom.insert(tk.INSERT, event)

app = tk.Tk()
app.title("Story the Game")
app.geometry("660x660+50+50")

""" Main Menu """

menubar = tk.Menu(app)
app.config(menu=menubar)

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Start Game", command=default_stg.gameStart.story_intro)
# TODO: selecting game imports appropriate story_name_stg module
file_menu.add_command(label="Select Game", command=lambda: select_game("default_stg"))

file_menu.add_separator()

file_menu.add_command(label="Quit", command=app.quit)
menubar.add_cascade(label="File", menu=file_menu)

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_cascade(label="About Me", command=about_me)
menubar.add_cascade(label="Help", menu=help_menu)

""" Toolbar """
toolbar = tk.Frame(app)

image_tool = ttk.Button(toolbar, text="Check Window Width",
					command=lambda: status_message("Window width: "+str(app.winfo_width())))
image_tool.pack(side='left', padx=2, pady=2)
print_tool = ttk.Button(toolbar, text="Check Width",
					command=lambda: status_message("Event width: "+str(eventFrame.winfo_width())))
print_tool.pack(side='left', padx=2, pady=2)

toolbar.pack(side='top', fill='x')

middle_sep = ttk.Separator(app, orient='horizontal')
""" Edit Screenplay Window """
# Place the text write code before the Tk's mainloop method
#scriptFrame = tk.Frame(app)
scriptWrapper = ttk.Labelframe(app, text='script wrapper')

scriptFrame = ttk.Labelframe(scriptWrapper, text='script frame', width=560)
aboutRoom = tk.Text(scriptFrame)
aboutRoom.insert(tk.END, "Please select a script to view and edit it.")
aboutRoom.pack()
scriptFrame.pack(side='left')

#eventFrame = tk.Frame(app)
eventFrame = ttk.Labelframe(scriptWrapper, text='event frame', width=100)

eventLabel = tk.Label(eventFrame, text='Insert Events:')
eventLabel.pack(pady=5)
promptButt = ttk.Button(eventFrame, text='Prompt User',
						command=lambda: insert_event(stg.PROMPT + '\n'))
promptButt.pack(fill='x', padx=5, pady=5)
choiceButt1 = ttk.Button(eventFrame, text='First Choice',
						command=lambda: insert_event('1. <Type script here>\n<And here.>\n' + stg.STOP))
choiceButt1.pack(fill='x', padx=5, pady=5)
choiceButt2 = ttk.Button(eventFrame, text='Second Choice',
						command=lambda: insert_event('2. <Type script here>\n<And here.>\n' + stg.STOP))
choiceButt2.pack(fill='x', padx=5, pady=5)
choiceButt3 = ttk.Button(eventFrame, text='Third Choice',
						command=lambda: insert_event('3. <Type script here>\n<And here.>\n' + stg.STOP))
choiceButt3.pack(fill='x', padx=5, pady=5)
itemButt = ttk.Button(eventFrame, text='Item Pickup',
						command=lambda: insert_event(stg.ITEM + '<What item? example: egg>'))
itemButt.pack(fill='x', padx=5, pady=5)
gameoverButt = ttk.Button(eventFrame, text='Game Over',
						command=lambda: insert_event(stg.GAMEOVER + '<How does the game end?>'))
gameoverButt.pack(fill='x', padx=5, pady=5)
continueButt = ttk.Button(eventFrame, text='"Correct" Choice',
						command=lambda: insert_event(stg.CONTINUE + '<roomName>'))
continueButt.pack(fill='x', padx=5, pady=5)
elseButt = ttk.Button(eventFrame, text='Invalid Choice',
						command=lambda: insert_event(stg.ELSE + '<Type script here>\n<And here.>\n' + stg.STOP))
elseButt.pack(fill='x', padx=5, pady=5)

eventFrame.pack(side='left')
scriptWrapper.pack()

#scriptControlWrapper = tk.Frame(app)
scriptControlWrapper = ttk.Labelframe(app, text='script control wrapper')
#scriptControlFrame = tk.Frame(scriptControlWrapper)
scriptControlFrame = ttk.Labelframe(scriptControlWrapper, text='script control frame')
scriptControlFrame.pack()
scriptControlWrapper.pack()

bottom_sep = ttk.Separator(app, orient='horizontal')

storyFiles = tk.StringVar()
storyFiles.set(None)
files = story_dict().keys()
story_drop_down = tk.OptionMenu(scriptControlFrame, storyFiles, *files, command=open_files)
story_drop_down.pack(side='left', padx=5, pady=5)

button1 = ttk.Button(scriptControlFrame, text="Save Script", width=20, command=save_script)
button1.pack(side='left', padx=5, pady=5)

""" Status Bar """
statusLabel = tk.Label(app, bd=1, text='Welcome to Story the Game!', relief='sunken', anchor = 'e')
statusLabel.pack(side='bottom', fill='x')
active_games()
app.mainloop()
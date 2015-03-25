import Tkinter as tk
import ttk

import stg
#import default_stg
from screenplays import default_stg

file_name = ''

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)

def story_dict():
		"""
		Builds the dictionary for the screenplay files.
		Dictionary keyed by the roomName with the file path as the value.
		"""
		path_dict = {}
		for story_object in stg.BaseStory:
			path_dict[story_object.room_name] = story_object.file_path()
		
		return path_dict

def popup_message(message):
	popup = tk.Tk()
	popup.wm_title("!")
	
	label = ttk.Label(popup, text=message, font = NORM_FONT)
	label.pack(side="top", fill="x", pady=10)
	
	B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
	B1.pack()
	popup.mainloop()

class StoryTheGameApp(tk.Tk):
	
	def __init__(self, *args, **kwargs):
		
		tk.Tk.__init__(self, *args, **kwargs)
		
		tk.Tk.iconbitmap(self, default="image\\stg.ico")
		tk.Tk.wm_title(self, "Story The Game")
		
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		
		""" Menus """
		menubar = tk.Menu(container)
		
		filemenu = tk.Menu(menubar, tearoff=0)
		filemenu.add_command(label="Play the Game", command=lambda: self.show_frame(PlayGame))
		filemenu.add_command(label="Select Story",
							command=lambda: popup_message("Not supported yet.\nCreate dropdown list of existing stories."))
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=quit)
		menubar.add_cascade(label="File", menu=filemenu)
		
		editmenu = tk.Menu(menubar, tearoff=0)
		editmenu.add_command(label="Edit Existing Story", command=lambda: self.show_frame(StoryEdit))
		editmenu.add_command(label="Create A Story", command=lambda: self.show_frame(NewStory))
		menubar.add_cascade(label="Edit", menu=editmenu)
		
		helpmenu = tk.Menu(menubar, tearoff=0)
		helpmenu.add_command(label="Help", command=lambda: popup_message("Not Supported yet!"))
		helpmenu.add_command(label="Tutorial", command=lambda: popup_message("Not Supported yet!"))
		helpmenu.add_separator()
		helpmenu.add_command(label="About Me", command=lambda: popup_message("The less you know, the better."))
		menubar.add_cascade(label="Help", menu=helpmenu)
		
		tk.Tk.config(self, menu=menubar)
		
		""" Frame Setup! """
		self.frames = {}
		
		for F in (StartPage, PlayGame, StoryEdit, NewStory):
			
			frame = F(container, self)
			
			self.frames[F] = frame
			
			frame.grid(row=0, column=0, sticky="nsew")
		
		self.show_frame(StartPage)
	
	def show_frame(self, cont):
		
		frame = self.frames[cont]
		frame.tkraise()

class StartPage(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		welcome = ttk.Label(self, text="    Welcome to...\nSTORY THE GAME!", font=LARGE_FONT)
		welcome.pack(pady=15)
		
		buttWrapper = tk.Frame(self)
		buttWrapper.pack(fill="x")
		
		button1 = ttk.Button(buttWrapper, text="Enter if you dare...",
							command=lambda: controller.show_frame(PlayGame))	# Throwaway function has issues when returning something
		button1.pack(side="left", fill="x", expand=1)
		
		button2 = ttk.Button(buttWrapper, text="Exit", command=quit)
		button2.pack(side="left", fill="x", expand=1)

class PlayGame(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		""" Story Printing """
		outputFrame = tk.Frame(self)
		outputFrame.pack(fill=tk.BOTH, expand=1)
		
		game_title = tk.Label(outputFrame, text="GAME TITLE HERE")
		game_title.pack()
		
		story_output = tk.Text(outputFrame, height=10)
		story_output.pack(fill=tk.BOTH, expand=1, padx=20, pady=10)
		
		""" User Game Controls """
		inputFrame = tk.Frame(self)
		inputFrame.pack()
		
		storyInput = tk.Text(inputFrame, height=1, width=30)
		storyInput.pack(side="left", padx=30, pady=15)
		
		submitButt = ttk.Button(inputFrame, text="Enter")
		submitButt.pack(side="left")
		
		""" Status Bar """
		statusBar = tk.Label(self, bd=1, text="Play Story the Game at your own risk", relief="sunken", anchor = "e")
		statusBar.pack(side="bottom", fill="x")

class StoryEdit(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		page_title = ttk.Label(self, text="Edit Story Page", font=LARGE_FONT)
		page_title.pack(side="top", pady=15)
		
		textEditFrame = tk.Frame(self)
		textEditFrame.pack(fill=tk.BOTH, expand=1, padx=30, pady=30)
		
		scrollBar = tk.Scrollbar(textEditFrame)
		scrollBar.pack(side="right", fill="y")
		
		self.aboutRoom = tk.Text(textEditFrame, height=10, yscrollcommand=scrollBar.set)
		self.aboutRoom.insert(tk.END, "Please select a script to view and edit it.")
		self.aboutRoom.pack(fill=tk.BOTH, expand=1)
		
		scrollBar.config(command=self.aboutRoom.yview)
		
		commandWrapper = tk.Frame(self)
		commandWrapper.pack()
		
		storyFiles = tk.StringVar()
		storyFiles.set(None)
		files = story_dict().keys()
		storyDropDown = tk.OptionMenu(commandWrapper, storyFiles, *files,
									command=self.open_files)
		storyDropDown.pack(side='left', padx=5, pady=5)
		
		""" Status Bar """
		status_text = "Edit the screenplay for each scene"
		self.statusBar = tk.Label(self, bd=1, text=status_text,
								relief="sunken", anchor = "e")
		# Status bar is copied for each page! TODO: Add it once for all pages!
		self.statusBar.pack(side="bottom", fill="x")
	"""
	TODO: Change these methods to global functions to be used.
	Is it okay to define widgets as a attributes?
	"""
	def save_script(self):
		global file_name
		if file_name:
			script_update = self.aboutRoom.get(1.0, tk.END)
			
			with open(file_name, 'w') as f:
				f.write(script_update)
		self.statusBar.configure(text="Script saved successfully.")
		return

	def open_files(self, selection):
		global file_name
		file_name = story_dict()[selection]
		with open(file_name) as f:
			self.aboutRoom.delete(1.0, tk.END)
			script_line = ""
			
			for i in f:
				script_line += i
			
			self.aboutRoom.insert(tk.END, script_line)
		self.statusBar.configure(text="File open: " + selection + ".txt")
		return

class NewStory(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		page_title = ttk.Label(self, text="New Story Page", font=LARGE_FONT)
		page_title.pack(side="top", pady=15)
		
		b_frame_wrapper = tk.Frame(self)
		#b_frame_wrapper = ttk.Labelframe(self, text="button frame wrapper")
		b_frame_wrapper.pack(side="top")
		
		button1 = ttk.Button(b_frame_wrapper, text="Check Frame Width",
							command=lambda: statusBar.configure(text="Frame width: %r" % self.winfo_width()))
		button1.pack(side="left", padx=20, pady=20)
		
		button2 = ttk.Button(b_frame_wrapper, text="Check Frame Height",
							command=lambda: statusBar.configure(text="Frame height: %r" % self.winfo_height()))
		button2.pack(side="left", padx=20, pady=20)
		
		""" Status Bar """
		statusBar = tk.Label(self, bd=1, text="Create your new story...", relief="sunken", anchor = "e")
		statusBar.pack(side="bottom", fill="x")

app = StoryTheGameApp()
app.geometry("880x540+50+50")
app.minsize(525, 300)
app.mainloop()
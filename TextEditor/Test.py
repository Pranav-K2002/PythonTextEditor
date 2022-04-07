from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from ctypes import windll
from PIL import Image, ImageTk

windll.shcore.SetProcessDpiAwareness(1)

import syntaxHighlighter


# Defining TextEditor Class
class TextEditor:

	# Defining Constructor
	def __init__(self, root):

		textSize = 15
		menuTextSize = 10
		statusbarTextSize = 15

		# Assigning root

		self.root = root

		# Title of the window
		self.root.title("BetterNote")

		# Window Geometry

		height = 1000
		width = 1000
		screenRes = str(height) + "x" + str(width)
		self.root.geometry(screenRes)

		icon = ImageTk.PhotoImage(Image.open('notepad.png'))
		root.iconphoto(False, icon)

		# Initializing filename
		self.filename = None
		self.title = StringVar()
		self.status = StringVar()

		self.titlebar = Label(self.root, textvariable=self.title, font=("times new roman", menuTextSize, "bold"), bd=2,
							  relief=GROOVE)
		self.titlebar.pack(side=TOP, fill=BOTH)
		self.settitle()

		# Creating Statusbar
		self.statusbar = Label(self.root, textvariable=self.status, font=("times new roman", statusbarTextSize, "bold"),
							   bd=2,
							   relief=GROOVE)

		# Creating Menubar
		self.menubar = Menu(self.root, font=("times new roman", menuTextSize, "bold"), activebackground="skyblue")

		# Configuring menubar on root window
		self.root.config(menu=self.menubar)

		# Creating File Menu
		self.filemenu = Menu(self.menubar, font=("times new roman", menuTextSize), activebackground="skyblue",
							 tearoff=0)

		# Adding New file Command
		self.filemenu.add_command(label="New", accelerator="Ctrl+N", command=self.newfile)

		# Adding Open file Command
		self.filemenu.add_command(label="Open", accelerator="Ctrl+O", command=self.openfile)

		# Adding Save File Command
		self.filemenu.add_command(label="Save", accelerator="Ctrl+S", command=self.savefile)

		# Adding Save As file Command
		self.filemenu.add_command(label="Save As", accelerator="Ctrl+A", command=self.saveasfile)

		# Adding Separator
		self.filemenu.add_separator()

		# Adding Exit window Command
		self.filemenu.add_command(label="Exit", accelerator="Ctrl+E", command=self.exit)

		# Cascading filemenu to menubar
		self.menubar.add_cascade(label="File", menu=self.filemenu)

		# Creating Edit Menu
		self.editmenu = Menu(self.menubar, font=("times new roman", menuTextSize), activebackground="skyblue",
							 tearoff=0)

		# Adding Cut text Command
		self.editmenu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut)

		# Adding Copy text Command
		self.editmenu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy)

		# Adding Paste text command
		self.editmenu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste)

		# Adding Seprator
		self.editmenu.add_separator()

		# Adding Undo text Command
		self.editmenu.add_command(label="Undo", accelerator="Ctrl+U", command=self.undo)

		# Cascading editmenu to menubar
		self.menubar.add_cascade(label="Edit", menu=self.editmenu)

		# Creating Help Menu
		self.helpmenu = Menu(self.menubar, font=("times new roman", menuTextSize), activebackground="skyblue",
							 tearoff=0)

		# Adding About Command
		self.helpmenu.add_command(label="About", command=self.infoabout)

		# Cascading helpmenu to menubar
		self.menubar.add_cascade(label="Help", menu=self.helpmenu)

		# Creating Scrollbar
		scrol_y = Scrollbar(self.root, orient=VERTICAL)

		# Creating Text Area
		self.txtarea = Text(self.root, yscrollcommand=scrol_y.set, font=("times new roman", textSize), state="normal",
							relief=GROOVE)

		# Packing scrollbar to root window
		scrol_y.pack(side=RIGHT, fill=Y)

		# Adding Scrollbar to text area
		scrol_y.config(command=self.txtarea.yview)

		# Packing Text Area to root window
		self.txtarea.pack(fill=BOTH, expand=1)

		# Calling shortcuts Function
		self.shortcuts()

	# Defining settitle function
	def settitle(self):
		# Checking if Filename is not None
		if self.filename:
			# Updating Title as filename
			self.title.set(self.filename)
		else:
			# Updating Title as Untitled
			self.title.set("Untitled")

	# Defining New file Function
	def newfile(self, *args):
		# Clearing the Text Area
		self.txtarea.delete("1.0", END)
		# Updating filename as None
		self.filename = None
		# Calling settitle Function
		self.settitle()
		# updating status
		self.status.set("New File Created")

	# Defining Open File Function
	def openfile(self, *args):
		# Exception handling
		try:
			# Asking for file to open
			self.filename = filedialog.askopenfilename(title="Select file", filetypes=(
				("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py")))
			# checking if filename not none
			if self.filename:
				# opening file in readmode
				infile = open(self.filename, "r")
				# Clearing text area
				self.txtarea.delete("1.0", END)
				# Inserting data Line by line into text area
				for line in infile:
					self.txtarea.insert(END, line)
				# Closing the file
				infile.close()
				# Calling Set title
				self.settitle()
				# Updating Status
				self.status.set("Opened Successfully")
		except Exception as e:
			messagebox.showerror("Exception", e)

	# Defining Save File Function
	def savefile(self, *args):
		# Exception handling
		try:
			# checking if filename not none
			if self.filename:
				# Reading the data from text area
				data = self.txtarea.get("1.0", END)
				# opening File in write mode
				outfile = open(self.filename, "w")
				# Writing Data into file
				outfile.write(data)
				# Closing File
				outfile.close()
				# Calling Set title
				self.settitle()
				# Updating Status
				self.status.set("Saved Successfully")
			else:
				self.saveasfile()
		except Exception as e:
			messagebox.showerror("Exception", e)

	# Defining Save As File Function
	def saveasfile(self, *args):
		# Exception handling
		try:
			# Asking for file name and type to save
			untitledfile = filedialog.asksaveasfilename(title="Save file As", defaultextension=".txt",
														initialfile="Untitled.txt", filetypes=(
					("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py")))
			# Reading the data from text area
			data = self.txtarea.get("1.0", END)
			# opening File in write mode
			outfile = open(untitledfile, "w")
			# Writing Data into file
			outfile.write(data)
			# Closing File
			outfile.close()
			# Updating filename as Untitled
			self.filename = untitledfile
			# Calling Set title
			self.settitle()
			# Updating Status
			self.status.set("Saved Successfully")
		except Exception as e:
			messagebox.showerror("Exception", e)

	# Defining Exit Function
	def exit(self, *args):
		op = messagebox.askyesno("WARNING", "Your Unsaved Data May be Lost!!")
		if op > 0:
			self.root.destroy()
		else:
			return

	# Defining Cut Function
	def cut(self, *args):
		self.txtarea.event_generate("<<Cut>>")

	# Defining Copy Function
	def copy(self, *args):
		self.txtarea.event_generate("<<Copy>>")

	# Defining Paste Function
	def paste(self, *args):
		self.txtarea.event_generate("<<Paste>>")

	# Defining Undo Function
	def undo(self, *args):
		# Exception handling
		try:
			# checking if filename not none
			if self.filename:
				# Clearing Text Area
				self.txtarea.delete("1.0", END)
				# opening File in read mode
				infile = open(self.filename, "r")
				# Inserting data Line by line into text area
				for line in infile:
					self.txtarea.insert(END, line)
				# Closing File
				infile.close()
				# Calling Set title
				self.settitle()
				# Updating Status
				self.status.set("Undone Successfully")
			else:
				# Clearing Text Area
				self.txtarea.delete("1.0", END)
				# Updating filename as None
				self.filename = None
				# Calling Set title
				self.settitle()
				# Updating Status
				self.status.set("Undone Successfully")
		except Exception as e:
			messagebox.showerror("Exception", e)

	# Defining About Function
	def infoabout(self):
		messagebox.showinfo("About Text Editor", "A Simple Text Editor\nCreated by Pranav and Hariesh.")

	# Defining shortcuts Function
	def shortcuts(self):
		# Binding Ctrl+n to newfile Function
		self.txtarea.bind("<Control-n>", self.newfile)
		# Binding Ctrl+o to openfile Function
		self.txtarea.bind("<Control-o>", self.openfile)
		# Binding Ctrl+s to savefile Function
		self.txtarea.bind("<Control-s>", self.savefile)
		# Binding Ctrl+a to saveasfile Function
		self.txtarea.bind("<Control-a>", self.saveasfile)
		# Binding Ctrl+e to exit Function
		self.txtarea.bind("<Control-e>", self.exit)
		# Binding Ctrl+x to cut Function
		self.txtarea.bind("<Control-x>", self.cut)
		# Binding Ctrl+c to copy Function
		self.txtarea.bind("<Control-c>", self.copy)
		# Binding Ctrl+v to paste Function
		self.txtarea.bind("<Control-v>", self.paste)
		# Binding Ctrl+u to undo Function
		self.txtarea.bind("<Control-u>", self.undo)


# Creating TK Container
root = Tk()
# Passing Root to TextEditor Class
TextEditor(root)


def hightlight():
	syntaxHighlighter.test()
	root.after(500, hightlight)


# Root Window Looping
hightlight()
root.mainloop()

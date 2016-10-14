#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#	@name		WindowExample.py
#	@author		Glenn Abastillas
#	@version	1.0.0
#	@date		February 29, 2016
#	
#	This class is an example of how to use the Tkinter GUI package to create functioning and interactive windows with Python
""" this is a sandbox for Tkinter
"""
from Tkinter import Frame
from Tkinter import Tk
from Tkinter import Button
from Tkinter import Label
from Tkinter import Entry
from Tkinter import Menu
from Tkinter import Canvas
from Tkinter import Scale

import tkFileDialog

__author__ 		= "Glenn Abastillas"
__copyright__ 	= "Copyright (c) February 29, 2016"
__credits__		= "Glenn Abastillas"

__version__		= "1.0.0"
__maintainer__	= "Glenn Abastillas"
__license__		= "Free"

class WindowExample(Frame):

	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.result = 0
		self.master.title("This is a test")
		self.master.minsize(width = 600, height = 800)
		#self.master.


		self.prompt = Label(self, text = "Enter a number:", anchor = "w", fg = "#984301")
		self.entry  = Entry(self, width = 50, highlightcolor = "red")
		self.submit = Button(self, text = "Submit", command = self.calculate)
		self.exit   = Button(self, text = "Exit", command = parent.destroy, fg = "red")
		self.output = Label(self, text = "")
		self.menu   = Menu(self, title = "Menu test", bg = "black")
		self.canvas = Canvas(self, cursor = "circle", highlightcolor = "blue", bg = "#019bf0")

		self.button1 = Button(self, text = "tast antum", bg = "red", fg = "green", command = self.newWindow, \
								activebackground = "red", activeforeground = "blue", relief = "sunken", cursor = "dot")

		self.newFrame = Frame(self, bg = "green", highlightcolor = "blue")
		self.button2 = Button(self.newFrame, text = "This is a tast")
		self.button2.grid()
		self.scale = Scale(self, from_ = 50, to_ = 60, orient = "horizontal", digits = 3, resolution = 0.25, highlightcolor = "red", command = self.calculate)
		self.scale.pack()
		self.open_file_button = Button(self, text = "Open File", command = self.openFile)

		self.prompt.pack(side = "top", fill = "x")
		self.entry.pack(side = "top", fill = "x")
		self.output.pack(side = "top", fill = "x", expand = True)
		self.submit.pack(side = "right")
		self.exit.pack(side = "left")
		self.button1.pack(fill="x")
		self.newFrame.pack(side="bottom", fill = "x", expand = True)
		self.button2.grid()
		self.canvas.pack()
		self.open_file_button.pack()
		#self.slider.pack()

		#self.tk = Tkinter.Tk()
		#self.tk.withdrow()
		#self.file_path = Tkinter.filedialog.askopenfilename()
		#print("test")
		self.entry.insert(string = "3", index = 0)
		#self.entry.insert(string = "blahblah", index = 3)

	def calculate(self, integer):
		integer = float(integer)
		#try:
		#	i = int(self.entry.get())
		#	self.result = "%s*2=%s" % (i, i*2)
		#except ValueError:
		#	self.result = "Please enter numbers only"
		self.entry.delete(0, len(self.entry.get()))
		self.result = "%s*2=%s" % (integer, integer*2)
		self.entry.insert(0, integer)

		self.output.configure(text=self.result)

	def newWindow(self):
		try:
			r2 = Tk()
			r2.mainloop()
		except ValueError:
			return None

	def openFile(self):
		file_in = tkFileDialog.askopenfilename()
		self.output.configure(text = file_in)

if __name__ == "__main__":
	root = Tk()
	
	w = 800
	h  = 600
	ws = root.winfo_screenheight()
	wh  = root.winfo_screenwidth()
	x = ((ws/2) - (w/2))*6
	y  = ((wh/2) - (h/2))

	print "w: {0}\th: {1}\tws: {2}\twh: {3}\tx: {4}\ty: {5}\t(w/3)*4:".format(w,h,ws,wh,x,y)
	root.geometry("{0}x{1}+{2}+{3}".format(w, h, x, y))

	WindowExample(root).pack(fill = "both", expand = True)
	root.mainloop()

#Tkinter.Frame.__init__()
#tk = Tkinter.Tk()
#tk.withdraw()
#file_path = tkFileDialog.askopenfilename()
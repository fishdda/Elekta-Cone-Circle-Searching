import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation

import tkinter as tk
from tkinter import ttk ## make some changes to Button

import os
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import pydicom as dicom
from matplotlib.patches import Circle
from tkinter import filedialog
import BBfinder as BB
from PIL import ImageTk, Image

LARGE_FONT = ("Verdana",12)

Medium_FONT = ("Verdana",10)

# path ='C:\\Users\\EXTHuaXia\\Desktop\\BBfinder\\Linac.png'
# img = ImageTk.PhotoImage(Image.open(path))


class SeaofBTCapp(tk.Tk):

	## it's the baseline of application
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="elekta.ico")
        tk.Tk.wm_title(self, "BBFinder15mm")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command=lambda: popupmsg("Not supported yet"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text="使用此软件有风险，所有风险请自行承担！！！！\n 这是XXX医院的15mmCone 8mmBB Ball\n",font = LARGE_FONT)
		label.pack(pady = 10,padx = 10)


		button1 = ttk.Button(self,text="Agree",
			command=lambda:controller.show_frame(PageOne))

		button1.pack(pady = 10,padx = 10)

		button2 = ttk.Button(self,text="Disagree",
			command=quit)

		button2.pack(pady = 10,padx = 10)


		# label2 = tk.Label(self,image = img)
		# label2.pack(side = "bottom", fill = "both", expand = "yes")


class PageOne(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text="gantry angles:",font = Medium_FONT)
		label.pack(pady = 5,padx = 10,side = 'top')

		entry = tk.Entry(self,text = "Plase Enter Gantry Angles:",font = Medium_FONT)
		entry.pack(pady = 5,padx = 10,side = 'top')


		button1 = ttk.Button(self,text="Open File",command=self.Open)
		button1.pack(pady = 5,padx = 10,side = 'top')


		button2 = ttk.Button(self,text="Plot",command = self.Plot_Canvas)
		button2.pack(pady = 5,padx = 10,side = 'top')


		button3 = ttk.Button(self,text="Error",command = self.Showtext)
		button3.pack(pady = 5,padx = 10,side = 'top')


	def Open(self):

		self.filename =  filedialog.askopenfilenames(initialdir = "C:/",
	    title = "Select file",filetypes = (("DICOM files","*.dcm"),("HIS files","*.his"),("all files","*.*")))
		print (self.filename)  # tuple

		## Read the image files
		self.img = BB.Read_File(self.filename)

		## Enter information ##
		RS,IR,OR = BB.Enter_Inf()

		## Finding the IsoCenter ##
		test_img,cir_in,cir_out,cir_error = BB.Find_Circles(self.img,IR,OR,RS)

		## Calculation of Modification ##
		self.D,self.SD = BB.Modify_Cal(cir_error)

		## Plot the Image ##
		self.f = BB.Plot(test_img,cir_in,cir_out,cir_error)


	def Showtext(self):

		label = tk.Label(self, text='Dx:{}mm, Dy:{}mm, Dz:{}mm \n SDx:{}mm, SDy:{}mm, SDz:{}mm'.format(self.D[0],
			self.D[1],self.D[2],self.SD[0],self.SD[1],self.SD[2]),font = LARGE_FONT)
		label.place(x=20, y=60)
		#this creates a new label to the GUI
		label.pack() 

	def Plot_Canvas(self):

		
		canvas = FigureCanvasTkAgg(self.f,self)
		canvas.draw()
		canvas.get_tk_widget().pack(side = tk.TOP,fill = tk.BOTH,expand = True)

		toolbar = NavigationToolbar2Tk(canvas, self)
		toolbar.update()
		canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = SeaofBTCapp()
app.geometry("1000x800")
app.mainloop()
from math import *
import numpy as np
from tkinter import *
import random
from tkinter import ttk
import time
from tkinter import messagebox





root = Tk()

root.title("Structural Dynamics Visualizer")
root.geometry("650x500")


################################################################
################################################################
########################## Colors ##############################
################################################################
################################################################

salmonPink = "#febbbb"
lightBlue = "#ddebff"
springGreen = "#00FF7F"



rows = 0
while rows < 100:
	root.rowconfigure(rows,weight=1)
	root.columnconfigure(rows,weight=1)
	rows +=1 

################################################################
################################################################
################# Function Definition Location #################
################################################################
################################################################
def phraseGenerator():
	phrases = ["Salutations, ","Goodmorrow, ","Aloha, ","Welcome, ", "Bonjour, ", "Ahoy, ", "Howdy, ", "Ciao, "]
	name = NameEntry.get()

	return phrases[random.randint(0,len(phrases)-1)] + name


def phraseDisplay():

	name = NameEntry.get()
	if name == '':
		messagebox.showerror("Error","Please input your name.")
	
	else:
		greeting = phraseGenerator()

		FillerLabel = Label(IntroTab,bg = springGreen)
		FillerLabel.grid(row=4,column=0,sticky= "NESW",columnspan = rows)
		FillerLabel = Label(IntroTab,bg = springGreen)
		FillerLabel.grid(row=5,column=0,sticky= "NESW",columnspan = rows)
		FillerLabel = Label(IntroTab,bg = springGreen)
		FillerLabel.grid(row=6,column=0,sticky= "NESW",columnspan = rows)

		greeting_Display = Label(master = IntroTab,text = greeting,justify=LEFT,width=len(greeting),relief = FLAT,state=ACTIVE)
		greeting_Display.grid(row=7,column=0,sticky="NESW")

		introText = "Welcome to my final project for structural dynamics. My goal is to help future students grapple with some of the challenging topics in this course. The primary goal of this application is to help visualize a SDOF structural response according to the user's choice of mass, stiffness, damping, etc. Simply click on the SDOF Visualizer Tab to begin! This program will not track your units, so it is on you to make sure the dimensonality for each entry is appropriate."

		Information = Label(master = IntroTab, text = introText,wraplength = 400)
		Information.grid(row=8,column=0,sticky="NESW")


def retrieveValues():
	Mass = MassEntry.get()
	Stiffness = StiffnessEntry.get()
	Damping = DampingEntry.get()
	InitialDisplacement = InitialDisplacementEntry.get()
	InitialVelocity = InitialVelocityEntry.get()
	MaxTime = TimeEntry.get()
	Force = ForceEntry.get()
	Frequency = FrequencyEntry.get()
	FullArray = [Mass,Stiffness,Damping,InitialDisplacement,InitialVelocity,MaxTime,Force,Frequency]
	for item in FullArray:
		if item == '':
			messagebox.showerror("Error","Please make sure all fields are filled.")
			break;
	return FullArray

def RunVisualizer():
	from scipy.integrate import odeint
	Parameters = retrieveValues()
	Mass = float(Parameters[0])
	Stiffness = float(Parameters[1])
	Damping = float(Parameters[2])
	InitialDisplacement = float(Parameters[3])
	InitialVelocity = float(Parameters[4])
	TimeMax = float(Parameters[5])
	Force = float((Parameters[6]))
	Frequency = float((Parameters[7]))
	time = np.linspace(0,TimeMax,1000)  #time range
	solution = odeint(SDOFModel,[InitialDisplacement,InitialVelocity],time,args=(Mass,Stiffness,Damping,Force,Frequency))
	Displacement=solution[:,0]   #displacement over time
	Visualizer(time,Displacement,Mass,Stiffness)


def SDOFModel(x,time,m,k,c,Force,Frequency):
	freq = (k/m)**0.5
	c = 2*m*freq*c
	u = x[0]     #define u
	dudt = x[1]  #define z
	xdot = [[],[]]

	pt = Force*sin(Frequency*time)

	#write two first order ODEs
	xdot[0] = dudt  #(1) z=u_dot
	xdot[1] = pt/m-c/m*dudt - k/m * u
	return xdot  #returns 2 values at each time t, u and u_dot


def animate(i,time,Displacement):
	import matplotlib.pyplot as plt
	import matplotlib.animation as animation

	#Building Animation
	x0 = max(time)/3
	x1 = max(time)/3+Displacement[i]
	x2 = max(time)/1.5+Displacement[i]
	x3 = max(time)/1.5

	y0 = 0
	y1 = 5
	y2 = 5
	y3 = 0

	X = [x0,x1,x2,x3]
	Y = [y0,y1,y2,y3]

	line[0].set_data(time[:i], Displacement[:i])
	line[1].set_data(X, Y)
	return line
    
# initialization function: plot the background of each frame
def init():
	import matplotlib.pyplot as plt
	import matplotlib.animation as animation
	line[0].set_data([],[])
	line[1].set_data([],[])
	return line

def Visualizer(time,Displacement,Mass,Stiffness):
	import matplotlib.pyplot as plt
	import matplotlib.animation as animation
	Period = 1/((Stiffness/Mass)**0.5 /(2*3.14159))

	global fig,ax1,ax2,line1,line2,line
	fig,(ax1,ax2) = plt.subplots(2,1,sharex=True)
	ax1.set_xlim((0, max(time)))
	ax1.set_ylim(min(Displacement), max(Displacement))
	ax2.set_xlim(0, max(time))
	ax2.set_ylim(0, 10)
	ax2.set_yticks([])
	line1, = ax1.plot([],[],lw=2)
	line2, = ax2.plot([],[],lw=2)
	line = [line1,line2]

	fig.subplots_adjust(hspace=0)
	fig.suptitle("Building Period: {:02.2f} seconds".format(Period))
	ax1.set(ylabel='Displacement')
	ax2.set(xlabel='Time (seconds)')
	
	anim = animation.FuncAnimation(fig, animate, frames=len(time), interval=10, blit=True,fargs = [time,Displacement],repeat=True)

	plt.show()


################################################################
################################################################
################# Create Tabs for each portion #################
################################################################
################################################################

nb = ttk.Notebook(root)
nb.grid(row=0,column = 0,columnspan = rows, rowspan = rows,sticky="NESW")

IntroTab = ttk.Frame(nb)
nb.add(IntroTab,text = "Introduction")

PremadeEarthquake = ttk.Frame(nb)
nb.add(PremadeEarthquake,text = "SDOF Visualizer")


################################################################
################################################################
###################### Introduction Tab ########################
################################################################
################################################################


WelcomeLabel = Label(IntroTab,text = "Welcome to Structural Dynamics",bg = salmonPink)
WelcomeLabel.grid(row=0,column=0,sticky= "NESW",columnspan=rows)

CreatorLabel = Label(IntroTab,text = "Created by Liam Fontes - Spring 2019",bg = lightBlue)
CreatorLabel.grid(row=1,column=0,sticky= "NESW",columnspan=rows)

NameInputLabel = Label(IntroTab,text = "Please input your name:",bg = salmonPink)
NameInputLabel.grid(row=2,column=0,sticky= "NESW")

NameEntry = Entry(IntroTab)
NameEntry.grid(row=2,column=2,sticky= "NESW")

GreetingsGen = Button(IntroTab,text = "Click To Begin!", command = phraseDisplay)
GreetingsGen.grid(row=3,column =0,sticky= "NESW",columnspan = rows)


################################################################
################################################################
################ Custom SDOF Problem Tab #######################
################################################################
################################################################

ribbonText2 = "Building Characterstics"
Header2 = Label(PremadeEarthquake,text = ribbonText2,bg = salmonPink)
Header2.grid(row=0,column=0,sticky= "NESW",columnspan = rows)

StiffnessText = "Building Stiffness:"
Stiffness = Label(PremadeEarthquake,text = StiffnessText,bg = lightBlue,wraplength=250)
Stiffness.grid(row=1,column=0,sticky= "NESW")
StiffnessEntry = Entry(PremadeEarthquake)
StiffnessEntry.grid(row=1,column=1,sticky= "NESW")

BuildingMassText = "Building Mass:"
BuildingMass = Label(PremadeEarthquake,text = BuildingMassText,bg = lightBlue,wraplength=250)
BuildingMass.grid(row=2,column=0,sticky= "NESW")
MassEntry = Entry(PremadeEarthquake)
MassEntry.grid(row=2,column=1,sticky= "NESW")

DampingText = "Viscous Damping Ratio:"
Damping = Label(PremadeEarthquake,text = DampingText,bg = lightBlue,wraplength=250)
Damping.grid(row=3,column=0,sticky= "NESW")
DampingEntry = Entry(PremadeEarthquake)
DampingEntry.grid(row=3,column=1,sticky= "NESW")

InitialDisplacementText = "Initial Displacement:"
InitialDisplacement = Label(PremadeEarthquake,text = InitialDisplacementText,bg = lightBlue,wraplength=250)
InitialDisplacement.grid(row=4,column=0,sticky= "NESW")
InitialDisplacementEntry = Entry(PremadeEarthquake)
InitialDisplacementEntry.grid(row=4,column=1,sticky= "NESW")

InitialVelocityText = "Initial Velocity:"
InitialVelocity = Label(PremadeEarthquake,text = InitialVelocityText,bg = lightBlue,wraplength=250)
InitialVelocity.grid(row=5,column=0,sticky= "NESW")
InitialVelocityEntry = Entry(PremadeEarthquake)
InitialVelocityEntry.grid(row=5,column=1,sticky= "NESW")

TimeText = "Maximum Time:"
TimeLabel = Label(PremadeEarthquake,text = TimeText,bg = lightBlue,wraplength=250)
TimeLabel.grid(row=6,column=0,sticky= "NESW")
TimeEntry = Entry(PremadeEarthquake)
TimeEntry.grid(row=6,column=1,sticky= "NESW")

ribbonText3 = "Periodic Loading"
Header3 = Label(PremadeEarthquake,text = ribbonText3,bg = salmonPink)
Header3.grid(row=7,column=0,sticky= "NESW",columnspan = rows)

ForceText = "Magnitude of Force:"
ForceLabel = Label(PremadeEarthquake,text = ForceText,bg = lightBlue,wraplength=250)
ForceLabel.grid(row=8,column=0,sticky= "NESW")
ForceEntry = Entry(PremadeEarthquake)
ForceEntry.grid(row=8,column=1,sticky= "NESW")

FrequencyText = "Force Frequency (rad/sec):"
FrequencyLabel = Label(PremadeEarthquake,text = FrequencyText,bg = lightBlue,wraplength=250)
FrequencyLabel.grid(row=9,column=0,sticky= "NESW")
FrequencyEntry = Entry(PremadeEarthquake)
FrequencyEntry.grid(row=9,column=1,sticky= "NESW")


AnalysisButton = Button(PremadeEarthquake,text = "Run Visualizer",command=RunVisualizer )
AnalysisButton.grid(row=10,column =0,columnspan=rows,sticky= "NESW")


root.mainloop()
from tkinter import *
import time
def green():
    screen.configure(background = "#00ff00")
def blue():
    screen.configure(background = "#0000ff")
def red():
    screen.configure(background = "#ff0000")

screen = Tk()
screen.minsize(400,400)
screen.configure(background = "#000000")
#logo = PhotoImage(file="C:/Users/162208/Downloads/Spec-RaspberryPi-GIF-256-Transp.gif", format = "gif -index 2")
#w1 = Label(screen, image = logo)
#w1.pack(side=RIGHT)
w = Label(screen,
          fg = "red",
          font = "Jokerman 16 bold",
          text="Hello World")
w.pack()
rbutton = Button(screen,
                fg = "red",
                font = "Jokerman 12 italic",
                text = "Red",
                command = red)
rbutton.pack(side = BOTTOM)
gbutton = Button(screen,
                fg = "green",
                font = "Jokerman 12 italic",
                text = "Green",
                command = green)
gbutton.pack(side = BOTTOM)
bbutton = Button(screen,
                fg = "blue",
                font = "Jokerman 12 italic",
                text = "Blue",
                command = blue)
bbutton.pack(side = BOTTOM)

    
screen.mainloop()


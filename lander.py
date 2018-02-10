# events-example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *
from PIL import ImageTk, Image


# MODEL VIEW CONTROLLER (MVC)
####################################
# MODEL:       the data
# VIEW:        redrawAll and its helper functions
# CONTROLLER:  event-handling functions and their helper functions
####################################


####################################
# customize these functions
####################################

# Initialize the data which will be used to draw on the screen.
def init(data):
    # load data as appropriate
    image = Image.open("llander-ship.gif")
    data.imageWidth, data.imageHeight = image.size
    data.r = data.imageHeight//2
    data.cx = 0
    data.cy = 0
    data.vy = 0
    data.gravity = 1
    data.boost = 4
    data.gameOver = False
    data.color = "cyan"
    data.background = PhotoImage(file = "Starsinthesky.gif")
    data.moon = PhotoImage(file = "moon.gif")
    data.landerPic = PhotoImage(file = "llander-ship.gif")


# These are the CONTROLLERs.
# IMPORTANT: CONTROLLER does *not* draw at all!
# It only modifies data according to the events.
def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if(event.keysym == "Left"): data.cx -= 10
    if(event.keysym == "Right"): data.cx += 10
    if event.char == " ": data.vy -= data.boost

def timerFired(data):
    if(data.cy + 5*data.r > data.height): #bottom of lander hit ground
        data.gameOver = True
        return
    data.vy += data.gravity
    data.cy += data.vy



# This is the VIEW
# IMPORTANT: VIEW does *not* modify data at all!
# It only draws on the canvas.
def redrawAll(canvas, data):
    # draw in canvas
    (cx, cy, r) = (data.cx, data.cy, data.r)
    color = data.color
    #find starry background, perhaps starry night... or just space
    #find landing zone
    #find half moon moon to use as foreground
    canvas.create_image(data.width/2,data.height/2,image = data.background)
    canvas.create_image(data.width/2,3*data.height/2,image = data.moon)
    canvas.create_image(cx, cy, image = data.landerPic)


####################################
####################################
# use the run function as-is
####################################
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    # create the root and the canvas
    root = Tk()
    root.wm_title("Lunar Lander > NASA")
    init(data)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1000, 1000)

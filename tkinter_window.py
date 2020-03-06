import math
from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import Image
from pyscreenshot import grab
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter.font import Font
from pathlib import Path
import img2pdf
import os
import sys

import random

root = Tk()

def motion(event):
    x, y = event.x, event.y

class Window(Frame):
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    global color
    color = DEFAULT_COLOR

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom

    def __init__(self, master=None):

        Frame.__init__(self, master)
        self.master = master

        # Create slideArea inside of Frame
        self.slide = Canvas(self, width=math.ceil(650/900*screenWidth),
                            height=math.ceil(400/600*screenHeight), bg="white", highlightbackground="grey")
        self.slide.place(x=math.ceil(125/900*screenWidth), y=math.ceil(150/600*screenHeight))

        # widget can take all window
        self.pack(fill=BOTH, expand=1)

        # Crate grey banner behind buttons
        self.banner = Canvas(self, width=screenWidth, height=math.ceil(screenHeight/6), bg="grey")
        self.banner.pack(side=TOP)

        # create button, link it to clickExitButton()
        standardHeight = math.ceil(screenHeight / 600)
        standardWidth = math.ceil((5 / 900) * screenWidth)
        exitButton = Button(self, text="Exit", command=self.clickExitButton, height=standardHeight, width=standardWidth)

        # buttons
        saveButton = Button(self, text="Save", command=self.saveScreenShot,height=standardHeight, width=standardWidth)
        loadButton = Button(self, text="Load", height=standardHeight, width=standardWidth)
        colorButton = Button(self, text="Color", command=self.chooseColor, height=standardHeight, width=standardWidth)
        brushButton = Button(self, text="Pen", command=self.paint, height=standardHeight, width=standardWidth)
        latexButton = Button(self, text="LaTex", height=standardHeight, width=standardWidth)
        presentButton = Button(self, text="Present", height=standardHeight, width=math.ceil((12/900) * screenWidth))

        imageButton = Button(self, text="Image", command=self.upload_image, height=standardHeight, width=standardWidth)
        linkButton = Button(self, text="Links", height=standardHeight, width=standardWidth)
        soundButton = Button(self, text="Sound", height=standardHeight, width=math.ceil(6/900 * screenWidth))

        textButton = Button(self, text="Text", command=self.type_text, height=standardHeight, width=standardWidth)
        codeButton = Button(self, text="Code", height=standardHeight, width=standardWidth)
        txtsizeButton = Button(self, text="Text Size", height=standardHeight, width=math.ceil((6/900) * screenWidth))

        newSlide = Button(self, text="New Slide", height=standardHeight, width=math.ceil(17/900*screenWidth))
        numSlide = Button(self, text="Number Slides", height=standardHeight, width=math.ceil(17/900*screenWidth))
        remSlide = Button(self, text="Remove Current Slide", height=standardHeight, width=math.ceil(17/900*screenWidth))

        slideColor = Button(self, text="Set Slide Color",
                            command=self.slide_color, height=standardHeight, width=math.ceil(12/900*screenWidth))

        # text
        font = ["Times New Roman", "Bengali", "Comic Sans MS"]
        self.defFont = StringVar(master)
        self.defFont.set(font[0])  # default value
        fontButton = OptionMenu(self, self.defFont, *font)
        fontButton.place(x=math.ceil(480/900*screenWidth), y=math.ceil(65/600*screenHeight))

        # place buttons
        # button columns
        newSlide.place(x=math.ceil(240/900*screenWidth), y=math.ceil(4/600*screenHeight))
        numSlide.place(x=math.ceil(400/900*screenWidth), y=math.ceil(4/600*screenHeight))
        remSlide.place(x=math.ceil(550/900*screenWidth), y=math.ceil(4/600*screenHeight))

        presentButton.place(x=math.ceil(280/900*screenWidth), y=math.ceil(35/600*screenHeight))
        slideColor.place(x=math.ceil(380/900*screenWidth), y=math.ceil(35/600*screenHeight))
        textButton.place(x=math.ceil(480/900*screenWidth), y=math.ceil(35/600*screenHeight))
        brushButton.place(x=math.ceil(530/900*screenWidth), y=math.ceil(35/600*screenHeight))
        colorButton.place(x=math.ceil(580/900*screenWidth), y=math.ceil(35/600*screenHeight))

        codeButton.place(x=math.ceil(233 / 900 * screenWidth), y=math.ceil(67 / 600 * screenHeight))
        imageButton.place(x=math.ceil(280 / 900 * screenWidth), y=math.ceil(67 / 600 * screenHeight))
        soundButton.place(x=math.ceil(327 / 900 * screenWidth), y=math.ceil(67 / 600 * screenHeight))
        linkButton.place(x=math.ceil(380 / 900 * screenWidth), y=math.ceil(67 / 600 * screenHeight))
        txtsizeButton.place(x=math.ceil(427 / 900 * screenWidth), y=math.ceil(67 / 600 * screenHeight))
        latexButton.place(x=math.ceil(627 / 900 * screenWidth), y=math.ceil(67 / 600 * screenHeight))

        # Top right corner buttons
        exitButton.place(x=math.ceil(850 / 900 * screenWidth), y=math.ceil(4 / 600 * screenHeight))
        saveButton.place(x=math.ceil(800 / 900 * screenWidth), y=math.ceil(4 / 600 * screenHeight))
        loadButton.place(x=math.ceil(850 / 900 * screenWidth), y=math.ceil(35 / 600 * screenHeight))

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.brushButton

    def clickExitButton(self):
        exit()

    def chooseColor(self):
        global color  # set color to global so it updates in other function
        col = askcolor()
        color = col[1]

    def paint(self):
        x = random.randint(0, 600)
        y = random.randint(0, 200)
        self.slide.create_rectangle(x, x+50, y, y+50, fill=color)

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        photo = ImageTk.PhotoImage(file=file_path)
        x = random.randint(0, 600)
        y = random.randint(0, 200)
        self.slide.create_image(x, y, image=photo, anchor=NW)
        img = Label(image=photo)
        img.image = photo  # reference to image

    def type_text(self):
        fontChoice = self.defFont.get()
        print(self.defFont.get())
        global color

        text = Text(root)

        font = Font(family=fontChoice, size=12)

        x = random.randint(0, 600)
        y = random.randint(0, 200)

        self.slide_id = self.slide.create_text(x, y, anchor="nw", font=font, fill=color)

        self.slide.itemconfig(self.slide_id, text="text")

    def slide_color(self):
        global color
        self.slide.configure(bg=color)

        # Update the width height

    def saveScreenShot(self):
        width = 650
        height = 500
        im = grab(bbox=(0, 0, width, height))

        indexPath = Path(__file__).parent / "Screenshots/index.txt"

        # Check to see if the index File exists
        if not Path.exists(indexPath):
            indexFile = open(indexPath, "w")
            indexFile.write(str(1))  # Create Index File
            index = 1
        else:
            indexFile = open(indexPath, "r+")
            index = indexFile.readline()
            index = int(index)
            index = index + 1

            # Update Index File
            indexFile.close()
            indexFile = open(indexPath, "w")
            indexFile.close()
            indexFile = open(indexPath, "r+")
            indexFile.write(str(index))

        # Save Image
        tempString1 = "Screenshots/slide%s.jpeg" % index
        im.save(tempString1, "JPEG")
        imagePath = Path(__file__).parent / tempString1

        # Making PDF
        tempString2 = "PDFs/PDF%s.pdf" % (index)
        pdfPath = Path(__file__).parent / tempString2
        pdfFile = open(pdfPath, "wb")
        savedImage = Image.open(imagePath)
        pdfBytes = img2pdf.convert(savedImage.filename)
        pdfFile.write(pdfBytes)

        # Close all Files
        indexFile.close()
        pdfFile.close()
        savedImage.close()

        # Potential Fix, change grab resolution to accomdate scaled elements
        '''
        img = grab(bbox=(100, 200, 300, 400))
        # to keep the aspect ratio
        w = 300
        h = 400
        maxheight = 600
        maxwidth = 800
        ratio = min(maxwidth/width, maxheight/height)
        # correct image size is not #oldsize * ratio#
        # img.resize(...) returns a resized image and does not effect img unless
        # you assign the return value
        img = img.resize((h * ratio, width * ratio), Image.ANTIALIAS)
        '''

def paint(event):
    global color
    paint_color = color

    #def savePDF(self):



# Set FullScreen
root.attributes("-fullscreen", True)
#root.geometry("900x600")
#screenWidth = 900
#screenHeight = 600

# Save Screen Resolution
screenWidth  = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

app = Window(root)


# set window title
root.wm_title("Slides")
root.bind('<Motion>', paint)
app.configure(background="black")


# show window
root.mainloop()

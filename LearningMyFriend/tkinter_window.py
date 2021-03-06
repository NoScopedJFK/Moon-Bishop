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
import playsound
import _thread
import random

root = Tk()
DEFAULT_COLOR = 'black'
color = DEFAULT_COLOR


def motion(event):
    x, y = event.x, event.y

def soundButtonClick(path):
    try:
        _thread.start_new_thread(soundHelper, (path, ))
    except:
        print("FAILED TO MAKE THREAD SEND HELP")

def soundHelper(filePath):
    playsound.playsound(filePath)

def showxy(event):
    global mousePosX
    global mousePosY
    mousePosX = event.x
    mousePosY = event.y

def openfile():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Open Sound File",
                                          filetypes=(("MP3 Files", "*.mp3"),
                                                     ("WAV Files", "*.wav")))
    return filename

class popupWindow(object):
    def __init__(self, master):
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Type in what you'd like displayed")
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        self.value=self.e.get()
        self.top.destroy()

class Window(Frame):
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    global color, mousePosX, mousePosY
    color = DEFAULT_COLOR

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom

    def __init__(self, master=None):

        Frame.__init__(self, master)
        self.master = master

        global mousePosX, mousePosY
        mousePosX = math.ceil(screenWidth/2)
        mousePosY = math.ceil(screenHeight/2)

        # Create slideArea inside of Frame
        self.slide = Canvas(self, width=math.ceil(650/900*screenWidth),
                            height=math.ceil(400/600*screenHeight), bg="white", highlightbackground="grey")
        self.slide.place(x=math.ceil(125/900*screenWidth), y=math.ceil(150/600*screenHeight))
        self.slide.x = math.ceil(125/900*screenWidth)
        self.slide.y = math.ceil(150/600*screenHeight)
        self.slide.width = math.ceil(650/900*screenWidth)
        self.slide.height = math.ceil(400/600*screenHeight)
        self.slide.update()
        self.slide.id = 0   # Slides Have An ID

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
        presentButton = Button(self, text="Present", command=lambda: self.newWindow(),
                               height=standardHeight, width=math.ceil((12/900) * screenWidth))

        imageButton = Button(self, text="Image", command=self.upload_image, height=standardHeight, width=standardWidth)
        linkButton = Button(self, text="Links", height=standardHeight, width=standardWidth)
        soundButton = Button(self, text="Sound", command=self.playSound, height=standardHeight,
                             width=math.ceil(6/900 * screenWidth))

        textButton = Button(self, text="Text", command=self.type_text, height=standardHeight, width=standardWidth)
        codeButton = Button(self, text="Code", height=standardHeight, width=standardWidth)
        txtsizeButton = Button(self, text="Text Size", height=standardHeight, width=math.ceil((6/900) * screenWidth))

        newSlide = Button(self, text="New Slide", command=self.newSlide, height=standardHeight, width=math.ceil(17/900*screenWidth))
        numSlide = Button(self, text="Number Slides", height=standardHeight, width=math.ceil(17/900*screenWidth))
        remSlide = Button(self, text="Remove Current Slide", command=self.removeSlide, height=standardHeight, width=math.ceil(17/900*screenWidth))

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

        # Create list of sound Buttons inside of This class
        self.soundButtons = list()

        # Create list of Slides inside of This class
        self.slides = list()
        self.slides.append(self.slide)

        # Get mouse Position on Mouse Press
        self.slide.bind('<Button>', showxy)

    def newWindow(self):
        cover = Canvas(self, width=screenWidth, height=screenHeight, bg="grey", highlightbackground="grey")
        cover.place(relx=1.0, rely=1.0, x=0, y=0, anchor="se")
        cover.exitButton = Button(self, text="Exit", command=lambda: self.removeWindow(cover),
                            width=math.ceil(10*800/screenWidth),
                            height=math.ceil(2*600/screenHeight), bg="red")
        cover.exitButton.place(x=0, y=0)
        cover.slides = self.slides
        cover.slide = cover.slides[0]
        # Raise Canvas over Canvas
        Misc.lift(cover.slide)
        cover.nextButton = Button(self, text="Next .>", command=lambda: self.advanceSlide(cover),
                            width=math.ceil(10*800/screenWidth),
                            height=math.ceil(2*600/screenHeight), bg="green")
        cover.nextButton.place(x=screenWidth-40, y=0)

    def advanceSlide(self, cover):
        if cover.slide.id < len(cover.slides)-1:
            id = cover.slide.id
            #cover.slide.destroy()
            cover.slide = cover.slides[id+1]
            Misc.lift(cover.slide)
        else:
            #cover.slide.destroy()
            self.removeWindow(cover)

    def removeWindow(self, cover):
        cover.exitButton.destroy()
        cover.nextButton.destroy()
        cover.destroy()
        Misc.lift(self.slide)

    def newSlide(self):
        # Save Current Slide
        curIndex = self.slide.id

        # Create slideArea inside of Frame
        self.slide = Canvas(self, width=math.ceil(650/900*screenWidth),
                            height=math.ceil(400/600*screenHeight), bg="white", highlightbackground="grey")
        self.slide.place(x=math.ceil(125/900*screenWidth), y=math.ceil(150/600*screenHeight))
        self.slide.x = math.ceil(125/900*screenWidth)
        self.slide.y = math.ceil(150/600*screenHeight)
        self.slide.width = math.ceil(650/900*screenWidth)
        self.slide.height = math.ceil(400/600*screenHeight)
        self.slide.update()
        self.slide.id = curIndex + 1  # newSlide Index

        # We are inserting a Slide
        if curIndex+1 <= len(self.slides)-1:
            self.slides.insert(curIndex+1, self.slide)
            self.shiftListRight(curIndex+1)

        # We are at the End of the Slides List
        else:
            self.slides.append(self.slide)
            self.test()

    def test(self):
        for x in range(0, len(self.slides)):
            print("Index: %s\tslideID: %s" %(x, self.slides[x].id))

    def removeSlide(self):
        # Method Tries to go backwards 1 slide in this self.slides list
        curIndex = self.slide.id

        # Only has 1 Slide
        if (curIndex == 0) and (len(self.slides) == 1):
            self.shiftListLeft(curIndex)
            self.slides.remove(self.slide)
            self.slide.destroy()
            self.slide.id = -1
            self.newSlide()

        # Removing something from inside of the list
        elif curIndex > len(self.slides)-1:
            self.shiftListLeft(curIndex)
            self.test()
            self.slide = self.slides[curIndex]
            self.slides.remove(self.slide)
            self.slide.destroy()
            self.test()
            self.slide.place(x=math.ceil(125 / 900 * screenWidth), y=math.ceil(150 / 600 * screenHeight))


        # Removing last item
        else:
            self.slides.remove(self.slide)
            self.slide.destroy()
            self.slide = self.slides[len(self.slides) - 1]
            self.slide.place(x=math.ceil(125 / 900 * screenWidth), y=math.ceil(150 / 600 * screenHeight))

    def shiftListLeft(self, startIndex):
        for i in range(startIndex, len(self.slides)-1):
            self.slides[i].id = i-1

    def shiftListRight(self, startIndex):
        for i in range(startIndex, len(self.slides)-1):
            self.slides[i].id = i+1

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

        global mousePosX
        global mousePosY
        x = mousePosX
        y = mousePosY

        self.slide.create_image(x, y, image=photo, anchor=NW)
        img = Label(image=photo)
        img.image = photo  # reference to image

    def type_text(self):
        fontChoice = self.defFont.get()
        global color

        self.popup()

        font = Font(family=fontChoice, size=12)

        global mousePosX
        global mousePosY
        x = mousePosX
        y = mousePosY

        self.slide.text = self.slide.create_text(x, y, anchor="nw", font=font, fill=color)
        self.slide.itemconfig(self.slide.text, text=self.entryValue())

    def popup(self):
        self.w = popupWindow(self.master)
        self.master.wait_window(self.w.top)

    def entryValue(self):
        return self.w.value

    def slide_color(self):
        global color
        self.slide.configure(bg=color)

    def playSound(self):
        file = openfile()
        if (file != ''):
            Height = math.ceil(self.slide.winfo_screenheight()/800*3)
            Width = math.ceil(self.slide.winfo_screenwidth()/1280*5)
            button = Button(self.slide, text="Sound", height=Height, width=Width,
                            command=lambda: soundButtonClick(file))
            global mousePosX, mousePosY
            button.place(x=mousePosX, y=mousePosY)
            self.soundButtons.append(button)

    def saveScreenShot(self):
        x = self.slide.x
        y = self.slide.y
        # the 4 here is because of the border the Canvas has
        # PROBLEM
        im = grab(bbox=(self.slide.x, self.slide.y, x+self.slide.width+4, y+self.slide.height+4))

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

# Save Screen Resolution
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

app = Window(root)


# set window title
root.wm_title("Slides")
root.bind('<Motion>', paint)
app.configure(background="black")


# show window
root.mainloop()

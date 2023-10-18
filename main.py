import cv2
import numpy as np
import imutils
import math
import tkinter
from PIL import ImageTk, Image
import cv2
import numpy as np
import imutils
import math

def calc_draw_center(framein):
    frame = cv2.flip(framein, 1)

#------Image pre-processing----------------------------------------------
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,50,255,cv2.THRESH_BINARY_INV)
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)
#-------Find center----------------------------------------
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    if len(cnts)>0:
        c = max(cnts, key=cv2.contourArea)
        ((x,y),radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = ((M["m10"]/M["m00"]), (M["m01"]/M["m00"]))
        cv2.drawContours(frame, cnts, -1, (0,255,0), 3)
    else:
        center = (0,0)
        radius = 0

    return frame,center,radius



def calc_displacement(initial_coordinate, final_coordinate,radius):
    dotDiameter = 0.012192*10 # dot diameter equals to 1cm
    if radius != 0:
        lengthEachPixel = dotDiameter/(radius*2)
    else:
        lengthEachPixel = 0
    displacementPixel = math.sqrt((initial_coordinate[0]-final_coordinate[0])**2+(initial_coordinate[1]-final_coordinate[1])**2)
    displacement = displacementPixel*lengthEachPixel
    
    return displacement
    
##---------------------------------------------------------------------------------------------------------------------------------------
##It sometimes calls an error, but restarting Kernel resolves 
#import tkinter
#from PIL import ImageTk, Image
#import cv2
#import numpy as np
#import imutils
#import math


root = tkinter.Tk()
root.geometry('1024x800')
root.title("High Accuracy Displacement Measurement")
#make a window
app = tkinter.Frame(root)
app.grid()

#make video frame
video_frame = tkinter.Label(app)
video_frame.grid()
video_frame.pack(padx=20,pady=100,side='left')



global onflag, displacement,radius, initial_coordinate, final_coordinate
onflag=2
displacement = 0
raduis= 1
initial_coordinate=[10,30]
final_coordinate = [100,500]


#text1: hello
#text1 = tkinter.Label(root, text="Hello")
#text1.place(x=60,y=20)

#text2: video title
text2 = tkinter.Label(root, text="Video")
text2.place(x=50,y=70)

#text3: show coordinates
text3 = tkinter.Label(root, text = "Click \"Start\" to \nset initial coordinate")
text3.place(x=850,y=130)

#text4: show displacement
text4 = tkinter.Label(root, text="distance = "+str(displacement) + "cm")
text4.place(x=850,y=300)

#takes initial coordinate and start tracking 
def starting():
    global onflag
    onflag = 1
    global initial_coordinate, final_coordinate
    initial_coordinate = final_coordinate
    text5 = tkinter.Label(root, text = "initial coordinate\n[x,y] =  "+str(np.around(initial_coordinate,decimals=4)))
    text5.place(x=850,y=50)
    coordinates_update()
    
    
    
    
def stopping():
    global onflag
    onflag = 0

def coordinates_update():
    global onflag
    global initial_coordinate, final_coordinate, radius
    displacement = calc_displacement(initial_coordinate, final_coordinate,radius)
    if (onflag==1):
        
        text3.configure(text = "current coordinates\n[x,y] " + str(np.around(final_coordinate,decimals=4)))
        text4.configure(text="distance = "+str(np.around(displacement,decimals=4))+"cm")
        text3.after(100, coordinates_update) #change update time for coordinates
    else:
        text3.configure(text = "final coordinates\n[x,y] " + str(np.around(final_coordinate,decimals=4)))
        text4.configure(text="distance = "+str(np.around(displacement,decimals=4))+"cm")

        print(initial_coordinate, final_coordinate)
    
b_start = tkinter.Button(root,text="Start",width=20,height=4,bg="blue",fg="yellow", 
                         command = starting)
b_start.place(x=300,y=20)


b_stop = tkinter.Button(root,text="Stop",width=20,height=4,bg="blue",fg="yellow",
                           command = stopping)
b_stop.place(x=500,y=20)



# Capture from camera
cap = cv2.VideoCapture(1)

# function for video streaming
def video_stream():
    global initial_coordinate
    global final_coordinate
    global radius
    ret, frame = cap.read()
    frame, cent, rad = calc_draw_center(frame)
    final_coordinate = cent
    radius = rad

    
    
#     frame = cv2.resize(frame,(800,600))
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    video_frame.imgtk = imgtk
    video_frame.configure(image=imgtk)
    video_frame.after(100, video_stream) #change the update interval (ms)



video_stream()
root.mainloop()

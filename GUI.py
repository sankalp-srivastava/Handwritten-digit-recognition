import cv2
import numpy as np
from tkinter import *
from PIL import ImageGrab



def clear_widget():
    global cv
    cv.delete('all')

def activate_event(event):
    global lastx, lasty 
    cv.bind('<B1-Motion>', draw_lines)
    lastx, lasty = event.x, event.y
    
def draw_lines(event):
    global lastx, lasty
    x, y = event.x, event.y
    #canvas drawing
    cv.create_line((lastx,lasty,x,y),width=8,fill='black',
                   capstyle=ROUND, smooth=TRUE, splinesteps=12)
    lastx, lasty =x, y
    
def Recognize_Digit():
    global image_number,filename
    image_number = 0
    filename = f'image_{image_number}.png'
    image_number+=1
    ImageGrab.grab(bbox=(15,45,960,775)).save(filename)
    
    

#loading the model
from keras.models import load_model
model = load_model(r'C:\Users\panka\Study\Machine Learning\Digit Recognition GUI\model.h5')
#print("model loaded succesfully")

#create a main window (named as root).
root = Tk()
root.geometry("640x550+0+0")
root.resizable(0,0)
root.title("Handwritten Digit Recognition GUI App")

#Initialize few variables
lastx, lasty = None, None
image_number = 0

#create a canvas for drawing
cv = Canvas(root,width = 640,height=480,bg = 'white')
cv.grid(row=0, column=0, pady=2, sticky=W, columnspan=2)

cv.bind('<Button-1>',activate_event)

#Adding Buttons and Labels
btn_save = Button(text = 'Recognise Digit', command = Recognize_Digit)
btn_save.grid(row=2 , column=0, pady=1, padx=1)
button_clear = Button(text = 'Clear Widget', command = clear_widget)
button_clear.grid(row=2, column=1, pady=1, padx=1)

#mainloop() to run the application
root.mainloop() 

#read the image in color format
image = cv2.imread(filename)
grey = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
ret, th = cv2.threshold(grey.copy(), 75, 255, cv2.THRESH_BINARY_INV)
contours, _ = cv2.findContours(th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

preprocessed_digits = []
for cnt in contours:
    #get bounding box and extract ROI
    x,y,w,h = cv2.boundingRect(cnt)
    #Create rectangle
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),thickness =2)
    digit = th[y:y+h, x:x+w]
    
    # Resizing that digit to (18, 18)
    resized_digit = cv2.resize(digit, (18,18))
    
    # Padding the digit with 5 pixels of black color (zeros) in each side to finally produce the image of (28, 28)
    padded_digit = np.pad(resized_digit, ((5,5),(5,5)), "constant", constant_values=0)
    
    # Adding the preprocessed digit to the list of preprocessed digits
    preprocessed_digits.append(padded_digit)
    prediction = model.predict(padded_digit.reshape(1, 28, 28, 1))  
    
    data = "Prediction = " + str(np.argmax(prediction))
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale =0.5
    color = (255,0,0)
    thickness =1
    cv2.putText(image,data,(x,y-5),font,fontScale,color,thickness)
    
#showing the predicted result in new window
cv2.imshow('image',image)
cv2.waitKey(0)
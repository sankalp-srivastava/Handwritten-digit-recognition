from tkinter import *
import tkinter as tk
from PIL import ImageGrab, Image
import numpy as np
import cv2
import win32gui
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


#loading the model
from keras.models import load_model
model = load_model(r'C:\Users\panka\Study\Machine Learning\Digit Recognition GUI\model.h5')
#print("model loaded succesfully")

def predict_digit(filename):
    
    #resize image to 28x28 pixels
    image = cv2.imread(filename)
    grey = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(grey.copy(), 75, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
        prediction = model.predict(padded_digit.reshape(1, 28, 28, 1))  
    
        data = "Prediction = " + str(np.argmax(prediction))
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale =0.5
        color = (255,0,0)
        thickness =1
        cv2.putText(image,data,(x,y-5),font,fontScale,color,thickness)
    cv2.imwrite('predict.png',image)
    return 'predict.png'

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.lastx = self.lasty = None

        self.x = self.y = 0
        #self.geometry("900x600")
        
        self.data=""

        # Creating elements
        self.canvas = tk.Canvas(self, width=900, height=600, bg = "white")
        #self.label = tk.Label(self, text="Draw and\nclick Recognize", font=("Comic Sans MS", 15))
        self.classify_btn = tk.Button(self, text = "Recognise", command = self.classify_handwriting) 
        self.button_clear = tk.Button(self, text = "Clear", command = self.clear_all)

        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, columnspan=2)
        #self.label.grid(row=0, column=1,pady=2, padx=2)
        #self.label.place(relx = 1.0, rely = 0.5,anchor ='ne')
        self.classify_btn.grid(row=1, column=0, pady=2, padx=2)
        self.button_clear.grid(row=1, column=1, pady=2,)

        #self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<Button-1>", self.activate_event)

    def clear_all(self):
        self.canvas.delete("all")
      

    def classify_handwriting(self):
        #HWND = self.canvas.winfo_id() # get the handle of the canvas
        HWND = self.canvas.winfo_id() # get the handle of the canvas
        rect = win32gui.GetWindowRect(HWND) # get the coordinate of the canvas
        ImageGrab.grab(rect).save('test.png')
        
        file_name= predict_digit("test.png")
        img = mpimg.imread(file_name)
        
        plt.imshow(img,aspect='auto')
        #plt.show()
        #self.label.configure(text= self.data)
    def activate_event(self, event): 
        
        self.canvas.bind('<B1-Motion>', self.draw_lines)
        self.lastx, self.lasty = event.x, event.y

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        
        self.canvas.create_line((self.lastx,self.lasty,self.x,self.y),width=8,fill='black',
                   capstyle=ROUND, smooth=TRUE, splinesteps=12)
        self.lastx, self.lasty =self.x, self.y
        

app = App()
mainloop()

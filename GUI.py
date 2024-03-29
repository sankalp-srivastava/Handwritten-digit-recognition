'''
A GUI Application that lets you draw with your mouse on a canvas and predict
the digits using a Pre-Trained CNN model.
For training the model refer to the IPython notebook

'''
#libraries
import tkinter as tk
import tkinter.filedialog as filedialog
from PIL import ImageGrab ,ImageTk, Image
import numpy as np
import cv2
import win32gui
from keras.models import load_model


# loading the model
model = load_model(r'C:\Users\panka\Study\Machine Learning\Digit Recognition GUI\model.h5')

def predict_digit(filename):

    # opening the image and converting it fit for input in model
    image = cv2.imread(filename)
    grey = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(grey.copy(), 75, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # Create rectangle
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
        digit = th[y:y + h, x:x + w]

        # Resizing that digit to (18, 18)
        resized_digit = cv2.resize(digit, (18, 18))

        # Padding the digit with 5 pixels of black color (zeros) in each side to 
        #finally produce the image of (28, 28)
        padded_digit = np.pad(resized_digit, ((5, 5), (5, 5)), "constant", constant_values=0)

        # sending the padded digit to model and prediciting
        prediction = model.predict(padded_digit.reshape(1, 28, 28, 1))
        #writing prediciton on image
        data = "Pred = " + str(np.argmax(prediction))
        #print(data)
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.5
        color = (0, 0, 0)
        thickness = 1
        cv2.putText(image, data, (x, y - 5), font, fontScale, color, thickness)
    #resizing & saving the final image
    image = cv2.resize(image,(800,600))
    cv2.imwrite('predict.png', image)

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.lastx = self.lasty = None
        self.x = self.y = 0
        #self.geometry("820x690")
        self.resizable(0,0)
        #self.resizable(width = True, height = True)
        self.title("Handwriiten Digit Recognition GUI")


        # Creating elements
        self.canvas = tk.Canvas(self, width=800, height=600, bg="white", borderwidth=5)
        self.classify_btn = tk.Button(self, text="Recognise", command=self.classify_handwriting,
                                      bg='deep sky blue')
        self.classify_btn.config(font=('helvetica', 14, 'bold'))
        self.button_clear = tk.Button(self, text="Clear", command=self.clear_all,
                                      bg='deep sky blue')
        self.button_clear.config(font=('helvetica', 14, 'bold'))
        self.openfile = tk.Button(self, text="Open A File", command=self.open_file,
                                      bg='deep sky blue')
        self.openfile.config(font=('helvetica', 14, 'bold'))


        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2, sticky=tk.W, columnspan=3)
        self.classify_btn.grid(row=1, column=0, pady=2, padx=2,columnspan=2)
        self.button_clear.grid(row=1, column=2, pady=2, padx =2,columnspan =2)
        self.openfile.grid(row=1, column=4, pady=2, padx =2)
        self.canvas.bind("<Button-1>", self.activate_event)
        
        img = Image.open("First.jpg")
        # PhotoImage class is used to add image to widgets, icons etc
        img = ImageTk.PhotoImage(img)
   
        # create a label
        panel = tk.Label(self, image = img)
      
        # set the image as img 
        panel.image = img
        panel.grid(row=0, column=3,columnspan = 3)

    def clear_all(self):
        #clear button
        self.canvas.delete("all")
        #reset the output screen
        img = Image.open("First.jpg")
      
        # PhotoImage class is used to add image to widgets, icons etc
        img = ImageTk.PhotoImage(img)
   
        # create a label
        panel = tk.Label(self, image = img)
      
        # set the image as img 
        panel.image = img
        panel.grid(row=0, column=3,columnspan = 3)
    def open_file(self):
        file_path = filedialog.askopenfilename()
        predict_digit(file_path)
        img = Image.open('predict.png')
        # PhotoImage class is used to add image to widgets, icons etc
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(self, image = img)
        #   set the image as img 
        panel.image = img
        panel.grid(row=0, column=3,columnspan = 3)
         
    def classify_handwriting(self):
        HWND = self.canvas.winfo_id()         # get the handle of the canvas
        rect = win32gui.GetWindowRect(HWND)   # get the coordinate of the canvas
        ImageGrab.grab(rect).save('test.png') # taking ss of canvas

        predict_digit("test.png")  
        # opens the output image
        img = Image.open('predict.png')
        # PhotoImage class is used to add image to widgets, icons etc
        img = ImageTk.PhotoImage(img)
   
        panel = tk.Label(self, image = img)
        #   set the image as img 
        panel.image = img
        panel.grid(row=0, column=3,columnspan = 3)

    def activate_event(self, event):
        self.canvas.bind('<B1-Motion>', self.draw_lines)
        self.lastx, self.lasty = event.x, event.y

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        self.canvas.create_line((self.lastx, self.lasty, self.x, self.y), width=8, fill='black',
                                capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=12)
        self.lastx, self.lasty = self.x, self.y


app = App()
tk.mainloop()

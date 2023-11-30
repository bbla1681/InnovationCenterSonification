import customtkinter
import tkinter
from tkinter import *
from time import sleep
from data_functions import data_to_midi


class Graphic(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        #Window
        self.geometry("400x150")
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.attributes('-fullscreen', True)
        
        self.canvas = customtkinter.CTkCanvas(self)
        self.canvas.grid(column=0, row=0, sticky= E+W+N+S)
        self.canvas.columnconfigure((0,1,2,3,4,5,6,7,8,9), weight= 1)
        self.canvas.rowconfigure((0,1,2,3,4,5,6,7,8,9), weight= 1)

        self.button = customtkinter.CTkButton(self, command= self.click_button)
        self.button.grid(column= 0 , row= 1, sticky= E+W+N+S)

        self.create_colors(10, [1,2,3,4,5])

        #create grid
        #for x in range(0,11):
            #self.canvas.create_line(int(self.winfo_width() * x * .10), 0,int(self.winfo_width() * x * .10), self.winfo_height())
            #self.canvas.create_line(0,int(self.winfo_height()*x * .10), self.winfo_width(), int(self.winfo_height() *x*.10))

    def click_button(self, x=0):
        if x < 10:
            self.canvas.delete("all")
            self.create_graph(x)
            self.after(500, lambda: self.click_button(x + 1))

    def create_graph(self, x):
        for y in range(0,10):   
            self.canvas.create_rectangle(int(self.winfo_width() * x * .10), int(self.winfo_height() * y * .10) , int(self.winfo_width() * (x+1) * .10), int(self.winfo_height() * (y + 1) * .10),
                                          fill= self.create_color(y), outline= "black", tags= "Grid_Column")
    def rgb_to_hex(self, r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))
    
    def create_colors(self, rows , notes):
        gradient_vals = []
        for i in range(len(notes)):
            blue_vals = self.map_value(notes, min(notes), max(notes), 0,255)
        for i in range(blue_vals):
            reversed_vals = []
            for x in range((len(rows)/2)):
                reversed_vals.append(blue_vals[i]*.2*x)
                gradient_vals.append(blue_vals[i]*.2*x)
            gradient_vals.append(reversed(reversed_vals))
            gradient_vals.insert((i * (rows/2)) + rows, blue_vals[i])
            

        for vals in gradient_vals:
            hex_vals = self.rgb_to_hex(0,0, vals)
        
        return hex_vals
    
    def map_value(value, min_value, max_value, min_result, max_result):
     #maps value (or array of values) from one range to another
     result = min_result + (value - min_value)/(max_value - min_value)*(max_result - min_result)
     return result
    



            


    
            

       
            

graphic = Graphic()
graphic.mainloop()
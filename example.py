import customtkinter
import tkinter
from tkinter import *
from time import sleep
import matplotlib.colors
#from data_functions import data_to_midi

#GRAPHIC IS WORKING GRADIENT IS WORKING JUST NEED TO IMPLEMENT INTO MAIN 

class Graphic(customtkinter.CTkFrame):
    def __init__(self, parent):
        customtkinter.CTkFrame.__init__(self,parent)
        #Window
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        
        self.canvas = customtkinter.CTkCanvas(self)
        self.canvas.grid(column=0, row=0, sticky= E+W+N+S)
        self.canvas.columnconfigure((0,1,2,3,4,5,6,7,8,9), weight= 1)
        self.canvas.rowconfigure((0,1,2,3,4,5,6,7,8,9), weight= 1)

        self.button = customtkinter.CTkButton(self, command= self.start_graphic)
        self.button.grid(column= 0 , row= 1, sticky= E+W+N+S)

        self.hex_vals = []

        #create grid
        #for x in range(0,11):
            #self.canvas.create_line(int(self.winfo_width() * x * .10), 0,int(self.winfo_width() * x * .10), self.winfo_height())
            #self.canvas.create_line(0,int(self.winfo_height()*x * .10), self.winfo_width(), int(self.winfo_height() *x*.10))

    def start_graphic(self, notes, bpms_per_column, colors):
        print("Clicked")
        interval = 0
        for i in range(len(notes)):
            for x in range(10):
                interval += bpms_per_column
                self.after(int(interval) , lambda i=i, x=x: self.create_wave(i, x, colors))

    def create_wave(self, i,x,colors):
        self.canvas.delete("all")
        for y in range(0,10):
            index = y+(i*10)
            self.canvas.create_rectangle(int(self.winfo_width() * x * .10), int(self.winfo_height() * y * .10) , int(self.winfo_width() * (x+1) * .10), int(self.winfo_height() * (y + 1) * .10),
                                          fill= colors[index], outline= "black", tags= "Grid_Column")
    def rgb_to_hex(self, r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    def create_colors(self, rows , notes):
        print(notes)
        blue_vals = []
        for i in range(len(notes)):
            blue_val = (int(self.map_value(notes[i], min(notes), max(notes), 20,255)))
            gradient_vals = []
            colors = []
            for i in range((int(rows/2))):
                gradient_vals.append(int(blue_val*(.2*(i+1))))
            for i in range(len(gradient_vals)):
                colors.append(gradient_vals[i])
            for i in range(len(gradient_vals)):
                colors.append(gradient_vals[-i-1])
            for i in range(len(colors)):
                self.hex_vals.append(self.rgb_to_hex(r= 0, g = 0, b = colors[i]))
        return self.hex_vals
    
    def map_value(self,value, min_value, max_value, min_result, max_result):
     #maps value (or array of values) from one range to another
     result = min_result + (value - min_value)/(max_value - min_value)*(max_result - min_result)
     return result

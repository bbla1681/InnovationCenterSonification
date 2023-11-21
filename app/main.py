import tkinter as tk
from tkinter import *
from tkcalendar import Calendar, DateEntry
import customtkinter

date_font = ("Helvetica", 24)
label_font = ("Helvetica", 16)

data_select_options = ["San Fransisco's Waves (Buoy)", "Davis Air Quality (Purple Air Sensor)", "Temperature In Room"]
wave_note_select_options = ["Height of Wave (Recommended)" , "Humidity", "Peak Period of Waves" , "Mean Period of Waves" ,  "Peak Direction of Wave"]
wave_velocity_select_options = ["Mean Period of Waves" , "Height of Wave" , "Humidity", "Peak Period of Waves" , "Peak Direction of Wave"]


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        #Window
        self.geometry("400x150")
        self.rowconfigure((0),weight=1)
        self.columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11),weight=1)

        #Left Frame
        self.leftFrame = customtkinter.CTkFrame(self)
        self.leftFrame.grid(row=0, column = 0 , columnspan= 2, padx= 20, pady= 20, sticky=E+W+N+S)
        self.leftFrame.rowconfigure((0), weight=0)
        self.leftFrame.columnconfigure(0, weight= 1)

        #Left Frame Modules

        #Start Label
        self.startLabel = customtkinter.CTkLabel(self.leftFrame, font = label_font, text="Start:", anchor=W)
        self.startLabel.grid(row=0, column = 0, padx=15,sticky = E+W+N+S)
        #Start Calendar
        self.startDateEntry = DateEntry(self.leftFrame, font=date_font, firstweekday='monday')
        self.startDateEntry.grid(row=1, column = 0 , padx=30, pady = 15, sticky=E+W+N+S)

        #End Label
        self.endLabel = customtkinter.CTkLabel(self.leftFrame, font = label_font, text="End:", anchor=W)
        self.endLabel.grid(row=2, column = 0, padx=15,sticky = E+W+N+S)

        #End Calendar
        self.endDateEntry = DateEntry(self.leftFrame, font=date_font)
        self.endDateEntry.grid(row=3, column = 0 , padx=30, pady=15, sticky= E+W+N+S)

        #Dataset Label
        self.dataLabel = customtkinter.CTkLabel(self.leftFrame, font= label_font, text= "Data:", anchor= W)
        self.dataLabel.grid(row= 4, column = 0, padx=15, pady=0, sticky= E+W+N+S)

        #Dataset Option Menu
        self.dataSelect = customtkinter.CTkOptionMenu(self.leftFrame, values=data_select_options, font= label_font)
        self.dataSelect.grid(row= 5, column = 0, padx=15, pady=10, sticky = E+W+N+S) 

        #Parameters For Music

        #Label For Notes Select
        self.noteLabel = customtkinter.CTkLabel(self.leftFrame, font= label_font, text= "Notes:", anchor= W)
        self.noteLabel.grid(row= 6, column = 0, padx=15, pady=0, sticky= E+W+N+S)

        #Option menu for notw select parameter
        self.noteSelect = customtkinter.CTkOptionMenu(self.leftFrame, values = wave_note_select_options, font = label_font)
        self.noteSelect.grid(row = 7, column= 0, padx= 15, pady=10 , sticky= E+W+N+S)

        #Begin Button
        self.button = customtkinter.CTkButton(self.leftFrame, text="Create Music", font= label_font, command=self.button_callbck)
        self.button.grid(row = 8, column=0, padx=15, pady=20, sticky = E+W)

        #Right Frame 
        self.rightFrame = customtkinter.CTkFrame(self)
        self.rightFrame.grid(row= 0,column = 2, columnspan= 10, padx=20, pady=20, sticky=E+W+N+S)
        self.rightFrame.rowconfigure(0, weight=1)
        self.rightFrame.columnconfigure(0, weight=1)

    def button_callbck(self):
        print("button clicked")

app = App()
app.mainloop()
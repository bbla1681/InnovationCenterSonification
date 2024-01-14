import customtkinter
import tkinter as tk
from tkinter import *

label_font = ("Helvetica", 40)

class Note_Select(customtkinter.CTkFrame,):
    def __init__(self,parent, selected_notes, **kwargs):

        customtkinter.CTkFrame.__init__(self,parent)

        self.notes = ["C","D","E","F","G","A","B"]

        if selected_notes == None:
            self.selected_notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
        else:
            self.selected_notes = selected_notes

        self.octave_start = 2
        self.octave_end = 7

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1,weight=1)
        self.columnconfigure(0, weight=1)

        self.title = customtkinter.CTkLabel(self, text= "Note Select", font=label_font)
        self.title.grid(row=0, column= 0, pady= 30)

        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(row=1,rowspan=12,column=0, sticky = NSEW)
        self.frame.rowconfigure((0,1,2,3,4,5,6),weight=  1)
        self.frame.columnconfigure((0,1,2,3,4),weight=1)

        self.note_checkbox = []

        self.create_checkboxes()
    
    def create_checkboxes(self):
        index = 0
        row = 0
        column = 0
        padx = 5
        pady = 5

        for note in self.notes:
            column = 0
            for octave in range(self.octave_start,self.octave_end):
                note_label = note+str(octave)
                self.note_checkbox.append(customtkinter.CTkCheckBox(self.frame, text= note_label))
                self.note_checkbox[index].grid(row = row, column = column)

                if note_label in self.selected_notes:
                    self.note_checkbox[index].select(1)

                column += 1
                index+=1
            row +=1
            
    def get_notes(self):
        notes_return = []
        for i in range(len(self.note_checkbox)):
            if self.note_checkbox[i].get():
                notes_return.append(self.note_checkbox[i].cget("text"))
        return notes_return
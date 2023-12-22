from tkinter import *
from tkcalendar import DateEntry
import customtkinter
from data_functions import data_to_midi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from audio_visualize import Graphic
import pygame
import os
import pandas as pd
from PIL import Image
from sound_editor import Sound_Editor
from datetime import date
from datetime import timedelta
from scrape_purple_air import scrape_air_data

title_font = ("Helvetica", 32)
date_font = ("Helvetica", 28)
label_font = ("Helvetica", 24)

data_select_options = ["San Fransisco's Waves (Buoy)", "FLC Air Quality (Purple Air Sensor)", "Temperature In Room"]

wave_note_select_options = ["Height of Wave (Recommended)" , "Peak Period of Waves" , "Mean Period of Waves" ,  "Peak Direction of Wave", "Peak Spread of Waves", "Mean Direction", "Mean Directional Spread"]
wave_velocity_select_options = ["Peak Period of Waves (Recommended)" , "Height of Wave" , "Mean Period of Waves" , "Peak Direction of Wave", "Peak Spread of Waves", "Mean Direction", "Mean Directional Spread"]

sensor_option =  ["Outdoor", "Spider Shed"]

outdoor_sensor_options = ["Outdoor Sensor (A)", "Outdoor Sensor (B)"]
spider_sensor_options = ["InnovationCenterPurple - Spider Shed A"]

data_source_dict = {"San Fransisco's Waves (Buoy)": 1 , "FLC Air Quality (Purple Air Sensor)": 2 , "Temperature In Room": 3}


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_default_color_theme("dark-blue")
        
        #Window
        self.geometry("1000x800")
        self.rowconfigure((1,2),weight=1)
        self.rowconfigure(0, weight=0)
        self.columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11),weight=1)

        #Initialize instruments and channels to check if they exist
        #These values will be used to reintiilize the sound editor to the previous state if closed
        self.instruments_vals = [0]
        self.channels = None

        self.hamburger_icon = customtkinter.CTkImage(Image.open("images\open.png"), size= (40,40))
        self.close_icon = customtkinter.CTkImage(Image.open("images\close.png"), size=(40,40))

        self.menu_open = customtkinter.CTkButton(self, width= 30, height=30,image= self.hamburger_icon, anchor=W, text= "", fg_color="transparent", command= self.open_menu)
        self.menu_open.grid(row = 0, column=0, padx= 15, pady = 0, sticky = W)

        #Left Frame
        self.place_left_frame()

        #Right Frame 
        self.place_right_frame()

        #Initializing actions for updating graph so we have an object that we can cancel
        self.graph_action = None

        #Initializing Sound to check if one exists or not
        self.sound_editor = None

        self.controlFrame = customtkinter.CTkFrame(self)
        self.controlFrame.grid(row=2, column = 0 , columnspan= 2, padx= 20 , pady= 10, sticky = E+W+N+S)
        self.controlFrame.rowconfigure(0, weight = 0)
        self.controlFrame.columnconfigure(0, weight=0)

        #self.audio_controls_frame = customtkinter.CTkFrame(self.controlFrame)
        #self.audio_controls_frame.grid(row= 0, column = 0, sticky= E+W+N+S) 

    def start_button_callback(self):
        input_dict = { #Wave Column Convert
                        "Height of Wave (Recommended)": "significantWaveHeight", "Height of Wave":"significantWaveHeight",
                              "Peak Period of Waves (Recommended)":"peakPeriod", "Peak Period of Waves": "peakPeriod" ,
                                "Mean Period of Waves": "meanPeriod" ,"Peak sDirection of Wave": "peakDirection",
                                  "Peak Spread of Waves": "peakDirectionalSpread", "Mean Direction": "meanDirection",
                                    "Mean Directional Spread": "meanDirectionalSpread",
                        #Purple Air Column Convert
                        "Outdoor Sensor (A)": "InnovationCenterPurple FLC - Outdoor A",
                          "Outdoor Sensor (B)": "InnovationCenterPurple FLC - Outdoor B"
                          }
            
        pygame.init()
        #Pause music if playing
        pygame.mixer.music.pause()
        #Select which data to use
        source = data_source_dict[self.dataSelect.get()]
        
        #Grabbing Data from GUI
        note_input = self.noteSelect.get()
        velocity_input = self.velocitySelect.get()

        note_column = input_dict[note_input]
        velocity_column = input_dict[velocity_input]
        bpm = int(self.bpmSlider.get())
        
        #Buoy Data
        if source == 1:
            #Converting The Calander Input into usable date for the API
            start_date = self.startDateEntry.get_date()
            start_date= str(start_date.year)+"-"+str(start_date.month)+"-"+str(start_date.day)
            end_date = self.endDateEntry.get_date()
            end_date= str(end_date.year)+"-"+str(end_date.month)+"-"+str(end_date.day)

            pan_switch = bool(self.panSwitch.get())

            if pan_switch:
                pan_column = "meanDirection"
            else:
                pan_column = False

            df = data_to_midi.get_data(1,100, start_date, end_date)

            data_to_midi.api_to_midi(start_date,end_date,note_column,velocity_column, bpm, pan_switch, self.instruments_vals, pan_column= pan_column) 

        #Air Quality
        elif source == 2:
            #Pan not available for this option
            pan_bool = False
            

            if self.airSensorSelect.get() == sensor_option[0]:
                # 0 = Pulls Outdoor Data
                scrape_air_data(0)
                df = pd.read_csv("purple_data\outdoor.csv")

            elif self.airSensorSelect.get() == sensor_option[1]:
                # 1 = Pulls Spider Shed Data
                scrape_air_data(1)
                df = pd.read_csv("purple_data\spider.csv")

            df=df.drop(df[df[note_column]==0].index)  

            data_to_midi.df_to_midi(df=df,note_column=note_column, velocity_column=velocity_column,bpm=bpm,pan_bool=pan_bool,instruments=self.instruments_vals)  
        
        note_y = df[note_column].values

        self.colors = self.wave_graphic.create_colors(10,note_y)

        pygame.mixer.music.load("gui_to_midi" + '.mid')
        pygame.mixer.music.play()
        
        #cancel if already started
        self.wave_graphic.cancel()
        self.wave_graphic.start_graphic(note_y, ((60000)/bpm)/10, self.colors)

    def bpm_slider_callback(self, event):
        num = self.bpmSlider.get()
        self.bpmSliderNum.delete(0,END)
        self.bpmSliderNum.insert(0,int(num))

    def bpm_input_callback(self, event):
        num = int(self.bpmSliderNum.get())
        if num>180:
            self.bpmSliderNum.config(placeholder_text= num)
        if num:
            self.bpmSlider.set(num)    
    """
    Graph Visualizer
    def update_graph(self,x,y, i):
            plt.ylim([0,.5])

            self.ax.clear() 
            self.ax.plot(x[i:i+3], y[i:i+3])
            self.ax.set_ylim([0, .5])

            self.canvas.draw_idle()  
            self.canvas.flush_events()
    """
    def update_dropdowns(self):
        if data_source_dict[self.dataSelect.get()] == 1:

            self.noteSelect.set(wave_note_select_options[0])
            self.noteSelect.configure(values = wave_note_select_options)

            self.velocitySelect.set(wave_velocity_select_options[0])
            self.velocitySelect.configure(values = wave_velocity_select_options)
        elif data_source_dict[self.dataSelect.get()] == 2:
            if self.airSensorSelect.get() == sensor_option[0]:
                self.noteSelect.set(outdoor_sensor_options[0])
                self.noteSelect.configure(values = outdoor_sensor_options)

                self.velocitySelect.set(outdoor_sensor_options[1])
                self.velocitySelect.configure(values = outdoor_sensor_options)
            elif self.airSensorSelect.get() == sensor_option[1]:
                self.noteSelect.configure(values = spider_sensor_options)
                self.velocitySelect.configure(values = spider_sensor_options)
    def update_air_dropdowns(self,argument):
            if self.airSensorSelect.get() == sensor_option[0]:
                self.noteSelect.set(outdoor_sensor_options[0])
                self.noteSelect.configure(values = outdoor_sensor_options)
                self.velocitySelect.set(outdoor_sensor_options[1])
                self.velocitySelect.configure(values = outdoor_sensor_options)
            elif self.airSensorSelect.get() == sensor_option[1]:
                self.noteSelect.configure(values = spider_sensor_options)
                self.noteSelect.set(spider_sensor_options[0])
                self.velocitySelect.set(spider_sensor_options[0])
                self.velocitySelect.configure(values = spider_sensor_options)

    def open_menu(self):
        self.menu = customtkinter.CTkFrame(self, fg_color="#1f538d")
        self.menu.grid(row=0,column =0, padx=0,pady=0, columnspan= 1, rowspan=3, sticky= NSEW)

        self.menu.rowconfigure((0,1), weight = 0)
        self.menu.rowconfigure((2), weight=1)
        self.menu.columnconfigure(0, weight=1)

        self.menu_close = customtkinter.CTkButton(self, width= 30, height=30,image= self.close_icon, anchor=W, text= "", fg_color="#1f538d", bg_color="#1f538d", command= self.close_menu)
        self.menu_close.grid(row = 0, column=0, padx= 15, pady = 0, sticky = W)
        self.menu_label = customtkinter.CTkLabel(self, font= title_font, text= "M E N U", bg_color="#1f538d")
        self.menu_label.grid( row = 1, column = 0, sticky= N+E+W)

        self.sound_editor_button = customtkinter.CTkButton(self.menu, text="S O U N D  E D I T O R", font = label_font, command=self.open_sound_editor)
        self.sound_editor_button.grid(row= 2, column= 0, sticky= E+W)
    def close_menu(self):
        self.menu.destroy()
        self.menu_close.destroy()
        self.menu_label.destroy()
    
    def open_sound_editor(self):
        if self.instruments_vals != [0]:
            self.sound_editor = Sound_Editor(self, channels= self.channels, instruments= self.instruments_vals)      
        else:
            self.sound_editor = Sound_Editor(self)
        self.sound_editor.rowconfigure((0), weight = 0)
        self.sound_editor.rowconfigure(1, weight=1)
        self.sound_editor.grid(row=0, column=0, rowspan=3, columnspan=12, sticky= NSEW)

        self.sound_editor_close = customtkinter.CTkButton(self, width= 30, height=30,image= self.close_icon, anchor=W, text= "", command= self.exit, fg_color="#292929")
        self.sound_editor_close.grid(row = 0, column=0, padx= 20, pady = 0, sticky = W)

    def exit(self):
        self.instruments_vals = self.sound_editor.get_instruments()
        self.channels = self.sound_editor.get_channel_count()
        self.sound_editor_close.destroy()
        self.sound_editor.destroy()

    def update_left_frame(self, argument):
        source = data_source_dict[self.dataSelect.get()]
        self.leftFrame.destroy()
        if  source == 1:
            self.place_left_frame()
        elif source == 2:
            self.remove_date_entry()

        self.update_dropdowns() 

    def place_left_frame(self):
        
        self.leftFrame = customtkinter.CTkFrame(self)
        self.leftFrame.grid(row=1, column = 0 , columnspan= 2, padx= 20, pady= 10, sticky=W+N+E+S)
        self.leftFrame.columnconfigure((0), weight= 1)
        self.leftFrame.rowconfigure((0,1,2,4,6,8,10,11,12,13),weight=1)

        #Dataset Label
        self.dataLabel = customtkinter.CTkLabel(self.leftFrame, font= label_font, text= "Data:", anchor= W)
        self.dataLabel.grid(row= 0, column = 0, padx=15, pady=5, sticky= E+W+N+S)

        self.dataSelect = customtkinter.CTkOptionMenu(self.leftFrame, values=data_select_options, font= label_font, command=self.update_left_frame)
        self.dataSelect.grid(row= 1, column = 0, columnspan=2, padx=15, pady=10, sticky = E+W+N+S)
        
         
        #Start Calendar
        self.startLabel = customtkinter.CTkLabel(self.leftFrame, font = label_font, text="Start:", anchor=W)
        self.startLabel.grid(row=2, column = 0, padx=15, pady= 5, sticky = E+W+N+S)

        self.startDateEntry = DateEntry(self.leftFrame, font=date_font, color="white")
        self.startDateEntry.grid(row=3, column = 0 ,columnspan=2, padx=30, pady = 15, sticky=E+W+N+S)
        self.startDateEntry.set_date(date.today() - timedelta(days = 1))

        #End Label
        self.endLabel = customtkinter.CTkLabel(self.leftFrame, font = label_font, text="End:", anchor=W)
        self.endLabel.grid(row=4, column = 0, padx=15, pady= 5, sticky = E+W+N+S)

        #End Calendar
        self.endDateEntry = DateEntry(self.leftFrame, font=date_font)
        self.endDateEntry.grid(row=5, column = 0 ,columnspan=2, padx=30, pady=15, sticky= E+W+N+S)

        #Parameters For Music

        #Label for notes
        self.noteLabel = customtkinter.CTkLabel(self.leftFrame, font= label_font, text= "Notes:", anchor= W)
        self.noteLabel.grid(row= 6, column = 0, padx=15, pady=5, sticky= E+W+N+S)

        #Label For Notes Select
        self.noteSelect = customtkinter.CTkOptionMenu(self.leftFrame, values = wave_note_select_options, font = label_font)
        self.noteSelect.grid(row = 7, column= 0,columnspan=2, padx= 15, pady=10 , sticky= E+W+N+S)

        #Label for velocity
        self.velocityLabel= customtkinter.CTkLabel(self.leftFrame, font= label_font, text= "Veloctiy:", anchor= W)
        self.velocityLabel.grid(row=8, column= 0, padx= 15, pady= 5, sticky= E+W+N+S)
        
        #Option menu for velocity select parameter
        self.velocitySelect= customtkinter.CTkOptionMenu(self.leftFrame, values= wave_velocity_select_options, font= label_font)
        self.velocitySelect.grid(row=9, column= 0,columnspan=2, padx= 15, pady=10, sticky= E+W+N+S)     

        #Label for BPM
        self.bpmLabel = customtkinter.CTkLabel(self.leftFrame,font = label_font, text= "BPM:" , anchor= W )
        self.bpmLabel.grid(row= 10, column= 0 , padx =15, pady= 5 , sticky= E+W+N+S)

        #Slider to pick beats
        self.bpmSlider = customtkinter.CTkSlider(self.leftFrame, from_= 30, to= 180, command= self.bpm_slider_callback)
        self.bpmSlider.set(60)
        self.bpmSlider.grid(row=11, column= 0, padx= 10, pady=10 , sticky= E+W+N+S)
        
        self.bpmSliderNum = customtkinter.CTkEntry(self.leftFrame, width= 60,font= label_font, placeholder_text= 60)
        self.bpmSliderNum.bind("<Return>", self.bpm_input_callback)
        self.bpmSliderNum.grid(row=11 , column= 1, padx=15, pady= 10, sticky= E+W+N+S)

        #Pan Switch for selecting if pan is on or off
        
        self.panSwitch = customtkinter.CTkSwitch(self.leftFrame, font= label_font, text= "Directional Audio")
        self.panSwitch.grid(row= 12 , column = 0, padx= 15, pady = 10, sticky= W+N+S)
        #Begin Button
        self.button = customtkinter.CTkButton(self.leftFrame, text="Listen", font= label_font, command=self.start_button_callback)
        self.button.grid(row = 13, column=0,columnspan=2, padx=15, pady=20, sticky = E+W)
    
    def place_right_frame(self):

        self.rightFrame = customtkinter.CTkFrame(self)
        self.rightFrame.grid(row= 1,column = 2, rowspan= 2,columnspan= 10, padx=20, pady=10, sticky=E+W+N+S)
        self.rightFrame.rowconfigure(0, weight=1)
        self.rightFrame.columnconfigure(0, weight=1)

        #Wave Graphic      

        self.wave_graphic = Graphic(self.rightFrame)
        self.wave_graphic.grid(row=0, column = 0, sticky= E+W+N+S)
        self.wave_graphic.canvas.configure(background="#292929", highlightthickness=0, relief="ridge")
        
        #Graph
        '''
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.rightFrame)
        self.canvas.get_tk_widget().grid(row=1, column=0, padx=20, pady=20, sticky=E + W + N + S)
        '''
    
    def remove_date_entry(self):
        
        self.leftFrame = customtkinter.CTkFrame(self)
        self.leftFrame.grid(row=1, column = 0 , columnspan= 2, padx= 20, pady= 10, sticky=W+N+E+S)
        self.leftFrame.columnconfigure((0), weight= 1)
        self.leftFrame.rowconfigure((0,1,2,4,6,8,10,11,12,13),weight=1)

        self.dataLabel = customtkinter.CTkLabel(self.leftFrame, font= label_font, text= "Data:", anchor= W)
        self.dataLabel.grid(row= 0, column = 0, padx=15, pady=0, sticky= E+W+N+S)

        self.dataSelect = customtkinter.CTkOptionMenu(self.leftFrame, values=data_select_options, font= label_font, command=self.update_left_frame)
        self.dataSelect.grid(row= 1, column = 0, columnspan=2, padx=15, pady=10, sticky = E+W+N+S)

        self.dataSelect.set(data_select_options[1])

        self.airSensorLabel = customtkinter.CTkLabel(self.leftFrame, font= label_font, text="Sensor:", anchor=W)
        self.airSensorLabel.grid(row= 2, column= 0, padx=15, pady=0, sticky= E+W+N+S)

        self.airSensorSelect = customtkinter.CTkOptionMenu(self.leftFrame, values=sensor_option, font= label_font, command=self.update_air_dropdowns)
        self.airSensorSelect.grid(row=3, column= 0,  columnspan= 2, padx=15, pady = 15, sticky= E+W+N+S )

        self.noteLabel = customtkinter.CTkLabel(self.leftFrame, font= label_font, text= "Notes:", anchor= W)
        self.noteLabel.grid(row= 4, column = 0, padx=15, pady=0, sticky= E+W+N+S)

        #Label For Notes Select
        self.noteSelect = customtkinter.CTkOptionMenu(self.leftFrame, font = label_font)
        self.noteSelect.grid(row = 5, column= 0,columnspan=2, padx= 15, pady=10 , sticky= E+W+N+S)

        #Label for velocity
        self.velocityLabel= customtkinter.CTkLabel(self.leftFrame, font= label_font, text= "Veloctiy:", anchor= W)
        self.velocityLabel.grid(row=6, column= 0, padx= 15, pady= 0, sticky= E+W+N+S)
        
        #Option menu for velocity select parameter
        self.velocitySelect= customtkinter.CTkOptionMenu(self.leftFrame, font= label_font)
        self.velocitySelect.grid(row=7, column= 0,columnspan=2, padx= 15, pady=10, sticky= E+W+N+S)     

        #Label for BPM
        self.bpmLabel = customtkinter.CTkLabel(self.leftFrame,font = label_font, text= "BPM:" , anchor= W )
        self.bpmLabel.grid(row= 8, column= 0 , padx =15, pady= 0 , sticky= E+W+N+S)

        #Slider to pick beats
        self.bpmSlider = customtkinter.CTkSlider(self.leftFrame, from_= 30, to= 180, command= self.bpm_slider_callback)
        self.bpmSlider.set(60)
        self.bpmSlider.grid(row=9, column= 0, padx= 10, pady=10 , sticky= E+W+N+S)
        
        self.bpmSliderNum = customtkinter.CTkEntry(self.leftFrame, width= 60,font= label_font, placeholder_text= 60)
        self.bpmSliderNum.bind("<Return>", self.bpm_input_callback)
        self.bpmSliderNum.grid(row=9 , column= 1, padx=15, pady= 10, sticky= E+W+N+S)

        #Begin Button
        self.button = customtkinter.CTkButton(self.leftFrame, text="Listen", font= label_font, command=self.start_button_callback)
        self.button.grid(row = 11, column=0,columnspan=2, padx=15, pady=20, sticky = E+W)

        

app = App()
app.mainloop()
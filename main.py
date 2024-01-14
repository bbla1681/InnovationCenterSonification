from tkinter import *
from tkcalendar import DateEntry
import customtkinter
from data_functions import data_to_midi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from audio_visualize import Graphic
import pygame
import pygame.midi
import pandas as pd
from PIL import Image
from sound_editor import Sound_Editor
from datetime import date
from datetime import timedelta
from scrape_purple_air import scrape_air_data
from note_selector import Note_Select
import numpy as np
from tkinter import messagebox


title_font = ("Helvetica", 32)
date_font = ("Helvetica", 28)
label_font = ("Helvetica", 24)
small_label_font = ("Helvetica", 18)

data_select_options = ["San Fransisco's Waves (Buoy)", "FLC Air Quality (Purple Air Sensor)", "All"]

wave_note_select_options = ["Height of Wave (Recommended)" , "Peak Period of Waves" , "Mean Period of Waves" ,  "Peak Direction of Wave", "Peak Spread of Waves", "Mean Direction", "Mean Directional Spread"]
wave_velocity_select_options = ["Peak Period of Waves (Recommended)" , "Height of Wave" , "Mean Period of Waves" , "Peak Direction of Wave", "Peak Spread of Waves", "Mean Direction", "Mean Directional Spread"]

sensor_option =  ["Outdoor", "Spider Shed"]

outdoor_sensor_options = ["Outdoor Sensor (A)", "Outdoor Sensor (B)"]
spider_sensor_options = ["Innovation Center Spider Shed"]

purple_data_path = r"C:\Users\bbla1\InnovationCenter\Sonification\InnovationCenterSonification\purple_data\\"      

input_dict = { #Wave Column Convert
                        "Height of Wave (Recommended)": "significantWaveHeight", "Height of Wave":"significantWaveHeight",
                              "Peak Period of Waves (Recommended)":"peakPeriod", "Peak Period of Waves": "peakPeriod" ,
                                "Mean Period of Waves": "meanPeriod" ,"Peak sDirection of Wave": "peakDirection",
                                  "Peak Spread of Waves": "peakDirectionalSpread", "Mean Direction": "meanDirection",
                                    "Mean Directional Spread": "meanDirectionalSpread",
                        #Purple Air Column Convert
                        "Outdoor Sensor (A)": "InnovationCenterPurple FLC - Outdoor A",
                          "Outdoor Sensor (B)": "InnovationCenterPurple FLC - Outdoor B",
                            "Innovation Center Spider Shed": "InnovationCenterPurple - Spider Shed A"
                          }

data_source_dict = {"San Fransisco's Waves (Buoy)": 1 , "FLC Air Quality (Purple Air Sensor)": 2 , "All": 3}

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_default_color_theme("dark-blue")
        self.title("Innovation Sonifier")
        #Window
        self.geometry("1000x800")
        # changed to cover control panel area. self.rowconfigure((1,2),weight=1)
        self.rowconfigure((1),weight=1)
        self.rowconfigure(0, weight=0)
        self.columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11),weight=1)

        #Initialize instruments and channels to check if they exist
        #These values will be used to reintiilize the sound editor to the previous state if closed
        self.instruments_vals = [0]
        self.instrument_assignment = [0]
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

        #Initializing Note Selector
        self.note_selector = None
        self.notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
        '''
        self.controlFrame = customtkinter.CTkFrame(self)
        self.controlFrame.grid(row=2, column = 0 , columnspan= 2, padx= 20 , pady= 10, sticky = E+W+N+S)
        self.controlFrame.rowconfigure(0, weight = 0)
        self.controlFrame.columnconfigure(0, weight=0)
        '''

        #self.audio_controls_frame = customtkinter.CTkFrame(self.controlFrame)
        #self.audio_controls_frame.grid(row= 0, column = 0, sticky= E+W+N+S) 

    def start_program(self):
        # mixer config
        freq = 44100  # audio CD quality
        bitsize = -16   # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 1024   # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)
        
        #Pause music if playing
        pygame.mixer.music.pause()

        if not self.check_errors():
            #Select which data to use
            self.source = data_source_dict[self.dataSelect.get()]
            bpm = int(self.bpmSlider.get())
            
            #Buoy Data
            if self.source == 1:
                #Converting The Calander Input into usable date for the API
                        #Grabbing Data from GUI
                dataset = "wave"
                note_input = self.waveNoteSelect.get()
                velocity_input = self.waveVelocitySelect.get()

                note_column = input_dict[note_input]
                velocity_column = input_dict[velocity_input]

                self.start_date = self.startDateEntry.get_date()
                self.start_date= str(self.start_date.year)+"-"+str(self.start_date.month)+"-"+str(self.start_date.day)
                self.end_date = self.endDateEntry.get_date()
                self.end_date= str(self.end_date.year)+"-"+str(self.end_date.month)+"-"+str(self.end_date.day)

                pan_switch = bool(self.panSwitch.get())

                if pan_switch:
                    pan_column = "meanDirection"
                else:
                    pan_column = False

                df = data_to_midi.get_data(1, self.start_date, self.end_date)

                data_to_midi.api_to_midi(self.notes,self.start_date,self.end_date,note_column,velocity_column, bpm, pan_switch, self.instruments_vals, pan_column= pan_column, instrument_assignment=self.instrument_assignment, dataset= dataset) 

            #Air Quality
            elif self.source == 2:
                dataset = "air"
                #Pan not available for this option
                pan_bool = False 

                note_input = self.purpleNoteSelect.get()
                velocity_input = self.purpleVelocitySelect.get()

                note_column = input_dict[note_input]
                velocity_column = input_dict[velocity_input]         

                if self.airSensorSelect.get() == sensor_option[0]:
                    # 0 = Pulls Outdoor Data
                    scrape_air_data(path=purple_data_path, sensor=0)
                    df = pd.read_csv("purple_data\outdoor.csv")

                elif self.airSensorSelect.get() == sensor_option[1]:
                    # 1 = Pulls Spider Shed Data
                    scrape_air_data(path=purple_data_path, sensor=1)
                    df = pd.read_csv("purple_data\spider.csv")

                df=df.drop(df[df[note_column]==0].index)  

                data_to_midi.df_to_midi(df=df,notes= self.notes,note_column=note_column, velocity_column=velocity_column,bpm=bpm,pan_bool=pan_bool,instruments=self.instruments_vals, instrument_assignment= self.instrument_assignment, dataset=dataset)  
            #Use both sources for music
            elif self.source == 3:
                dataset = "all"
                #Grabs Purple Air Data first
                purple_note_input = self.purpleNoteSelect.get()
                purple_velocity_input = self.purpleVelocitySelect.get()

                purple_note_column = input_dict[purple_note_input]
                purple_velocity_column = input_dict[purple_velocity_input]

                if self.airSensorSelect.get() == sensor_option[0]:
                    # 0 = Pulls Outdoor Data
                    scrape_air_data(purple_data_path,0)
                    purple_df = pd.read_csv("purple_data\outdoor.csv")

                elif self.airSensorSelect.get() == sensor_option[1]:
                    # 1 = Pulls Spider Shed Data
                    scrape_air_data(purple_data_path,1)
                    purple_df = pd.read_csv("purple_data\spider.csv")

                purple_df=purple_df.drop(purple_df[purple_df[purple_note_column]==0].index)

                #Grabs Wave Data Next
                wave_note_input = self.waveNoteSelect.get()
                wave_velocity_input = self.waveVelocitySelect.get()

                wave_note_column = input_dict[wave_note_input]
                wave_velocity_column = input_dict[wave_velocity_input]

                self.start_date = self.startDateEntry.get_date()
                self.start_date= str(self.start_date.year)+"-"+str(self.start_date.month)+"-"+str(self.start_date.day)
                self.end_date = self.endDateEntry.get_date()
                self.end_date= str(self.end_date.year)+"-"+str(self.end_date.month)+"-"+str(self.end_date.day)

                pan_switch = bool(self.panSwitch.get())

                wave_df = data_to_midi.get_data(1,100, self.start_date, self.end_date)

                #normalize each dataset before combination
                wave_df[wave_note_column] = wave_df[wave_note_column].apply(lambda x: data_to_midi.map_value(x, min(wave_df[wave_note_column]), max(wave_df[wave_note_column]), 0,1))
                wave_df[wave_velocity_column] = wave_df[wave_velocity_column].apply(lambda x: data_to_midi.map_value(x, min(wave_df[wave_note_column]), max(wave_df[wave_note_column]), 0,1))
                purple_df[purple_note_column] = purple_df[purple_note_column].apply(lambda x: data_to_midi.map_value(x, min(purple_df[purple_note_column]), max(purple_df[purple_note_column]), 0 , 1))
                purple_df[purple_velocity_column] = purple_df[purple_velocity_column].apply(lambda x: data_to_midi.map_value(x, min(purple_df[purple_note_column]), max(purple_df[purple_note_column]), 0 , 1))

                df = pd.DataFrame()
                note_column = "note"
                velocity_column = "velocity"

                if len(purple_df[purple_note_column]) > len(wave_df[wave_note_column]):
                    df[note_column] = np.append(purple_df[purple_note_column].values, self.duplicate_until_size(wave_df[wave_note_column].values, len(purple_df[purple_note_column])))
                    df[velocity_column] = np.append(purple_df[purple_velocity_column].values, self.duplicate_until_size(wave_df[wave_velocity_column].values, len(purple_df[purple_velocity_column])))

                    if pan_switch:
                        pan_column = "meanDirection"
                        pan_values = self.duplicate_until_size(wave_df[pan_column].values, len(df[note_column]))
                        df[pan_column] = pan_values
                    else:
                        pan_column = False

                else:
                    df[note_column] = np.append(wave_df[wave_note_column], self.duplicate_until_size(purple_df[purple_note_column].values, len(wave_df[wave_note_column])))
                    df[velocity_column] = np.append(wave_df[wave_velocity_column], self.duplicate_until_size(purple_df[purple_velocity_column].values, len(wave_df[wave_velocity_column])))

                    if pan_switch:          
                        # Ensure size matches df
                        pan_column = "meanDirection"
                        pan_values = wave_df[pan_column]
                        df[pan_column] = pan_values
                    else:
                        pan_column = False

                data_to_midi.df_to_midi(df,self.notes,note_column,velocity_column, bpm, pan_switch, self.instruments_vals, pan_column= pan_column, instrument_assignment=self.instrument_assignment, dataset= dataset)          

            note_y = df[note_column].values

            print(len(note_y))

            self.colors = self.wave_graphic.create_colors(10,note_y)

            pygame.mixer.music.load("gui_to_midi.mid")
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

            self.waveNoteSelect.set(wave_note_select_options[0])
            self.waveNoteSelect.configure(values = wave_note_select_options)

            self.waveVelocitySelect.set(wave_velocity_select_options[0])
            self.waveVelocitySelect.configure(values = wave_velocity_select_options)
        elif data_source_dict[self.dataSelect.get()] == 2:
            if self.airSensorSelect.get() == sensor_option[0]:

                self.purpleNoteSelect.set(outdoor_sensor_options[0])
                self.purpleNoteSelect.configure(values = outdoor_sensor_options)

                self.purpleVelocitySelect.set(outdoor_sensor_options[1])
                self.purpleVelocitySelect.configure(values = outdoor_sensor_options)

            elif self.airSensorSelect.get() == sensor_option[1]:

                self.purpleNoteSelect.configure(values = spider_sensor_options)
                self.purpleVelocitySelect.configure(values = spider_sensor_options)

    def update_air_dropdowns(self,argument):
            if self.airSensorSelect.get() == sensor_option[0]:

                self.purpleNoteSelect.set(outdoor_sensor_options[0])
                self.purpleNoteSelect.configure(values = outdoor_sensor_options)

                self.purpleVelocitySelect.set(outdoor_sensor_options[1])
                self.purpleVelocitySelect.configure(values = outdoor_sensor_options)

            elif self.airSensorSelect.get() == sensor_option[1]:
                self.purpleNoteSelect.set(spider_sensor_options[0])
                self.purpleNoteSelect.configure(values = spider_sensor_options)
                
                
                self.purpleVelocitySelect.set(spider_sensor_options[0])
                self.purpleVelocitySelect.configure(values = spider_sensor_options)

    def open_menu(self):
        self.menu = customtkinter.CTkFrame(self, fg_color="#1f538d")
        self.menu.grid(row=0,column =0, padx=0,pady=0, columnspan= 1, rowspan=3, sticky= NSEW)

        self.menu.rowconfigure((0,1), weight = 0)
        self.menu.rowconfigure((2,3), weight=1)
        self.menu.columnconfigure(0, weight=1)

        self.menu_close = customtkinter.CTkButton(self, width= 30, height=30,image= self.close_icon, anchor=W, text= "", fg_color="#1f538d", bg_color="#1f538d", command= self.close_menu)
        self.menu_close.grid(row = 0, column=0, padx= 15, pady = 0, sticky = W)

        self.menu_label = customtkinter.CTkLabel(self, font= title_font, text= "M E N U", bg_color="#1f538d")
        self.menu_label.grid( row = 1, column = 0, sticky= N+E+W)

        self.sound_editor_button = customtkinter.CTkButton(self.menu, text="S O U N D  E D I T O R", font = label_font, command=self.open_sound_editor)
        self.sound_editor_button.grid(row= 2, column= 0, sticky= E+W)

        self.sound_editor_button = customtkinter.CTkButton(self.menu, text="N O T E  S E L E C T O R", font = label_font, command=self.open_note_selector)
        self.sound_editor_button.grid(row= 3, column= 0, sticky= N+E+W)

    def close_menu(self):
        self.menu.destroy()
        self.menu_close.destroy()
        self.menu_label.destroy()
    
    def open_sound_editor(self):
        if self.instruments_vals != [0]:
            self.sound_editor = Sound_Editor(self, channels= self.channels, instruments = self.instruments_vals, instrument_assignment = self.instrument_assignment)      
        else:
            self.sound_editor = Sound_Editor(self)
        self.sound_editor.rowconfigure((0), weight = 0)
        self.sound_editor.rowconfigure(1, weight=1)
        self.sound_editor.grid(row=0, column=0, rowspan=3, columnspan=12, sticky= NSEW)

        self.sound_editor_close = customtkinter.CTkButton(self, width= 30, height=30,image= self.close_icon, anchor=W, text= "", command= self.exit_sound_editor, fg_color="#292929")
        self.sound_editor_close.grid(row = 0, column=0, padx= 20, pady = 0, sticky = W)

    #create note selector
    def open_note_selector(self):

        self.note_select = Note_Select(self, selected_notes=self.notes)
        self.note_select.grid(row=0, column=0, rowspan=3, columnspan=12, sticky= NSEW)
        self.note_select.rowconfigure((0), weight = 0)
        self.note_select.rowconfigure(1, weight=1)
        

        self.note_select_close = customtkinter.CTkButton(self, width= 30, height=30,image= self.close_icon, anchor=W, text= "", command= self.exit_note_select, fg_color="#292929")
        self.note_select_close.grid(row = 0, column=0, padx= 20, pady = 0, sticky = W)

    def exit_sound_editor(self):
        #0 index returns instrument midi values, 1 returns array of assignments to which dataset the instrument will be assigned to
        self.instruments_vals = self.sound_editor.get_instruments()[0]
        self.instrument_assignment = self.sound_editor.get_instruments()[1]
        self.channels = self.sound_editor.get_channel_count()
        self.sound_editor_close.destroy()
        self.sound_editor.destroy()
    
    def exit_note_select(self):
        self.notes = self.note_select.get_notes()
        self.note_select_close.destroy()
        self.note_select.destroy()
        
    def update_left_frame(self, argument):
        source = data_source_dict[self.dataSelect.get()]
        self.leftFrame.destroy()
        if  source == 1:
            self.place_left_frame()
        elif source == 2:
            self.purple_left_frame_update()
        elif source == 3:
            self.all_source_left_frame_update()

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
        self.startDateEntry.grid(row=3, column = 0 ,columnspan=2, padx=15, pady = 15, sticky=E+W+N+S)
        self.startDateEntry.set_date(date.today() - timedelta(days = 1))

        #End Label
        self.endLabel = customtkinter.CTkLabel(self.leftFrame, font = label_font, text="End:", anchor=W)
        self.endLabel.grid(row=4, column = 0, padx=15, pady= 5, sticky = E+W+N+S)

        #End Calendar
        self.endDateEntry = DateEntry(self.leftFrame, font=date_font)
        self.endDateEntry.grid(row=5, column = 0 ,columnspan=2, padx=15, pady=15, sticky= E+W+N+S)

        #Parameters For Music

        #Label for notes
        self.waveNoteLabel = customtkinter.CTkLabel(self.leftFrame, font= label_font, text= "Notes:", anchor= W)
        self.waveNoteLabel.grid(row= 6, column = 0, padx=15, pady=5, sticky= E+W+N+S)

        #Label For Notes Select
        self.waveNoteSelect = customtkinter.CTkOptionMenu(self.leftFrame, values = wave_note_select_options, font = label_font)
        self.waveNoteSelect.grid(row = 7, column= 0,columnspan=2, padx= 15, pady=10 , sticky= E+W+N+S)

        #Label for velocity
        self.waveVelocityLabel= customtkinter.CTkLabel(self.leftFrame, font= label_font, text= "Veloctiy:", anchor= W)
        self.waveVelocityLabel.grid(row=8, column= 0, padx= 15, pady= 5, sticky= E+W+N+S)
        
        #Option menu for velocity select parameter
        self.waveVelocitySelect= customtkinter.CTkOptionMenu(self.leftFrame, values= wave_velocity_select_options, font= label_font)
        self.waveVelocitySelect.grid(row=9, column= 0,columnspan=2, padx= 15, pady=10, sticky= E+W+N+S)     

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
        self.button = customtkinter.CTkButton(self.leftFrame, text="Listen", font= label_font, command=self.start_program)
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
    
    def purple_left_frame_update(self):
        
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

        self.purpleNoteLabel = customtkinter.CTkLabel(self.leftFrame, font= label_font, text= "Notes:", anchor= W)
        self.purpleNoteLabel.grid(row= 4, column = 0, padx=15, pady=0, sticky= E+W+N+S)

        #Label For Notes Selecfra
        self.purpleNoteSelect = customtkinter.CTkOptionMenu(self.leftFrame, font = label_font)
        self.purpleNoteSelect.grid(row = 5, column= 0,columnspan=2, padx= 15, pady=10 , sticky= E+W+N+S)

        #Label for velocity
        self.purpleVelocityLabel= customtkinter.CTkLabel(self.leftFrame, font= label_font, text= "Veloctiy:", anchor= W)
        self.purpleVelocityLabel.grid(row=6, column= 0, padx= 15, pady= 0, sticky= E+W+N+S)
        
        #Option menu for velocity select parameter
        self.purpleVelocitySelect= customtkinter.CTkOptionMenu(self.leftFrame, font= label_font)
        self.purpleVelocitySelect.grid(row=7, column= 0,columnspan=2, padx= 15, pady=10, sticky= E+W+N+S)     

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
        self.button = customtkinter.CTkButton(self.leftFrame, text="Listen", font= label_font, command=self.start_program)
        self.button.grid(row = 11, column=0,columnspan=2, padx=15, pady=20, sticky = E+W)

    def all_source_left_frame_update(self):
        
        self.leftFrame = customtkinter.CTkFrame(self)
        self.leftFrame.grid(row=1, column = 0 , columnspan= 2, padx= 20, pady= 10, sticky=W+N+E+S)
        self.leftFrame.columnconfigure((0), weight= 1)
        self.leftFrame.rowconfigure((0,1,2,4,6,8,10,11,12,13),weight=1)

        #Dataset Label
        self.dataLabel = customtkinter.CTkLabel(self.leftFrame, font= small_label_font, text= "Data:", anchor= W)
        self.dataLabel.grid(row= 0, column = 0, padx=15, pady=5, sticky= E+W+N+S)

        self.dataSelect = customtkinter.CTkOptionMenu(self.leftFrame, values=data_select_options, font= small_label_font, command=self.update_left_frame)
        self.dataSelect.grid(row= 1, column = 0, columnspan=2, padx=15, pady=5, sticky = E+W+N+S)
        self.dataSelect.set("All")
         
        #Start Calendar
        self.startLabel = customtkinter.CTkLabel(self.leftFrame, font = small_label_font, text="Start:", anchor=W)
        self.startLabel.grid(row=2, column = 0, padx=15, pady= 5, sticky = E+W+N+S)

        self.startDateEntry = DateEntry(self.leftFrame, font=small_label_font, color="white")
        self.startDateEntry.grid(row=3, column = 0 ,columnspan=2, padx=15, pady = 5, sticky=E+W+N+S)
        self.startDateEntry.set_date(date.today() - timedelta(days = 1))

        #End Label
        self.endLabel = customtkinter.CTkLabel(self.leftFrame, font = small_label_font, text="End:", anchor=W)
        self.endLabel.grid(row=4, column = 0, padx=15, pady= 5, sticky = E+W+N+S)

        #End Calendar
        self.endDateEntry = DateEntry(self.leftFrame, font=small_label_font)
        self.endDateEntry.grid(row=5, column = 0 ,columnspan=2, padx=15, pady=5, sticky= E+W+N+S)

        #Parameters For Music

        #Label for wave notes
        self.waveNoteLabel = customtkinter.CTkLabel(self.leftFrame, font= small_label_font, text= "Wave Notes:", anchor= W)
        self.waveNoteLabel.grid(row= 6, column = 0, padx=15, pady=5, sticky= E+W+N+S)

        #Label For wave Notes Select
        self.waveNoteSelect = customtkinter.CTkOptionMenu(self.leftFrame, values = wave_note_select_options, font = small_label_font)
        self.waveNoteSelect.grid(row = 7, column= 0,columnspan=2, padx= 15, pady=5 , sticky= E+W+N+S)

        #Label for wave velocity
        self.waveVelocityLabel= customtkinter.CTkLabel(self.leftFrame, font= small_label_font, text= "Wave Veloctiy:", anchor= W)
        self.waveVelocityLabel.grid(row=8, column= 0, padx= 15, pady= 5, sticky= E+W+N+S)
        
        #Option menu for wave velocity select parameter
        self.waveVelocitySelect= customtkinter.CTkOptionMenu(self.leftFrame, values= wave_velocity_select_options, font= small_label_font)
        self.waveVelocitySelect.grid(row=9, column= 0,columnspan=2, padx= 15, pady=5, sticky= E+W+N+S)    

        self.airSensorLabel = customtkinter.CTkLabel(self.leftFrame, font= small_label_font, text="Sensor:", anchor=W)
        self.airSensorLabel.grid(row= 10, column= 0, padx=15, pady=5, sticky= E+W+N+S)

        self.airSensorSelect = customtkinter.CTkOptionMenu(self.leftFrame, values=sensor_option, font= small_label_font, command=self.update_air_dropdowns)
        self.airSensorSelect.grid(row=11, column= 0,  columnspan= 2, padx=15, pady = 5, sticky= E+W+N+S )

        #Label for purple notes
        self.purpleNoteLabel = customtkinter.CTkLabel(self.leftFrame, font= small_label_font, text= "Air Quality Notes:", anchor= W)
        self.purpleNoteLabel.grid(row= 12, column = 0, padx=15, pady=5, sticky= E+W+N+S)

        #Label For purple Notes Select
        self.purpleNoteSelect = customtkinter.CTkOptionMenu(self.leftFrame, values = outdoor_sensor_options, font = small_label_font)
        self.purpleNoteSelect.grid(row = 13, column= 0,columnspan=2, padx= 15, pady=5 , sticky= E+W+N+S)

        #Label for purple velocity
        self.purpleVelocityLabel= customtkinter.CTkLabel(self.leftFrame, font= small_label_font, text= "Air Quality Veloctiy:", anchor= W)
        self.purpleVelocityLabel.grid(row=14, column= 0, padx= 15, pady= 5, sticky= E+W+N+S)
        
        #Option menu for purple velocity select parameter
        self.purpleVelocitySelect= customtkinter.CTkOptionMenu(self.leftFrame, values= outdoor_sensor_options, font= small_label_font)
        self.purpleVelocitySelect.grid(row=15, column= 0,columnspan=2, padx= 15, pady=5, sticky= E+W+N+S)

        #Label for BPM
        self.bpmLabel = customtkinter.CTkLabel(self.leftFrame,font = small_label_font, text= "BPM:" , anchor= W )
        self.bpmLabel.grid(row= 16, column= 0 , padx =15, pady= 5 , sticky= E+W+N+S)

        #Slider to pick beats
        self.bpmSlider = customtkinter.CTkSlider(self.leftFrame, from_= 30, to= 180, command= self.bpm_slider_callback)
        self.bpmSlider.set(60)
        self.bpmSlider.grid(row=17, column= 0, padx= 10, pady=5 , sticky= E+W+N+S)
        
        self.bpmSliderNum = customtkinter.CTkEntry(self.leftFrame, width= 60,font= small_label_font, placeholder_text= 60)
        self.bpmSliderNum.bind("<Return>", self.bpm_input_callback)
        self.bpmSliderNum.grid(row=17 , column= 1, padx=15, pady= 5, sticky= E+W+N+S)

        #Pan Switch for selecting if pan is on or off
        
        self.panSwitch = customtkinter.CTkSwitch(self.leftFrame, font= small_label_font, text= "Directional Audio")
        self.panSwitch.grid(row= 18 , column = 0, padx= 15, pady = 5, sticky= W+N+S)
        #Begin Button
        self.button = customtkinter.CTkButton(self.leftFrame, text="Listen", font= small_label_font, command=self.start_program)
        self.button.grid(row = 19, column=0,columnspan=2, padx=15, pady=5, sticky = E+W)

    def duplicate_until_size(self,arr, target_size):

        while len(arr) < target_size:
            arr = np.append(arr,arr)  # Duplicate the array
        return arr[:target_size]  # Trim to the target size

    def check_errors(self):
        error_text = None
        source = data_source_dict[self.dataSelect.get()]
        #Check if start date is greater than the end date
        if (source == (1 or 3)) and (self.startDateEntry.get_date() > self.endDateEntry.get_date()):
            error_text = "Start date must be before end date"
        #Check if data rows grabbed is more than 100. If so check if the user is okay with this. 24 rows per day
        elif (source == 1 and (self.endDateEntry.get_date() - self.startDateEntry.get_date()).days * 24) > 500 or (source == 3 and ((self.endDateEntry.get_date() - self.startDateEntry.get_date()).days * 24) > 250):
            if not messagebox.askokcancel("Warning", 'You are pulling over 500 data points, this may take a while.\nAre you sure you want to continue?'):
                error_text = "Canceled Operation"
        #Checks if instruments have not been created for the data being used
        elif (source == 1 and 0 not in self.instrument_assignment) or (source == 2 and 1 not in self.instrument_assignment) or (source == 3 and ((0 not in self.instrument_assignment) or (1 not in self.instrument_assignment))):
            error_text = "Please select an instrument in sound editor for this dataset"
        #Checks if notes have been selected
        elif len(self.notes) == 0:
            error_text = "Please select notes to use in the Note Editor"
        #Checks if valid bpm. 30 < bpm < 180
        elif 30 <= int(self.bpmSliderNum.get()) and int(self.bpmSliderNum.get()) <= 180:
            error_text = "Invalid bpm"   
        print(self.bpmSliderNum.get())
        if error_text:
            messagebox.showerror("Error",error_text)
            return True
        return False
         

app = App()
app.mainloop()
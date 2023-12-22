from tkinter import *
from tkcalendar import DateEntry
import customtkinter
from data_functions import data_to_midi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from audio_visualize import Graphic
import pygame


date_font = ("Helvetica", 28)
label_font = ("Helvetica", 24)

data_select_options = ["San Fransisco's Waves (Buoy)", "Davis Air Quality (Purple Air Sensor)", "Temperature In Room"]
wave_note_select_options = ["Height of Wave (Recommended)" , "Humidity", "Peak Period of Waves" , "Mean Period of Waves" ,  "Peak Direction of Wave"]
wave_velocity_select_options = ["Peak Period of Waves (Recommended)" , "Height of Wave" , "Humidity", "Mean Period of Waves" , "Peak Direction of Wave"]


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_default_color_theme("dark-blue")
        
        #Window
        self.geometry("400x150")
        self.rowconfigure((0),weight=1)
        self.columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11),weight=1)

        #Left Frame
        self.leftFrame = customtkinter.CTkFrame(self)
        self.leftFrame.grid(row=0, column = 0 , columnspan= 2, padx= 20, pady= 20, sticky=E+W+N+S)
        self.leftFrame.columnconfigure((0), weight= 1)

        #Left Frame Modules

        #Start Label
        self.startLabel = customtkinter.CTkLabel(self.leftFrame, font = label_font, text="Start:", anchor=W)
        self.startLabel.grid(row=0, column = 0, padx=15, pady= 15, sticky = E+W+N+S)
        #Start Calendar
        self.startDateEntry = DateEntry(self.leftFrame, font=date_font, color="white")
        self.startDateEntry.grid(row=1, column = 0 ,columnspan=2, padx=30, pady = 15, sticky=E+W+N+S)

        #End Label
        self.endLabel = customtkinter.CTkLabel(self.leftFrame, font = label_font, text="End:", anchor=W)
        self.endLabel.grid(row=2, column = 0, padx=15,sticky = E+W+N+S)

        #End Calendar
        self.endDateEntry = DateEntry(self.leftFrame, font=date_font)
        self.endDateEntry.grid(row=3, column = 0 ,columnspan=2, padx=30, pady=15, sticky= E+W+N+S)

        #Dataset Label
        self.dataLabel = customtkinter.CTkLabel(self.leftFrame, font= label_font, text= "Data:", anchor= W)
        self.dataLabel.grid(row= 4, column = 0, padx=15, pady=0, sticky= E+W+N+S)

        #Dataset Option Menu
        self.dataSelect = customtkinter.CTkOptionMenu(self.leftFrame, values=data_select_options, font= label_font)
        self.dataSelect.grid(row= 5, column = 0, columnspan=2, padx=15, pady=10, sticky = E+W+N+S) 

        #Parameters For Music

        #Label for notes
        self.noteLabel = customtkinter.CTkLabel(self.leftFrame, font= label_font, text= "Notes:", anchor= W)
        self.noteLabel.grid(row= 6, column = 0, padx=15, pady=0, sticky= E+W+N+S)

        #Label For Notes Select
        self.noteSelect = customtkinter.CTkOptionMenu(self.leftFrame, values = wave_note_select_options, font = label_font)
        self.noteSelect.grid(row = 7, column= 0,columnspan=2, padx= 15, pady=10 , sticky= E+W+N+S)

        #Label for velocity
        self.velocityLabel= customtkinter.CTkLabel(self.leftFrame, font= label_font, text= "Veloctiy:", anchor= W)
        self.velocityLabel.grid(row=8, column= 0, padx= 15, pady= 0, sticky= E+W+N+S)
        
        #Option menu for velocity select parameter
        self.velocitySelect= customtkinter.CTkOptionMenu(self.leftFrame, values= wave_velocity_select_options, font= label_font)
        self.velocitySelect.grid(row=9, column= 0,columnspan=2, padx= 15, pady=10, sticky= E+W+N+S)

        #Label for BPM
        self.bpmLabel = customtkinter.CTkLabel(self.leftFrame,font = label_font, text= "BPM:" , anchor= W )
        self.bpmLabel.grid(row= 10, column= 0 , padx =15, pady= 0 , sticky= E+W+N+S)

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

        #Right Frame 
        self.rightFrame = customtkinter.CTkFrame(self)
        self.rightFrame.grid(row= 0,column = 2, rowspan= 2,columnspan= 10, padx=20, pady=20, sticky=E+W+N+S)
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

        #Initializing actions for updating graph so we have an object that we can cancel
        self.graph_action = None

        self.controlFrame = customtkinter.CTkFrame(self)
        self.controlFrame.grid(row=1, column = 0 , columnspan= 2, padx= 20 , pady= 20, sticky = E+W+N+S)
        self.controlFrame.rowconfigure(0, weight = 0)
        self.controlFrame.columnconfigure(0, weight=0)


        #self.audio_controls_frame = customtkinter.CTkFrame(self.controlFrame)
        #self.audio_controls_frame.grid(row= 0, column = 0, sticky= E+W+N+S) 



    def start_button_callback(self):
        data_source_dict = {"San Fransisco's Waves (Buoy)": 1 , "Davis Air Quality (Purple Air Sensor)": 2 , "Temperature In Room": 3}
        data_source = self.dataSelect.get()
        note_column = self.noteSelect.get()
        velocity_column = self.velocitySelect.get()
        start_date = self.startDateEntry.get_date()
        start_date= str(start_date.year)+"-"+str(start_date.month)+"-"+str(start_date.day)
        end_date = self.endDateEntry.get_date()
        end_date= str(end_date.year)+"-"+str(end_date.month)+"-"+str(end_date.day)
        pan_switch = bool(self.panSwitch.get())
        bpm = int(self.bpmSlider.get())
    
        #Convert Using Dictionary later
        if note_column == "Height of Wave (Recommended)":
            note_column = "significantWaveHeight"
        if velocity_column == "Peak Period of Waves (Recommended)":
            velocity_column = "peakPeriod"

        if data_source_dict[data_source] == 1:
            time_column = "meanPeriod"
            index = 1

        if pan_switch:
            pan_column = "meanDirection"

        else:
            pan_column = False

        df = data_to_midi.get_data(1,100, start_date, end_date)

        time_x = df["meanPeriod"].values    
        note_y = df["significantWaveHeight"].values

        for i in range(1,len(time_x)):
            time_x[i] += time_x[i-1]
            
        spb = pow(bpm/60,-1)

        data_to_midi.api_to_midi(start_date,end_date,note_column,velocity_column, time_column, bpm, pan_switch, pan_column= pan_column) 
        pygame.init()
        pygame.mixer.music.load("gui_to_midi" + '.mid')
        pygame.mixer.music.play()

        self.colors = self.wave_graphic.create_colors(10,note_y)
        
        self.wave_graphic.cancel()

        self.wave_graphic.start_graphic(note_y, ((60000)/bpm)/10, self.colors)

        
        #for i in range(len(time_x) - 3):
           #graph_action = self.rightFrame.after(int(spb * 1000), self.update_graph(time_x, note_y, i))

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
    def update_graph(self,x,y, i):
            plt.ylim([0,.5])

            self.ax.clear() 
            self.ax.plot(x[i:i+3], y[i:i+3])
            self.ax.set_ylim([0, .5])

            self.canvas.draw_idle()  
            self.canvas.flush_events()
    """
    def cancel_action(self):
        if self.graph_action:
            try:
                data = self.tk.call('after', 'info', self.graph_action)
                script = self.tk.splitlist(data)
                print(script)
                for item in script:
                    self.deletecommand(item)
                print(script, "HEre is ")
            except TclError:
                pass    
            
            
app = App()
app.mainloop()
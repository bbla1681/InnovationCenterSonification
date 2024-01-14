import customtkinter
import tkinter as tk
from tkinter import *
from PIL import Image
sound_names = [
    'Acoustic Grand Piano',
    'Bright Acoustic Piano',
    'Electric Grand Piano',
    'Honky-tonk Piano',
    'Electric Piano 1',
    'Electric Piano 2',
    'Harpsichord',
    'Clavi',
    'Celesta',
    'Glockenspiel',
    'Music Box',
    'Vibraphone',
    'Marimba',
    'Xylophone',
    'Tubular Bells',
    'Dulcimer',
    'Drawbar Organ',
    'Percussive Organ',
    'Rock Organ',
    'Church Organ',
    'Reed Organ',
    'Accordion',
    'Harmonica',
    'Tango Accordion',
    'Acoustic Guitar (nylon)',
    'Acoustic Guitar (steel)',
    'Electric Guitar (jazz)',
    'Electric Guitar (clean)',
    'Electric Guitar (muted)',
    'Overdriven Guitar',
    'Distortion Guitar',
    'Guitar Harmonics',
    'Acoustic Bass',
    'Electric Bass (finger)',
    'Electric Bass (pick)',
    'Fretless Bass',
    'Slap Bass 1',
    'Slap Bass 2',
    'Synth Bass 1',
    'Synth Bass 2',
    'Violin',
    'Viola',
    'Cello',
    'Contrabass',
    'Tremolo Strings',
    'Pizzicato Strings',
    'Orchestral Harp',
    'Timpani',
    'String Ensemble 1',
    'String Ensemble 2',
    'SynthStrings 1',
    'SynthStrings 2',
    'Choir Aahs',
    'Voice Oohs',
    'Synth Voice',
    'Orchestra Hit',
    'Trumpet',
    'Trombone',
    'Tuba',
    'Muted Trumpet',
    'French Horn',
    'Brass Section',
    'SynthBrass 1',
    'SynthBrass 2',
    'Soprano Sax',
    'Alto Sax',
    'Tenor Sax',
    'Baritone Sax',
    'Oboe',
    'English Horn',
    'Bassoon',
    'Clarinet',
    'Piccolo',
    'Flute',
    'Recorder',
    'Pan Flute',
    'Blown Bottle',
    'Shakuhachi',
    'Whistle',
    'Ocarina',
    'Lead 1 (square)',
    'Lead 2 (sawtooth)',
    'Lead 3 (calliope)',
    'Lead 4 (chiff)',
    'Lead 5 (charang)',
    'Lead 6 (voice)',
    'Lead 7 (fifths)',
    'Lead 8 (bass + lead)',
    'Pad 1 (new age)',
    'Pad 2 (warm)',
    'Pad 3 (polysynth)',
    'Pad 4 (choir)',
    'Pad 5 (bowed)',
    'Pad 6 (metallic)',
    'Pad 7 (halo)',
    'Pad 8 (sweep)',
    'FX 1 (rain)',
    'FX 2 (soundtrack)',
    'FX 3 (crystal)',
    'FX 4 (atmosphere)',
    'FX 5 (brightness)',
    'FX 6 (goblins)',
    'FX 7 (echoes)',
    'FX 8 (sci-fi)',
    'Sitar',
    'Banjo',
    'Shamisen',
    'Koto',
    'Kalimba',
    'Bagpipe',
    'Fiddle',
    'Shanai',
    'Tinkle Bell',
    'Agogo',
    'Steel Drums',
    'Woodblock',
    'Taiko Drum',
    'Melodic Tom',
    'Synth Drum',
    'Reverse Cymbal',
    'Guitar Fret Noise',
    'Breath Noise',
    'Seashore',
    'Bird Tweet',
    'Telephone Ring',
    'Helicopter',
    'Applause',
    'Gunshot'
]

dataset_names = ["San Fransisco's Waves (Buoy)", "FLC Air Quality (Purple Air Sensor)"]
label_font = ("Helvetica", 40)

class Sound_Editor(customtkinter.CTkFrame,):
    def __init__(self,parent, **kwargs):

        customtkinter.CTkFrame.__init__(self,parent)

        #Window
        self.rowconfigure((0),weight=0)
        self.rowconfigure((1),weight=1)
        self.columnconfigure((0),weight=1)

        self.title = customtkinter.CTkLabel(self, text= "Sound Editor", font=label_font)
        self.title.grid(row=0, column= 0, pady= 30)

        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row= 1, column = 0, padx= 20, pady=20 , sticky = NSEW)
        self.main_frame.columnconfigure((0,1), weight= 1)
        self.main_frame.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13), weight=1)
        
        self.add_channel = customtkinter.CTkButton(self.main_frame, text= "Add Channel", command=self.add_channel_callback)
        self.add_channel.grid(row=0, column= 2, padx= 20, pady=20, sticky = N+E)

        self.delete_channel = customtkinter.CTkButton(self.main_frame, text= "Delete Channel", command= self.delete_channel_callback)
        self.delete_channel.grid(row= 0, column = 3, padx = 20 , pady = 20, sticky = N+E )

        self.drop_downs = []
        self.channel_labels = []
        self.data_assign = []

        if "channels" in kwargs:
            self.channels = kwargs['channels']
            if self.channels <=7:
                for channel in range(self.channels):
                    self.channel_labels.append(customtkinter.CTkLabel(self.main_frame, text="Channel " + str(channel+1) + ": "))
                    self.channel_labels[channel].grid(row= channel*2,column = 0, pady=0,sticky= W)
                    self.drop_downs.append(customtkinter.CTkOptionMenu(self.main_frame, values= sound_names))
                    self.drop_downs[channel].grid(row=channel*2+1, column= 0, padx=5, columnspan=3, sticky= E+W)
                    self.data_assign.append(customtkinter.CTkOptionMenu(self.main_frame, values = dataset_names))
                    self.data_assign[channel].grid(row=channel*2+1, column= 3, pady=5, sticky= E+W)
                    self.get_instruments()
        else:
            self.channels = 0
            self.add_channel_callback()

        if 'instruments' in kwargs:
            self.instruments = kwargs['instruments']
            self.instrument_assign = kwargs['instrument_assignment']

            for i in range(len(self.instruments_and_assignments)):
                self.drop_downs[i].set(sound_names[self.instruments[i]])
                self.data_assign[i].set(dataset_names[self.instrument_assign[i]])
        

    def add_channel_callback(self): 
        if self.channels <7:
            self.channels+=1
            index = self.channels-1
            self.channel_labels.append(customtkinter.CTkLabel(self.main_frame, text="Channel " + str(self.channels) + ": "))
            self.channel_labels[index].grid(row= index*2,column = 0, pady=0,sticky= W)
            self.drop_downs.append(customtkinter.CTkOptionMenu(self.main_frame, values= sound_names))
            self.drop_downs[index].grid(row=index*2+1, column= 0, columnspan= 3, padx=5, sticky= E+W)
            self.data_assign.append(customtkinter.CTkOptionMenu(self.main_frame, values = dataset_names))
            self.data_assign[index].grid(row=index*2+1, column= 3, padx=5, sticky= E+W)

    def delete_channel_callback(self):
        if self.channels > 1:
            index = self.channels - 1
            self.drop_downs[index].destroy()
            self.drop_downs.pop(index)
            self.channel_labels[index].destroy()
            self.channel_labels.pop(index)
            self.data_assign[index].destroy()
            self.data_assign.pop(index)
            self.channels -= 1 

    def get_instruments(self):
        self.instruments = []
        self.instrument_assign = []
        self.instruments_and_assignments = []
        if self.drop_downs is None:
            return [0]
        for i in range(len(self.drop_downs)):
            self.instruments.append(sound_names.index(self.drop_downs[i].get()))
            self.instrument_assign.append(dataset_names.index(self.data_assign[i].get()))
        self.instruments_and_assignments.append(self.instruments)
        self.instruments_and_assignments.append(self.instrument_assign)
        return self.instruments_and_assignments
          
    def get_channel_count(self):
        return self.channels


'''
Code for testing within file. File alone does not run without this
root = customtkinter.CTk()

root.rowconfigure(0,weight=1)
root.columnconfigure(0,weight=1)

sound_editor = Sound_Editor(root)
sound_editor.grid(row=0,column=0,sticky=NSEW )


root.mainloop()
'''

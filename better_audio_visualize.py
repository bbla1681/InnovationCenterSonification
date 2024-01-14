import numpy as np
import pygame

class Visualizer():

    def __init__(self, notes):

        self.notes = notes
        
        pygame.init()

        self.screen_x_max = 600
        self.screen_y_max = 600

        self.screen = pygame.display.set_mode((self.screen_x_max,self.screen_y_max))
        self.clock = pygame.time.Clock()

        self.PINK = (250,200,230)

        self.bpm = 60
        self.padx = 10
        self.pady = 100

        self.spacing = 10


    def run(self):
        run = True

        frequency_data = []

        for note in self.notes:
            frequency_data.append(self.get_frequency_data(note))

        while run: 
            self.screen.fill((255,255,255))
            averaged_frequency_data = []
            #Cycles through frequency data to average the first 5 points to the right 
            for i in range(len(frequency_data)):
                for j in range(frequency_data[i]):
                    data = 0
                    data_list = []
                    for k in range(5):
                        data += frequency_data[i][j+k]
                    data_list.append(data/5)
                    averaged_frequency_data.append(data_list)
                    j += 5
            #Gets Correct coordinates for the screen
            for i in averaged_frequency_data:
                x_start = self.padx
                x_end = self.spacing
                y_start = self.screen_y_max - self.pady
                y_end = 0
                for j in averaged_frequency_data[i]:
                    pygame.draw.polygon(self.screen, self.PINK)

    def midi_to_frequency(self, midi_note):
        return 440.0 * (2 ** ((midi_note - 69) / 12.0))

    def get_frequency_data(self, midi_note):

        # Set the frequency range from 1 Hz to 10k kHz
        frequency_range = np.logspace(0, 4, num=1000)
        print(frequency_range)

        # Set the range of MIDI notes you want to analyze
        midi_notes = np.arange(60, 64)  # MIDI notes for C4 to E4

        # Calculate corresponding amplitudes for each MIDI note
        amplitudes_per_note = []

        for midi_note in midi_notes:
            amplitude = np.sin(2 * np.pi * frequency_range * self.midi_to_frequency(midi_note))
            amplitudes_per_note.append(amplitude)

        amplitudes_per_note = np.array(amplitudes_per_note)

        # Convert the list of arrays to a 2D NumPy array
        return amplitudes_per_note 

visualizer = Visualizer()

visualizer.run()
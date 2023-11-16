from data_to_midi import df_to_midi, api_to_midi

filename="api_function_to_midi"

note_names = ['C2','D2','E2','G2','A2',
             'C3','D3','E3','G3','A3',
             'C4','D4','E4','G4','A4']

note_column = "significantWaveHeight"

velocity_column = "peakPeriod"

time_column = "meanPeriod"

beats = 60

bpm=60

vel_min,vel_max = 30,80

start='2023-11-09'
end='2023-11-10'

include_Track=True



api_df = api_to_midi(filename= filename, note_column=note_column, 
                     velocity_column= velocity_column, time_column= time_column , beats= beats, bpm=bpm, notes= note_names,
                       vel_min= vel_min, vel_max= vel_max, start=start, end=end)

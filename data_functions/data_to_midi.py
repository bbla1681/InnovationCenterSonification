from midiutil import MIDIFile 
from .sofar_api import get_data
from audiolazy import str2midi
import mido

def df_to_midi(df, note_column, velocity_column, time_column, bpm, pan_bool, **kwargs):
    filename = "gui_to_midi"
    notes = ['C2','D2','E2','G2','A2',
             'C3','D3','E3','G3','A3',
             'C4','D4','E4','G4','A4']
    vel_min = 80
    vel_max = 127
    notes_vals = df[note_column].values
    times = df[time_column].values
    velocity_vals = df[velocity_column]  


    #Puts the time data into a sequence, one after another instead of having potentially overlapping values (4, 4 , 5) -> (4,8,13) creates a timeline
    times[0] = bpm
    for i in range(1,len(times)):
        times[i] = times[i-1] + bpm

    beats = len(times)
    t_data = map_value(times, 0, max(times), 0,beats)
    
    normalized_velocity = map_value(velocity_vals, min(velocity_vals), max(velocity_vals), 0, 1)
    normalized_velocity = 1 - normalized_velocity
    normalized_notes = map_value(notes_vals, min(notes_vals), max(notes_vals), 0, 1)
    
    note_midis = [str2midi(n) for n in notes] 
    n_notes = len(note_midis)

    midi_data = []
    for i in range(len(normalized_notes)):
        note_index = round((map_value(normalized_notes[i], min(normalized_notes), max(normalized_notes), 0, n_notes-1))) 
        midi_data.append(note_midis[note_index])

    vel_data = []   
    for i in range(len(normalized_velocity)):
        note_velocity = round(map_value(normalized_velocity[i],0,1,vel_min, vel_max)) 
        vel_data.append(note_velocity)

    print(midi_data)

    #create midi file object, add tempo
    my_midi_file = MIDIFile(1) #one track 
    my_midi_file.addTempo(track=0, time=0, tempo=bpm) 

    #add midi notes
    for i in range(len(t_data)):
        my_midi_file.addNote(track=0, channel=0, time=t_data[i], pitch=midi_data[i], volume=vel_data[i], duration=2)
    #create and save the midi file itself
    with open(filename + '.mid', "wb") as f:
        my_midi_file.writeFile(f)
    
    if pan_bool:
        track_number = 1
        angles = df[kwargs["pan_column"]]
        adjusted_angles = map_value(angles, min(angles), max(angles), 30,97)
        int_angles = adjusted_angles.astype("int")
        add_pan(df, filename, track_number , int_angles)

def api_to_midi( start, end, note_column, velocity_column, time_column, bpm, pan_bool, **kwargs):
    api_df = get_data(index=1, lim=100, start=start, end=end)
    
    df_to_midi(api_df, note_column, velocity_column, time_column, bpm, pan_bool, **kwargs)


def map_value(value, min_value, max_value, min_result, max_result):
     #maps value (or array of values) from one range to another
     result = min_result + (value - min_value)/(max_value - min_value)*(max_result - min_result)
     return result

def add_pan(df, filename, track_number, pan_values):
    mid = mido.MidiFile("gui_to_midi" + ".mid")
    track = mid.tracks[track_number]
    current_time = 0
    index = 0
    pan_index = 0
    
    for i in range(len(track)):
        msg = track[i]

        try:
            if msg.type == "note_on":
                # Calculate the panning value based on the note number
                # Example: Panning based on note number (0 to 127)
                        
                panning_value = pan_values[pan_index]

                if msg.time != 0:
                        
                    pan_control = mido.Message('control_change', channel=msg.channel, control=10, value= panning_value, time= msg.time)
                    
                
                    track.insert(index+1, pan_control)
                   
                    if pan_index < len(pan_values)-1:
                        pan_index+=1
        except:
            print("Skipping Message, Non 'Note On' Value")
        index+=1
    mid.save(filename+".mid")
    return mid
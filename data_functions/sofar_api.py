from pysofar.sofar import SofarApi
import pandas as pd

def get_data(index,start,end):
    wave_heights = []
    api = SofarApi()

    #Get Devices and choose which one to use, right now it seems index 1 is the only one providing data
    devices = api.devices
    spotter_grid = api.get_spotters()
    spt_1 = spotter_grid[index]

    #Grabbing Latest Data Need To make function for this still
    #spt_1_dat = spt_1.latest_data()
    #spt_1_dat_freq = spt_1.latest_data(include_directional_moments=True)

    #Grabbbing Data by date and by key of waves
    spt_1_query = spt_1.grab_data(start_date=start, end_date=end, limit = None)
    wave_data = spt_1_query["waves"]

    #Append and return data as a pandas dataframe
    for i in range(len(wave_data)):
        wave_heights.append(wave_data[i])

    df = pd.DataFrame.from_records(wave_heights)
    
    return df

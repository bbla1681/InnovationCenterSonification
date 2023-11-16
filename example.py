from pysofar.sofar import SofarApi
from pysofar.spotter import Spotter
from pysofar.__init__ import get_token
import pandas as pd

# Had to Edit the __init__.py file and changed line 16 to userpath = os.getcwd()
api = SofarApi()
devices = api.devices

# grab spotter objects for the devices
spotter_grid = api.get_spotters()
# each array value is a spotter object
#The second Spotter appears to be the only one producing data
spt_1 = spotter_grid[1]
print("spotter 1" , spt_1)
print("grid" , spotter_grid)
#print(spt_0.mode)
#print(spt_0.lat)
#print(spt_0.lon)
#print(spt_0.timestamp)

# Get most recent data from the above spotter with waves
spt_0_dat = spt_1.latest_data()
#print(spt_0_dat)

# what if we want frequency data with directional moments as well
spt_0_dat_freq = spt_1.latest_data(include_directional_moments=True)
#print(spt_0_dat_freq)

# What about a specific range of time with waves and track data
spt_1_query = spt_1.grab_data(
    limit=100,
    start_date='2023-11-09',
    end_date='2023-11-10',
    include_track=True, include_wind= True
)
wave_heights = []
wave_data = spt_1_query["waves"]
for i in range(len(wave_data)):
    wave_heights.append(wave_data[i])

df = pd.DataFrame.from_records(wave_heights)

df


# What if we want all data from all spotters over all time
# this will take a few seconds
#all_dat = api.get_all_data()
#print(all_dat.keys())
#print(all_dat)



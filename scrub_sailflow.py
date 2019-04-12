import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import os
import csv
import re

# import send_email_text

# Run scrubber on all stations and save
def run_scrub():
    # Start timer
    start_time = time.time()

    # Determine current time
    now = datetime.utcnow()

    # Data storage folder
    fol_name = '../sailflow/{:s}/'.format(now.strftime('%Y%m'))

    # Make folder if doesn't yet exist
    if not os.path.exists(fol_name):
        os.mkdir(fol_name)

    # File name
    file_name = 'sailFlowPS_{:s}'.format(now.strftime('%Y%m%d_%H%M'))

    # Read in Station Names
    station_data = read_station_csv('sailflow_station_list.csv')


    # Loop through each station and write data from scrub to a csv file
    with open(fol_name + file_name, 'w') as f:
        f.writelines('Station_Name,Station_ID,Lat,Lon,Wind_Speed,Wind_Gust_Speed,Wind_Direction,SLP,Time\n')
        for key in station_data:
            # Name of station being scrubbed
            uniqueID = station_data[key]
            try:
                data = sailflow_scrubber(uniqueID)
                f.writelines('{},{},{},{},{},{},{},{},{}\n'.format(
                    key, uniqueID, data['lat'], data['lon'],
                    data['spd'], data['gust'], data['wnddir'], data['slp'],
                    data['timestamp']))
            except:
                #alert = 'weatherlink_scrubber failed on station {:s}'.format(tempName)
                #send_email_text.send_email('SayNoToMtBakerEruptions@gmail.com', alert)
                #print(key)
                nate = ''
    f.close()

def read_station_csv(csvName):
    ## Read in the data from CSV and make a dictionary
    with open(csvName) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # Make lists to house data from CSV
        name = []
        ID = []
        # Append values in CSV to variables
        for row in readCSV:
            name.append(row[0])
            ID.append(row[1])
        # Make a dictionary from the data
    station_data = dict(zip(name, ID))
    return station_data


def sailflow_scrubber(station_id):
    # Dictionary to house data
    data = {}
    # Conversion to MPH from KPH
    km2mph = 0.621371
    # Make the URL for the unique station
    base_url = 'https://www.sailflow.com/spot/'
    unique_url = base_url + station_id
    # Access Page
    page = requests.get(unique_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # Data is hidden in the script 'variable'
    # This is more for a trouble shooting, good for printing out the results
    currentCond = soup.find_all('script')[12].get_text()
    # Grab just the data
    data_values=json.loads(currentCond.split(";")[12].replace('\r\n            var stations = ','').replace('null','"NaN"'))[0]['data_values'][0]
    # assign data to variabls
    if data_values[2] != 'NaN':
        speed = round(data_values[2] * km2mph)
    else:
        speed = 'NaN'
    if data_values[4] != 'NaN':
        gust_speed = round(data_values[4] * km2mph)
    else:
        gust_speed = 'NaN'
    if data_values[5] != 'NaN':
        wnddir = data_values[5]
    else:
        wnddir = 'NaN'
    if data_values[11] != 'NaN':
        slp = round(data_values[11])
    else:
        slp = 'NaN'
    if data_values[0] != 'NaN':
        timestamp = data_values[0]
    else:
        timestamp = 'NaN'

    # Get Lat Lon values
    # Find all of the " " inds which will be for lat lon info
    quo_inds = [m.start() for m in re.finditer('"', currentCond)]
    la1 = quo_inds[4] + 1
    la2 = quo_inds[5]
    lo1 = quo_inds[6] + 1
    lo2 = quo_inds[7]
    lat = currentCond[la1:la2]
    lon = currentCond[lo1:lo2]

    # Add Data to Dictionary
    slp_key = 'slp'
    dir_key = 'wnddir'
    spd_key = 'spd'
    gst_key = 'gust'
    tsam_key = 'timestamp'
    lat_key = 'lat'
    lon_key = 'lon'
    data.update({slp_key: slp})
    data.update({dir_key: wnddir})
    data.update({spd_key: speed})
    data.update({gst_key: gust_speed})
    data.update({tsam_key: timestamp})
    data.update({lat_key: lat})
    data.update({lon_key: lon})
    return data


# Runs Main Script if used as stand-alone
if __name__ == '__main__':
    try:
        run_scrub()
    except:
        alert = 'run_scrub() failed for unknown reason'
        # send_email_text.send_email('TidesAreFakeNews@gmail.com', alert)
        raise Exception(alert)









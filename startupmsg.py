#!/usr/bin/python
import time
import datetime
import requests
import json

# Creates a presonalized greeting f(time of the day)
# The program rounds to the hour because it is clearer, faster,
# but basically becasue we do not need the precision

# Retrieves current hour from current time
current_hour = time.localtime().tm_hour

# We need the ISO date for the API Call
current_iso_date = str(time.localtime().tm_year) + "-" + str(time.localtime().tm_mon).zfill(2) + \
    "-" + str(time.localtime().tm_mday).zfill(2)


# Setting threshold hours to print time based messages
# I use the Dawn and Sunset thresholds from the external service https://sunrise-sunset.org/api
# Note: lat and long for Jerez are hardcoded. Can we get them by geolocating the device? IP geolocation?
uri = 'https://api.sunrise-sunset.org/json?lat=36.7147&lng=-6.1059&date=' + current_iso_date
response_API = requests.get(uri)
data = response_API.text
# Parse the data into a JSON => Dictionary in Python
data_dictionary = json.loads(data)
# Note: What happens if there is no internet connection or server times out?
status = data_dictionary['status']
if status == "UNKNOWN_ERROR":
    # TBD: try to connect again, just in case => create a function for the call of the api
    # TBD: wrap this in a try:catch funtion to catch errors
    print('\033[1;31merror: API Service failed! \33[0m\n')
    sunrise = "08:00:00"
    solar_noon = "12:00:00"
    sunset = "20:00:00"

elif status == "OK":
    # Note: According to API docs, time retrieved is not adjusted to summer calendar ?!
    #sunrise = int(data_dictionary['results']['sunrise'].split(":")[0])
    #sunset = int(data_dictionary['results']['sunset'].split(":")[0])
    #solar_noon = int(data_dictionary['results']['solar_noon'].split(":")[0])

    current_time = datetime.datetime(time.localtime().tm_year, time.localtime().tm_mon, time.localtime(
    ).tm_mday, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
    # The API returns the hour in format: HH:MM:SS AM/PM => use split and convert to datetime
    sunrise_split = data_dictionary['results']['sunrise'].split(":")
    horas = int(sunrise_split[0])
    minutos = int(sunrise_split[1])
    segundos = int((sunrise_split[2]).split()[0])
    sunrise = datetime.datetime(time.localtime().tm_year, time.localtime().tm_mon, time.localtime(
    ).tm_mday, horas, minutos, segundos)

    solar_noon_split = data_dictionary['results']['solar_noon'].split(":")
    horas = int(solar_noon_split[0])
    minutos = int(solar_noon_split[1])
    segundos = int((solar_noon_split[2]).split()[0])
    solar_noon = datetime.datetime(time.localtime().tm_year, time.localtime().tm_mon, time.localtime(
    ).tm_mday, horas, minutos, segundos)

    sunset_split = data_dictionary['results']['sunset'].split(":")
    horas = int(sunset_split[0])
    minutos = int(sunset_split[1])
    segundos = int((sunset_split[2]).split()[0])
    am_pm = sunset_split[2].split()[1]
    if am_pm == "pm" or "PM":
        horas = horas + 12
    sunset = datetime.datetime(time.localtime().tm_year, time.localtime().tm_mon, time.localtime(
    ).tm_mday, horas, minutos, segundos)

    #print("current: " + str(current_time.time()))
    #print("sunrise: " + str(sunrise.time()))
    #print("noon: " + str(solar_noon.time()))
    #print("sunset: " + str(sunset.time()))


else:
    sunrise = "08:00:00"
    solar_noon = "12:00:00"
    sunset = "20:00:00"

print("_,-._")
print("/ \_/ \")
print(">-(_)-<")
print("\_/ \_/")
print(" `-' ")  
# Gets the greeting message ready
# Night => bright blue "[94m
# Morning => bright yellow "[93m
# Evening => yellow (~orange) "[33m

greeting_message = "🌞 Buenos días"
color_code = "\033[1;93m"
if (current_time.time() > solar_noon.time() and current_time.time() < sunset.time()):
    greeting_message = "😎 Buenas tardes"
    color_code = "\033[1;33m"
elif (current_time.time() > sunset.time() or current_time.time() < sunrise.time()):
    greeting_message = "🌚 Buenas noches"
    color_code = "\033[94m"

# Name can be got from the system, now hardcoded
name = "Dani"

print(color_code + greeting_message + ' ' + "\033[39m" + name + "\n")

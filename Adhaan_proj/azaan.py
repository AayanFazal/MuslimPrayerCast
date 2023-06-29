#arp -a 
from tkinter.messagebox import YES
from turtle import clear
from numpy import cumprod
import requests
import json
from datetime import datetime 
import time
import pychromecast 
device = pychromecast.Chromecast("192.XXX.X.XXX") #IP address of google home device(s) 
device.wait() 
media = device.media_controller
url = "https://www.islamcan.com/audio/adhan/azan1.mp3" 
media.play_media(url,'audio/mp3')
 


# Returns prayer time from data and converts it into a time object
def get_prayer_time(data, prayer_name): 
    current_date = (data['date'])
    prayer_time = current_date + ";" + (data['today'][prayer_name])
    return datetime.strptime(prayer_time, "%a,%d %b %Y;%H:%M").time()

url = "https://dailyprayer.abdulrcs.repl.co/api/trenton" #Prayer time API, grabs prayer timings in Trenton, NJ - Can be changed 
response = requests.get(url)
data = response.json()

Fajr_time = get_prayer_time(data, 'Fajr')
sunrise_time = get_prayer_time(data,'Sunrise')
Dhuhr_time = get_prayer_time(data, 'Dhuhr')
Asr_time = get_prayer_time(data, 'Asr')
Maghrib_time = get_prayer_time(data, 'Maghrib')
Isha_time = get_prayer_time(data, "Isha'a")

today = datetime.now() 
current_time = today.time() 

M_hour,M_min,M_sec = (Maghrib_time.hour + 1,Maghrib_time.minute,Maghrib_time.second) 
M_end = Maghrib_time.replace(hour=M_hour, minute = M_min, second=M_sec)  

I_hour,I_min,I_sec = (Isha_time.hour + 1,Isha_time.minute,Isha_time.second) 
I_end = Isha_time.replace(hour=I_hour, minute = I_min, second=I_sec)  

def between(start_time,end_time,curr): 
    return curr > start_time and curr < end_time 

# fajr = 3, sunrise = 6 
# curr = 1  => No
# curr = 4 => Yes
# curr = 7 => No
# curr > fajr and curr < sunrise

# test code
#current_time = current_time.replace(hour=4, minute=50, second=0)
#print("Modified Current Time:")
print(current_time)
if between(Fajr_time,sunrise_time,current_time): 
    media.play_media(url,'audio/mp3')
    print("Fajr time")
    
elif between(Dhuhr_time,Asr_time,current_time): 
    media.play_media(url,'audio/mp3')
    print("Dhuhr time")
   
elif between(Asr_time,Maghrib_time,current_time): 
    media.play_media(url,'audio/mp3')
    print("Asr time")
    
elif between(Maghrib_time,M_end,current_time): 
    media.play_media(url,'audio/mp3')
    print("Maghrib time")
   
elif between(Isha_time,I_end,current_time): 
    media.play_media(url,'audio/mp3')
    print("Isha time")
    
else: 
    print("No prayer time")


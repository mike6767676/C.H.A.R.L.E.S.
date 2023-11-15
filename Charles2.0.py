 #importing
import os
import pyttsx3
from googlesearch import search
import webbrowser
from playsound import playsound
import time
import speech_recognition as sr
import pywhatkit as kt
import pvporcupine
import struct
import pyaudio
import pyautogui
from homeassistant_api import Client
import requests
from AppOpener import close

USER = "jack"

#Change based on pc
KWpath = 'D:\Jarvis\Wake word\Hey-Charles_en_windows_v2_2_0.ppn'

#home assistant
ServerURL = "https://homejrn.duckdns.org:8123/api"
Access_Token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlMjMzNjgzNjRlMjA0ZGRhYjAzN2ZiMDExMjc5YTdlMSIsImlhdCI6MTY4OTkzNTQ3NywiZXhwIjoyMDA1Mjk1NDc3fQ.J4uaVtqs98QQcTIE746P0ZdgVbrMxmzD0Z2FBoTeKcA"

#weather
Base_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = "930c9d3b79ad06aeeca1414e2a783b23"
city = "Fort Shawnee"

#wake word
def wake_word():
    porcupine = None
    print("Ready to help jack!")
    
    try:
        porcupine = pvporcupine.create(access_key='EWUXSsgHJffkhskOM4oC6ZjW74fr3vIy2fK4HYEnZlxkbLB25GCANQ==', keyword_paths=[KWpath])
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                main()
    finally:
            if porcupine is not None:
                porcupine.delete()



#def
engine = pyttsx3.init()

#voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

#rate
rate = engine.getProperty('rate')
engine.setProperty('rate', 170)




#main/start
def main():
    try:
    #request
        r=sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)

            engine.say("what would you like jack?")
            engine.runAndWait()
            print ("What would you like Jack?")

            audio1 = r.listen(source)

            audio = r.recognize_google(audio1)

        #stopwatch
        if audio =="stopwatch":
            engine.say("press enter to start")
            engine.runAndWait()
            input("press enter to start")
            Start_time= time.time()
            engine.say("press enter to stop")
            engine.runAndWait()
            input("press enter to stop")
            end_time= time.time()
            duration = int(end_time - Start_time)
            engine.say(str(duration) + "seconds", None)
            engine.runAndWait()
            print("duration was:", duration, "seconds")
            wake_word()

        #calculator
        if "calculate" in audio:
            w, x, M, y = audio.split()

            x = int(x)
            y = int(y)

            if M =="*":
                Z = x * y
            if M =="/":
                Z = x / y
            if M =="-":
                Z = x - y
            if M =="+":
                Z = x + y

            print(Z)
            engine.say(Z)
            engine.runAndWait()
            
            wake_word()

        #lights
        if audio == "turn on Jack's lamp":
            with Client(ServerURL, Access_Token) as client:
                light = client.get_domain("light")
                light.turn_on(entity_id="light.jack_s_lamp")
            
            engine.say("turning on")
            engine.runAndWait()
            print("Turning on...")
            wake_word()
        
        if audio == "turn off Jack's lamp":
            with Client(ServerURL, Access_Token) as client:
                light = client.get_domain("light")
                light.turn_off(entity_id="light.jack_s_lamp")
            
            engine.say("turning off")
            engine.runAndWait()
            print("Turning off...")
            wake_word()   
        
        #time
        if audio =="what is the time" or audio =="what time is it" or audio =="what's the time":
            time1 = time.strftime("%I:%M %p")
            time2 = time1.split(":", -1)
            time3 = " ".join(time2)
            engine.say("the time is" + time3, None)
            engine.runAndWait()
            print("The time is", time1)
            
            wake_word()

        #weather
        if audio =="what is the weather" or audio =="what's the weather":
            url = Base_URL + "appid=" + API_KEY + "&q=" + city
            response = requests.get(url).json()
            temp_fahrenheit = (response['main']['temp'] - 273.15) * (9/5) + 32
            temp_fahrenheit2 = round(temp_fahrenheit)
            description = response['weather'][0]['description']
            engine.say("it is " + str(temp_fahrenheit2) + "degrees fahrenheit and it is " + description)
            engine.runAndWait()
            print("It is " + str(temp_fahrenheit2) + "*F and it is " + description) 
            wake_word()    


        #google search
        if "search" in audio:
            w1  = audio.split()
            del w1[0]
            w2 = " ".join(w1)
            #searching
            print("searching", w2)
            kt.search(w2)
            wake_word()    

        #youtube
        if audio =="open YouTube":
            webbrowser.open("https://www.youtube.com/")
            engine.say("opening")
            engine.runAndWait()
            print("Opening...")
                
            wake_word()

        #home assistant
        if audio =="open Home assistant":
            webbrowser.open("https://homejrn.duckdns.org:8123/lovelace/home")
            engine.say("opening")
            engine.runAndWait()
            print("Opening...")
                
            wake_word()
            
        #Valorant
        if audio =="open valorant":
            os.startfile("C:\Riot Games\Riot Client\RiotClientServices.exe")
            engine.say("opening")
            engine.runAndWait()
            print("Opening...")
            
            wake_word()

        #battle front
        if audio =="open Battlefront":
            os.startfile("C:\Program Files\EA Games\STAR WARS Battlefront II\starwarsbattlefrontii.exe")
            engine.say("opening")
            engine.runAndWait()
            print("Opening...")
            
            wake_word()

        #keegan's dum request
        if audio == "you're gay Charles" or audio == "you're gay" or audio == "Charles you're gay":
            engine.say("you're stupid keegan")
            engine.runAndWait()
            print("You're stupid keegan!!!")
            
            wake_word()

        #vscode
        if audio =="open Visual Studio code" or audio =="open vs code":
            os.startfile("C:/Users/jacks/AppData/Local/Programs/Microsoft VS Code/Code.exe")
            engine.say("opening")
            engine.runAndWait()
            print("Opening...")
            
            wake_word()

        #volume controls
        if audio =="turn up the volume" or audio =="turn the volume up":
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            engine.say("turning up")
            engine.runAndWait()
            print("Turning up...")
            
            wake_word()

        if audio =="turn down the volume" or audio =="turn the volume down":
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            engine.say("turning down")
            engine.runAndWait()
            print("Turning down...")
            
            wake_word()
        

        #spotify
        if audio =="open Spotify":
            os.system("Spotify")
            engine.say("opening")
            engine.runAndWait()
            print("Opening...")
            
            wake_word()

        if audio =="start music":
            os.system("Spotify")
            time.sleep(8)
            pyautogui.press("space")
            engine.say("starting")
            engine.runAndWait()
            print("Starting...")
            
            wake_word()

        #pause/play/skip music
        if audio =="play music":
            pyautogui.press("playpause")
            engine.say("playing")
            engine.runAndWait()
            print("Playing...")
            
            wake_word()
        
        if audio =="skip song":
            pyautogui.press("nexttrack")
            engine.say("skiping")
            engine.runAndWait()
            print("Skiping...")
            
            wake_word()
            
        if audio =="pause music":
            close("Spotify")
            engine.say("pauseing")
            engine.runAndWait()
            print("Pauseing...")
            
            wake_word()

        
        #discord
        if audio =="open Discord":
            os.startfile("C:/Users/jacks/AppData/Local/Discord/app-1.0.9015/Discord.exe")
            engine.say("opening")
            engine.runAndWait()
            print("Opening...")
            
            wake_word()
            
        #exit
        if audio == "exit" or "exit" in audio or audio =="stop" or audio =="close":
            engine.say("good bye")
            engine.runAndWait()
            wake_word()
            

        #unknown commands
        else:
            engine.say("I didn't get that")
            engine.runAndWait()
            print("I didn't get that")
            main()

    #unknown commands
    except:
        engine.say("I didn't get that")
        engine.runAndWait()
        print("I didn't get that")
        main()
  
wake_word()


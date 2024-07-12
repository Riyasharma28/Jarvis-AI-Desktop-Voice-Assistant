from http import client
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI 
from gtts import gTTS
import pygame 
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "59dde19eccff4142804bba57a42e7af7"

def aiProcess(command):
    client = OpenAI(api_key="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",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content



def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
     # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r=requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles',[])

            for articles in articles:
                speak(articles['title'])
    else:
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        r = sr.Recognizer()
        print("Recognizing")
        
        try:
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source, timeout=2)
                word = r.recognize_google(audio) 
            
            if word.lower() == "jarvis":
                speak("ya")
            
                with sr.Microphone() as source:
                    print("Jarvis Active!")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                processCommand(command)
  
        except Exception as e:
            print("Error: {0}".format(e))

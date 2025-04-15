import pyttsx3
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
import datetime
import pyautogui
import random
import webbrowser
import os
import subprocess  # For better app opening
from plyer import notification
from pygame import mixer

# Password Protection
for i in range(3):
    a = input("Enter Password to open Jarvis: ")
    with open("password.txt", "r") as pw_file:
        pw = pw_file.read()
    if a == pw:
        print("WELCOME SIR! PLEASE SPEAK 'WAKE UP' TO LOAD ME UP.")
        break
    elif i == 2 and a != pw:
        exit()
    else:
        print("Try Again")

# Text-to-Speech Engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Speech Recognition
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 4)
    try:
        print("Understanding...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception:
        print("Say that again...")
        return "None"
    return query.lower()

# Alarm Function
def alarm(query):
    with open("Alarmtext.txt", "a") as timehere:
        timehere.write(query)
    os.startfile("alarm.py")

# Function to Open Applications
def open_application(query):
    app_name = query.replace("open", "").strip()  # Extract application name
    speak(f"Opening {app_name}")

    # Method 1: Using pyautogui (Windows Start Menu Search)
    pyautogui.press("win")  # Open Windows Start menu
    pyautogui.sleep(1)
    pyautogui.typewrite(app_name, interval=0.1)  # Type application name
    pyautogui.sleep(1)
    pyautogui.press("enter")  # Press enter to open the application

    # Method 2: Using subprocess (For better reliability)
    try:
        subprocess.Popen(app_name, shell=True)  # Try opening directly
    except Exception as e:
        speak("Sorry, I couldn't open the application.")
        print(f"Error: {e}")

# Main Program Loop
if __name__ == "__main__":
    while True:
        query = takeCommand()

        if "wake up" in query:
            from GreetMe import greetMe
            greetMe()

            while True:
                query = takeCommand()

                if "go to sleep" in query:
                    speak("Okay sir, you can call me anytime.")
                    break
                
                elif "change password" in query:
                    speak("What's the new password?")
                    new_pw = input("Enter the new password: ")
                    with open("password.txt", "w") as new_password:
                        new_password.write(new_pw)
                    speak("Done sir")
                    speak(f"Your new password is {new_pw}")

                elif "screenshot" in query:
                    im = pyautogui.screenshot()
                    im.save("screenshot.jpg")
                    speak("Screenshot taken.")

                elif "click my photo" in query:
                    pyautogui.press("super")
                    pyautogui.typewrite("camera")
                    pyautogui.press("enter")
                    pyautogui.sleep(2)
                    speak("SMILE!")
                    pyautogui.press("enter")

                elif "open app" in query:
                    open_application(query)

                elif "google" in query:
                    query = query.replace("search", "")
                    query = query.replace("google", "")
                    speak(f"Searching Google for {query}")
                    webbrowser.open(f"https://www.google.com/search?q={query.strip()}")

                elif "youtube" in query:
                    query = query.replace("search", "")
                    query = query.replace("youtube", "")
                    speak(f"Searching YouTube for {query}")
                    webbrowser.open(f"https://www.youtube.com/results?search_query={query.strip()}")


                elif "wikipedia" in query:
                    query = query.replace("search", "")
                    query = query.replace("wikipedia", "")
                    speak(f"Searching Wikipedia for {query}")
                    webbrowser.open(f"https://en.wikipedia.org/wiki/{query.strip().replace(' ', '_')}")


                elif "news" in query:
                    from NewsRead import latestnews
                    latestnews()

                elif "calculate" in query:
                    from Calculatenumbers import WolfRamAlpha, Calc
                    query = query.replace("calculate", "").strip()
                    Calc(query)

                elif "temperature" in query or "weather" in query:
                    search = "temperature in delhi"
                    url = f"https://www.google.com/search?q={search}"
                    r = requests.get(url)
                    data = BeautifulSoup(r.text, "html.parser")
                    temp = data.find("div", class_="BNeawe").text
                    speak(f"Current {search} is {temp}")

                elif "set an alarm" in query:
                    speak("Set the time in format HH MM SS")
                    a = input("Please enter the time (HH MM SS): ")
                    alarm(a)
                    speak("Done sir.")

                elif "the time" in query:
                    strTime = datetime.datetime.now().strftime("%H:%M")
                    speak(f"Sir, the time is {strTime}")

                elif "pause" in query:
                    pyautogui.press("k")
                    speak("Video paused.")

                elif "play" in query:
                    pyautogui.press("k")
                    speak("Video played.")

                elif "mute" in query:
                    pyautogui.press("m")
                    speak("Video muted.")

                elif "volume up" in query:
                    pyautogui.press("volumeup")
                    speak("Turning volume up, sir.")

                elif "volume down" in query:
                    pyautogui.press("volumedown")
                    speak("Turning volume down, sir.")

                elif "remember that" in query:
                    rememberMessage = query.replace("remember that", "").strip()
                    speak(f"You told me to remember that: {rememberMessage}")
                    with open("Remember.txt", "a") as remember:
                        remember.write(rememberMessage + "\n")

                elif "what do you remember" in query:
                    with open("Remember.txt", "r") as remember:
                        speak("You told me to remember: " + remember.read())

                elif "tired" in query:
                    speak("Playing your favorite songs, sir.")
                    songs = [
                        "https://www.youtube.com/watch?v=OqxSZytsjMA",
                        "https://www.youtube.com/watch?v=8YdXb2SgUFY",
                        "https://www.youtube.com/watch?v=KBYSpR8N6pc"
                    ]
                    webbrowser.open(random.choice(songs))

                elif "schedule my day" in query:
                    tasks = []
                    speak("Do you want to clear old tasks? Say YES or NO")
                    query = takeCommand()
                    if "yes" in query:
                        open("tasks.txt", "w").close()
                    no_tasks = int(input("Enter the number of tasks: "))
                    for i in range(no_tasks):
                        task = input(f"Enter task {i+1}: ")
                        tasks.append(task)
                        with open("tasks.txt", "a") as file:
                            file.write(f"{i+1}. {task}\n")

                elif "show my schedule" in query:
                    with open("tasks.txt", "r") as file:
                        content = file.read()
                    mixer.init()
                    mixer.music.load("notification.mp3")
                    mixer.music.play()
                    notification.notify(
                        title="My Schedule:",
                        message=content,
                        timeout=15
                    )

                elif "shutdown the system" in query:
                    speak("Are you sure you want to shut down?")
                    shutdown = input("Do you wish to shut down your computer? (yes/no): ")
                    if shutdown.lower() == "yes":
                        os.system("shutdown /s /t 1")
                    else:
                        pass

                elif "finally sleep" in query:
                    speak("Going to sleep, sir.")
                    exit()

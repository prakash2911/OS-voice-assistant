import email
from logging import exception
from sys import flags
import pyttsx3  
import datetime
import speech_recognition as sr  
import webbrowser 
import os
import pyautogui  
import psutil  
import pyjokes
import random
import importlib
import yfinance as yf
import time


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)
engine.setProperty('rate',160)

class Person:
    name = 'Owner'
    
    def setName(self, name):
        self.name = name
        
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def gettime():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("the current time is")
    speak(Time)


def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak("the current date is")
    speak(date)
    speak(month)
    speak(year)


def wishme():
    speak("Welcome back sir!")
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Good morning sir!")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon sir")
    elif hour >= 18 and hour < 24:
        speak("Good Evening sir")
    else:
        speak("Good night sir")

    speak("dexter at your service. Please tell me how can i help you?")
def compusage():
    cpu_usage = str(psutil.cpu_percent())
    speak("Usage of CPU is at: " + cpu_usage)

    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = str(battery.percent)
    plugged = "Plugged In" if plugged else "Not Plugged In"
    speak("Usage of BATTERY is at: " + percent)
    speak("The CPU count is " + psutil.cpu_count)
    speak("The CPU count is " + psutil.cpu_count)
    speak(plugged)

    ram_usage = str(psutil.virtual_memory())
    print("Usage of RAM is at: " + ram_usage)
    speak("Usage of RAM is at: " + ram_usage)
    speak("the disk usage is " + psutil.disk_usage('/'))

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print(query)

    except Exception as e:
        print(e)
        #speak("Say that again please...")
        return "None"
    return query


def jokes():
    speak(pyjokes.get_joke())

def there_exists(terms, query):
    for term in terms:
        if term in query:
            return True
flags = False
if __name__ == "__main__":
    speak("say dexter to start the service.")
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(query)
            if there_exists(["dexter"],query.lower()):
                wishme()
                person_obj = Person()
                flags = True
                break
        except:
            print("listening")
while True and flags:
    query = takeCommand().lower()
    if there_exists(['hey', 'hi', 'hello', "dexter"],query):
        greetings = [f"hey, how can I help you {person_obj.name}", f"hey, what's up? {person_obj.name}",
                f"I'm listening {person_obj.name}", f"how can I help you? {person_obj.name}",
                f"hello {person_obj.name}"]
        greet = greetings[random.randint(0, len(greetings) - 1)]
        speak(greet)
    elif there_exists(["what is your name", "what's your name", "tell me your name"],query):
        if person_obj.name:
            speak("my name is dexter")
        else:
            speak("my name is dexter. what's your name?")
    elif there_exists(["my name is"],query):
        person_name = query.split("is")[-1].strip()
        speak(f"okay, i will remember that {person_name}")
        person_obj.setName(person_name)  # remember name in person object
    elif there_exists(["how are you", "how are you doing"],query):
        speak(f"I'm very well, thanks for asking {person_obj.name}")
    elif there_exists(["who created you", "who made you"],query):
        speak("My owner is Team 8 and God created my owner.")
    elif there_exists(["can you make me laugh", "make me laugh",'tell me a joke','joke'],query):
        speak("Yeah of course")
        jokes()
    elif there_exists(["open notes"],query):
        os.system("gedit sample.txt")
    # 4: time
    elif there_exists(["what's the time", "tell me the time", "what time is it"],query):
        gettime()
        # 5: search google
    elif there_exists(["search for"],query) and 'youtube' not in query and 'github' not in query:
        search_term = query.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on google')
    elif there_exists(["github"],query) and 'youtube' not in query and 'google' not in query:
        search_term = query.split("for")[-1]
        url = f"https://github.com/search?q=+{search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on github')
    # 6: search youtube
    elif there_exists(["youtube"],query) and 'google' not in query and 'google' not in query:
        search_term = query.split("for")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on youtube')
        time.sleep(5)
    elif there_exists(['computer usage','computer performance'],query):
        compusage()
    # 7: get stock price
    elif there_exists(["price of"],query):
        search_term = query.lower().split(" of ")[-1].strip()
        stocks = {
            "apple": "AAPL",
            "microsoft": "MSFT",
            "facebook": "FB",
            "tesla": "TSLA",
            "bitcoin": "BTC-USD"
        }
        try:
            stock = stocks[search_term]
            stock = yf.Ticker(stock)
            price = stock.info["regularMarketPrice"]
            print(search_term)
            speak(f'price of {search_term} is {price} {stock.info["currency"]} {person_obj.name}')
        except:
            speak('oops, something went wrong')
    elif there_exists(["exit", "quit", "goodbye", "good bye", "bye"],query):
        speak("going offline")
        flags= False
        os.system('python3 /dexter/final.py')
    elif there_exists(["open"],query):
        application = query.split("the")[-1].strip()
        if application == "calculator":
            os.system("gnome-calculator")
        elif application == "calendar":
            os.system("gnome-calendar")
        elif application == ["terminal", "command line"]:
            os.system("gnome-terminal")
    elif there_exists(["screenshot", "ss"],query):
        os.system("gnome-screenshot")
    elif there_exists(["video", "screen video"],query):
        try:
            os.system("sudo apt install kazam")
        except SystemError:
            os.system("kazam")
        os.system("kazam")
    elif there_exists(["camera", "cam", "am i beautiful", "am i handsome"],query):
        try:
            os.system("sudo apt install cheese")
        except SystemError:
            os.system("cheese")
        os.system("cheese")
    elif(query.find("computer") != -1):
        le = query.find("computer")+len("computer")+1
        query = query[le:]
        try:
            if (query == "suspend" or query == "sleep"):
                os.system("systemctl suspend")
            elif (query == "power off" or query == "shutdown"):
                os.system("systemctl poweroff")
            elif (query == "reboot" or query == "restart"):
                os.system("systemctl reboot -i")
        except:
            speak("Couldn't do it")
    elif(query.find("reboot") != -1):
        le = query.find("reboot")+len("reboot")+1
        query = query[le:]
        try:
            if (query == "computer" or query == "pc"):
                os.system("systemctl reboot -i")
        except:
            speak("Couldn't do it")
    elif(query.find("restart") != -1):
        le = query.find("restart")+len("restart")+1
        query = query[le:]
        try:
            if (query == "computer" or query == "pc"):
                os.system("systemctl reboot -i")
        except:
            speak("Couldn't do it")
    elif(query.find("suspend") != -1):
        le = query.find("suspend")+len("suspend")+1
        query = query[le:]
        try:
            if (query == "computer" or query == "pc"):
                os.system("systemctl suspend")
        except:
            speak("Couldn't do it")
    elif(query.find("sleep") != -1):
        le = query.find("sleep")+len("sleep")+1
        query = query[le:]
        try:
            if (query == "computer" or query == "pc"):
                os.system("systemctl suspend")
        except:
            speak("Couldn't do it")
    elif(query.find("shutdown") != -1):
        le = query.find("shutdown")+len("shutdown")+1
        query = query[le:]
        try:
            if (query == "computer" or query == "pc"):
                os.system("systemctl poweroff")
        except:
            speak("Couldn't do it")
    elif(query.find("Power off") != -1):
        le = query.find("Power off")+len("Power off")+1
        query = query[le:]
        try:
            if (query == "computer" or query == "pc"):
                os.system("systemctl poweroff")
        except:
            speak("Couldn't do it")
    elif there_exists(['watch', 'netflix'],query):
        watchs = query.split("watch")[-1]
        url = f"https://google.com/search?q={watchs}"
        webbrowser.get().open(url)
        time.sleep(10)
        pyautogui.moveTo(200, 315)
        pyautogui.click(x=200, y=315)
        speak('Have a good time')
    elif there_exists(["set alarm", "alarm"],query):
        try:
            os.system("sudo apt-get install vlc-bin")
        except SystemError:
            os.system("sudo apt-get install vlc-bin")
        alarm = query.split("alarm")[-1]
        os.system("sleep {}h && vlc alarm.mp3".format(alarm))
    elif there_exists(["timer", "set timer"],query) and "alarm" not in query:
        time = query.split("for")[-1].strip()
        os.system("sleep {} && vlc alarm.mp3".format(time))
    elif there_exists(["cancel alarm"],query):
        pyautogui.hotkey('ctrlleft', 'c')
    elif there_exists(["roll a die"],query):
        rand = random.randint(1, 6)
        speak("Result is {}".format(rand))
    elif there_exists(["flip a coin"],query):
        coin = ['heads'] * 50 + ['tails'] * 50 + ['perpendicular'] * 1
        speak(random.choice(coin))
    elif query == "what time is it in":
        location = query.split("in")[-1].strip()
        url = "https://www.google.com/search?q=what+time+is+it+in+{}".format(location)
        webbrowser.get().open(url)
    elif "how much is" in query:
        convert = query.split("is")[-1].strip()  # 5 dollar in euros
        url = f"https://www.google.com/search?q=how+much+is+{convert}"
        webbrowser.get().open(url)
    elif there_exists(["calculate"],query):
        search = query.split("calculate")[-1].strip()
        url = f"https://www.google.com/search?q=how+much+is+{search}"
        webbrowser.get().open(url)
    elif there_exists(["what is"],query):
        search = query.split("is")[-1].strip()
        url = f"https://www.google.com/search?q=how+much+is+{search}"
        webbrowser.get().open(url)
    elif there_exists(["pip"],query):
        package = query.split("install")[-1]
        try:
            os.system("pip install {}".format(package))
            importlib.import_module(package)
        except ImportError:
            speak("Import ERROR")
    elif there_exists(["update", "update the system"],query):
        os.system("sudo -S apt update")
        os.system("sudo -S apt upgrade")
    elif there_exists(["take note", "note"],query):
        text_file = open("sample.txt", "w")
        note = takeCommand()
        text_file.write(note)
        text_file.close()
    elif "count to" in query:
        count = query.split("to")[-1].strip()
        for i in range(int(count)):
            speak(str(i+1))
    elif there_exists(["telegram message to"],query):
        data = query.split("to")[-1].strip()
        url = "https://web.telegram.org/#/im?p=@{}".format(data)
        time.sleep(3)
        webbrowser.get().open(url)
    elif there_exists(["call me"],query):
        nickname = query.split("me")[-1].strip()
        person_obj.setName(nickname)
    elif there_exists(["increase sound", "incrase volume"],query):
        os.system("pactl -- set-sink-volume 0 +10%")
    elif there_exists(["decrease sound", "decrease volume"],query):
        os.system("pactl -- set-sink-volume 0 -10%")
    elif there_exists(["find location"],query):
        speak('Which location you want to search for')
        location = takeCommand()
        url = 'https://google.nl/maps/place' + str(location)
        webbrowser.get().open(url)
        speak("here is your location" + str(location) + '/&amp;')
    elif there_exists(["search for viki", "vikipedia"],query):
        speak('Which concept you want to search for')
        concept = takeCommand()
        url = 'https://wikipedia.org/wiki/' + str(concept)
        webbrowser.get().open(url)
    elif there_exists(["translate"],query):
        speak('Which word you want to translate for')
        words = takeCommand()
        url = 'https://translate.google.com/?hl=tr#view=home&op=translate&sl=auto&tl=tr&text=' + str(words)
        webbrowser.get().open(url)
    elif there_exists(["increase brigh", "brighter"],query):
        os.system("xrandr --output VGA1 --brightness 1")
        os.system("xrandr --output Virtual1 --brightness 1")
    elif there_exists(["decrease brightness"],query):
        os.system("xrandr --output Virtual1 --brightness 0.1")
        os.system("xrandr --output Virtual1 --brightness 0.1")
    elif there_exists(["enable bluetooth",'bluetooth'],query):
        os.system("sudo service bluetooth start")
    elif there_exists(["disable bluetooth"],query):
        os.system("sudo service bluetooth stop")
    elif there_exists(["lock"],query):
        pyautogui.hotkey('ctrlleft', 'altleft', 'l')
    elif there_exists(["ping to"],query):
        site = query.split("to")[-1].strip()
        os.system("ping {}".format(site))
    elif there_exists(["calendar"],query):
        os.system("cal")
    elif there_exists(["who is"],query):
        os.system("sudo apt install whois")
        speak('Which word you want to translate for')
        who = takeCommand()
        os.system("whois {}".format(who))
    elif there_exists(["install sublime text"],query):
        os.system("wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -")
        os.system('echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee '
                '/etc/apt/sources.list.d/sublime-text.list')
        os.system("sudo apt-get install sublime-text")
        os.system("sublime-text")
    elif there_exists(["summarize"],query):
        subject = query.split("summarize")[-1].strip()
        url = f"https://google.com/search?q={subject}summarize"
        webbrowser.get().open(url)
        # TODO : ADD BETTER SOLUTION
    elif there_exists(["what's the weather like today?", "do I need an umbrella today?", "what's the weather going to be like", "what's the temperature outside? ","is there a chance of rain on"],query):
        url = "https://google.com/search?q=weather"
        webbrowser.get().open(url)
    elif there_exists(["to do"],query):
        os.system("sudo add-apt-repository ppa:mank319/go-for-it")
        os.system("sudo apt update && sudo apt install go-for-it")
        # TODO : ADD TO DO LIST WITH SPEECH
    elif there_exists(["remind me"],query):
        os.system("sudo add-apt-repository ppa:umang/indicator-stickynotes")
        os.system("sudo apt-get install indicator-stickynotes")
        os.system("indicator-stickynotes")
        # TODO : ADD TO DO LIST WITH SPEECH
    elif there_exists(["what's the traffic like on the way to work"],query):
        url = "https://www.google.com/search?q=what%E2%80%99s+the+traffic+like+on+the+way+to+work"
        webbrowser.get().open(url)
    elif there_exists(["find my phone"],query):
        url = "https://www.google.com/android/find"
        webbrowser.get().open(url)
    elif (query.find("go to") != -1):
            le = query.find("go to")+len("go to")+1
            query = query[le:]
            try:
                if (query == "facebook" or query == "fb"):
                    webbrowser.open("https://www.facebook.com")

                elif (query == "twitter" or query == "Twitter"):
                    webbrowser.open("https://www.twitter.com")

                elif (query == "github" or query == "Github"):
                    webbrowser.open("https://www.github.com")

                elif (query == "instagram" or query == "Insta"):
                    webbrowser.open("https://www.instagram.com")

                elif (query == "youtube" or query == "yt"):
                    webbrowser.open("https://www.youtube.com")
                elif (query == "whatsapp"):
                	webrowser.open("https://web.whatsapp.com")

                else:
                    webbrowser.open(""+query.lower())
            except:
                speak("Sorry,Couldn't do it")
    elif query == "self destroy" or query =="self destroyed":
        speak("dexter service stopped")
        flag = False
        break
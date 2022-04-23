from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys

recogniser = speech_recognition.Recognizer()
speaker = tts.init()
speaker.setProperty('rate', 150)
todo_list = ['OS project', 'CA exam']


def create_note():
    global recogniser

    speaker.say("What do you feel like writing onto the note ?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone as mic:

                recogniser.adjust_for_ambient_noise(mic, duration=2.0)
                audio = recogniser.listen(mic)

                note = recogniser.recognize_google(audio)
                note = note.lower()

                speaker.say("Choose a filename!")
                speaker.runAndWait()

                recogniser.adjust_for_ambient_noise(mic, duration=2.0)
                audio = recogniser.listen(mic)

                filename = recogniser.recognize_google(audio)
                filename = filename.lower()

            with open(filename, 'w') as f:
                f.write(note)
                done = True
                speaker.say(f"I successfully created the note {filename}")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recogniser = speech_recognition.Recognizer()
            speaker.say("I did not understand you! PLease try again")
            speaker.runAndWait()


def add_todo():
    global recogniser

    speaker.say("What todo do you want to add")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recogniser.adjust_for_ambient_noise(mic, duration=2.0)
                audio = recogniser.listen(mic)

                item = recogniser.recognize_google(audio)
                item = item.lower()

                todo_list.append(item)
                done = True

                speaker.say(f"I added {item} to thr to do list")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recogniser = speech_recognition.Recognizer()
            speaker.say("I did not understand you! PLease try again")
            speaker.runAndWait()


def show_todo():

    speaker.say("The items on your to do list are as following")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()


def hello():
    speaker.say("Hello what can I do for you?")
    speaker.runAndWait()


def quit():
    speaker.say("Bye")
    speaker.runAndWait()
    sys.exit()


mappings = {
    "greeting": hello,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todo": show_todo,
    "exit": quit
}
assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

while True:
    try:
        with speech_recognition.Microphone() as mic:

            recogniser.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recogniser.listen(mic)

            message = recogniser.recognize_google(audio)
            message = message.lower()

        assistant.request(message)
    except speech_recognition.UnknownValueError:
        recogniser = speech_recognition.Recognizer()

#Import library
import speech_recognition as sr
import time

#Import module
import remote
import script_gui

speechOn = False    #Cek apakah speech recognition menyala atau tidak

def listen_and_respond():
    while script_gui.windowOpen:
        time.sleep(1/script_gui.fps)

        while speechOn:
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()

            while speechOn:
                print("Menunggu suara...")
                try:
                    with microphone as source:
                        recognizer.adjust_for_ambient_noise(source)
                        print("Tolong ucapkan sesuatu...")
                        audio = recognizer.listen(source)

                    command = recognizer.recognize_google(audio, language="id-ID")
                    print(f"Anda mengatakan {command}")

                    # Check the command
                    if "nyala" in command.lower():
                        remote.myRemote.nyalakanAC()
                    elif "mati" in command.lower():
                        remote.myRemote.matikanAC()
                    else:
                        print("Perintah tidak valid!")

                except sr.UnknownValueError:
                    print("Perintah tidak terdengar")
                except:
                    pass

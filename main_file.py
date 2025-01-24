import pyttsx3
import working
import speech_recognition as sr
import mysql.connector
import time
import os
import threading

class Brain:
    def __init__(self):
        self.engine=pyttsx3.init('sapi5')
        voices=self.engine.getProperty('voices')
        self.engine.setProperty('voices',voices[1].id)
        self.conn=mysql.connector.connect(
            host="localhost",
            user="root",
            password="Taher@2002",
            database="ai"
        )
        self.working()
        
    def speak(self,to_say):
        self.engine.say(to_say)
        self.engine.runAndWait()
        
    def print_loop():
        print("\rListening....",end="",flush=True)
    def takeCommand(self):
        r=sr.Recognizer()
        r.dynamic_energy_threshold=False
        r.dynamic_energy_threshold=1000
        r.dynamic_energy_adjustment_damping=0.016
        r.dynamic_energy_ratio=1.0
        r.pause_threshold=0.5
        r.operation_timeout=None
        r.pause_threshold=0.6
        r.non_speaking_duration=0.5
        
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            while True:
                os.system("cls" if os.name=="nt" else "clear")
                print("\rListening...",end="",flush=True)
                try:
                    audio=r.listen(source,timeout=None)
                    print("\rRecognizing...",end="",flush=True)
                    query=r.recognize_google(audio,language="en-in")
                    if query:
                        print("\nCommand :- "+query,flush=True)
                        return query
                    else: return ""
                
                except sr.UnknownValueError:
                    query=""
                
                finally:
                    print("\r",end="",flush=True)
                    
            stt_thread=threading.Thread(target=takeCommand())
            print_thread=threading.Thread(target=print_loop)
            stt_thread.start()
            print_thread.start()
            stt_thread.join()
            print_thread.join()
    def working(self):
        greet=working.wishMe()
        self.speak(f"{greet} sir")
        while True:
            ### all logic will be here
            #### user will give the command and on the basis of that command respective funtion will be called from working.py
            command=self.takeCommand()
            # command="lets change your name"
            command=command.lower()
            command=command.split()
            

            if("None" in command):
                pass
            elif("hello" in command and "what" not in command):
                self.speak("hello sir!!")
                
            elif(("play" in command and ("song" in command or "songs" in command)) or ("random" in command and ("song" in command or "songs" in command))):
                # working on this module
                if(command[-1]=="song" or command[-1]=="songs"):
                    self.speak("playing song according to your taste sir....")
                    # almost done
                    working.play_song(self.conn)
                    
                else:
                    str_name=""
                    for i in range(command.index("song")+1 ,len(command)):
                        str_name+=f"{command[i]} "
                    working.particular_song(self.conn,str_name)
            
            elif(("show" in command or "display" in command) and ("song" in command or "songs" in command)):
                working.show_music_name(self.conn)
                time.sleep(3)
                self.speak("do you want me to play any of these songs ?")
                ans_yes_no=input("do you want me to play any of these songs ? :- ")
                if("yes" in ans_yes_no):
                    self.speak("playing song sir !!!")
                    working.play_song(self.conn)
                else:
                    self.speak("Okay sir")
                
                
            elif("stop" in command and "song" in command):
                working.stop_song(self.conn)
            
            if("sleep" in command or "exit" in command or "quit" in command):
                used_name=working.check_name(self.conn,command)
                if(used_name!="none"):
                    real_name=working.your_name(self.conn)        
                    time.sleep(0.3)
                    self.speak(f"sorry sir, but my name is {real_name} and not {used_name}")
                working.closing_tasks(self.conn)
                break
                     
brain=Brain()
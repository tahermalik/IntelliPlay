import datetime as dt
import random
import webbrowser as wb
from pynput import mouse
from pynput.mouse import Controller,Button
import keyboard as kb
import time
import Levenshtein
import pyautogui as pag
import os

def wishMe():
    hour=dt.datetime.now().hour
    if(hour>=6 and hour<=11):
        return "Good Morning"
    elif(hour>=12 and hour<=15):
        return "Good Afternoon"
    elif(hour>=16 and hour<=23):
        return "Good Evening"
    else:
        return "what is the problem"

def your_name(conn):
    cursor=conn.cursor()
    cursor.execute("select*from name")
    row=cursor.fetchone()
    if(row[0]=="none"):
        return "not yet decided"
    else:
        return row[0]
    
    
def check_name(conn,command):
    cursor=conn.cursor()
    cursor.execute("select*from previous_names")
    result=cursor.fetchall()
    names_list=[i[0] for i in result]
    for i in names_list:
        for j in command:
            if(i==j): return j
    return "none"

   
def min_mid_max(conn):
    cursor=conn.cursor()
    cursor.execute("select*from counter_win")
    result=cursor.fetchone()   
    if(int(result[0])==0):
        for _ in range(int(result[0])+1):
            pag.hotkey('win','up')
            time.sleep(0.2)
    cursor.execute("update counter_win set num_win_up_down=2")
    conn.commit()

def particular_song(conn,song_name):
    cursor=conn.cursor()
    wb.open_new_tab(f"https://www.youtube.com/results?search_query={song_name.replace(' ','+')}")
    time.sleep(2)
    min_mid_max(conn)
    x_coordinate=531
    y_coordinate=683
    mouse_controller=Controller()
    mouse_controller.position=(x_coordinate,y_coordinate)
    
    mouse_controller.click(button=Button.left)
    
    time.sleep(2)
    pag.hotkey('win','down')
    time.sleep(0.2)
    pag.hotkey('win','down')
    time.sleep(0.3)
    
    cursor.execute("select*from song_db")
    result=cursor.fetchall()
    song_list=[i[1] for i in result]
    id_list=[i[0] for i in result]
    flag=calculate_similarity(song_list,song_name)
    if(len(result)>=10 and flag==0):
        cursor.execute(f"delete from song_db where id={id_list[0]}")
        
    if(flag==0):
        cursor.execute(f"insert into song_db(song_name) values ('{song_name}')")
    conn.commit()
        
def calculate_similarity(song_list,song_name):
    for i in song_list:
        distance=Levenshtein.distance(i,song_name)
        max_len=max(len(i),len(song_name))
        similarity=(1-distance/max_len)
        
        if(similarity>=0.80):
            # print(similarity)
            return 1
    return 0
        
def play_song(conn,song_name=None):
    if(song_name==None):
        cursor=conn.cursor()
        cursor.execute("select*from song_db")
        result=cursor.fetchall()
        conn.commit()
        list_of_songs=[i[1] for i in result]
        index_of_song=random.randint(0,len(list_of_songs)-1)
        song_name=list_of_songs[index_of_song] # this song need to be played

    wb.open_new_tab(f"https://www.youtube.com/results?search_query={song_name.replace(' ','+')}")
    time.sleep(2)
    min_mid_max(conn)
    x_coordinate=531
    y_coordinate=683
    mouse_controller=Controller()
    mouse_controller.position=(x_coordinate,y_coordinate)
    
    mouse_controller.click(button=Button.left)
    
    time.sleep(2)
    pag.hotkey('win','down')
    time.sleep(0.2)
    pag.hotkey('win','down')
    # with mouse.Listener(on_click=on_click) as listener:
    #     listener.join()
    
# def on_click(x,y,button,pressed):
#     if pressed:
#         print(f"Mouse clicked ar : x={x} and y={y}")
#         return False
    
    
def show_music_name(conn):
    cursor=conn.cursor()
    cursor.execute("select*from song_db")
    result=cursor.fetchall()
    conn.commit()
    for index,song_name in enumerate(result):
        print(f"{index+1} --> {song_name[1]}")
        
def stop_song(conn):
    os.system("taskkill /im msedge.exe")
    os.system("cls" if os.name=="nt" else "clear")
    time.sleep(0.2)
    cursor=conn.cursor()
    cursor.execute("update counter_win set num_win_up_down=0")
    conn.commit()
       
def closing_tasks(conn):
    os.system("taskkill /im msedge.exe")
    os.system("cls" if os.name=="nt" else "clear")
    cursor=conn.cursor()
    cursor.execute("update counter_win set num_win_up_down=0")
    conn.commit()

        




    
    
    
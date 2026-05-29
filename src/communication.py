from config import get_config
import select
import sys
import os
import pygame
import random
from Animation import start_speaking, EyesGosTo, EyesGoLeft, EyeGoRight, EyesFoCenter

def StopStartRobot():
    DataVariables = get_config()
    conn = DataVariables.conn
    if conn is not None:
        try:
            conn.sendall(f"{DataVariables.left_button_state}\n".encode())
        except Exception as e:
            print("Error sending:", e)

    if DataVariables.left_button_state == "Stop":
        handle_robot_command("eye buttonp")
    else:
        handle_robot_command("eye buttons")
        
##############################################
######### Handle TERMINAL input  (New version)
##############################################
def handle_terminal_input_and_talk_to_java():
    DataVariables = get_config()
    if select.select([sys.stdin], [], [], 0)[0]:
        user_input = sys.stdin.readline().strip()
        if user_input:
            if DataVariables.no_socket:
                handle_robot_command(user_input)  # go directly to face
            else:
                if DataVariables.conn == None : 
                    raise Exception("No connection available. Cannot send data to Java.")
                else :
                    DataVariables.conn.sendall((user_input + "\n").encode())  

##############################################
######### play sound form Audios #############
##############################################
def playsound(name):

    DataVariables = get_config()
    
    actual_name = getattr(DataVariables.audio_register, name, None)
    if actual_name is None:
        print(f"Command '{name}' not found in audio register.")
        return
    
    file_path = os.path.join(DataVariables.audio_dir, actual_name)
    print(f"Playing sound: {file_path}")
    
    DataVariables.STOP_SPEAKING_EVENT = pygame.USEREVENT + 1
    if os.path.exists(file_path):
        sound = pygame.mixer.Sound(file_path)
        length_in_seconds = sound.get_length()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        start_speaking(int(length_in_seconds))
        pygame.time.set_timer(DataVariables.STOP_SPEAKING_EVENT, int(length_in_seconds) * 1000 + 400)
    else:
        print(f"Sound not found: {file_path}")
        
##############################################
######### play sound form Audios #############
##############################################
def playsound2(input):
    DataVariables = get_config()
    
    sound_files = {
        "rb": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/rb.mp3",
        "kb": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/kb.mp3",
        "gb": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/gb.mp3",
        "rs": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/rs.mp3",
        "gs": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/gs.mp3",
        "ks": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/ks.mp3",
        "Aus3": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/Aus3.mp3",
        "On8": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/On8.mp3",
        "Aus2": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/Aus2.mp3",
        "On7": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/On7.mp3",
        "On6": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/On6.mp3",
        "On5": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/On5.mp3",
        "On4": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/On4.mp3",
        "On3": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/On3.mp3",
        "g2": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/g2.mp3",
        "g1": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/g1.mp3",
        "boxfull": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/boxfull.mp3",
        "leermagazine": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/leermagazine.mp3",
        "Aus1": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/Aus1.mp3",
        "On1": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/On1.mp3",
        "On2": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/On2.mp3",
        "ns" : "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/leermagazine.mp3",
        "buttonp": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/buttonp.mp3",
        "buttons": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/buttons.mp3"
    }


    DataVariables.STOP_SPEAKING_EVENT = pygame.USEREVENT + 1
    if input in sound_files:
        file_path = sound_files[input]
        sound = pygame.mixer.Sound(file_path)
        length_in_seconds = sound.get_length()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        start_speaking(int(length_in_seconds))
        pygame.time.set_timer(DataVariables.STOP_SPEAKING_EVENT, int(length_in_seconds)*1000 + 400)  # 3000 ms = 3 sec

    else:
        print("Input not recognized.")
        
def robot_listener_thread():
    DataVariables = get_config()
    conn = DataVariables.conn
    while DataVariables.running:
        try:
            ready, _, _ = select.select([conn], [], [], 0.1)
            if ready:
                data = conn.recv(1024)
                if data:
                    strData = data.decode().strip()
                    handle_robot_command(strData)
        except Exception:
            continue
        
##############################################
######### Handle input from Roboter /Java ####
##############################################

def handle_robot_command(user_input):
    DataVariables = get_config()
    command = user_input.strip()
    print("received command:", command)

    # ── Eye commands ──────────────────────────────────────
    if command.startswith("eye "):
        value = command[4:].strip()
        if value == "left":     EyesGoLeft()
        elif value == "right":  EyeGoRight()
        elif value == "center": EyesFoCenter()
        elif value.isdigit():   EyesGosTo(int(value))
        else: print(f"Unknown eye command: {value}")
        return

    # ── Sound commands ────────────────────────────────────
    if command.startswith("sound "):
        if not DataVariables.SpeakAllowed:
            return
        value = command[6:].strip()
        # s o u n d ' '
        # 1 2 3 4 5 6
        playsound(value)
        return

    print(f"Unknown command: {command}")
    

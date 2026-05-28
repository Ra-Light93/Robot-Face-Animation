from config import get_config
import select
import sys
import pygame
import random
from Animation import start_speaking, EyesGosTo

def StopStartRobot():
    DataVariables = get_config()
    conn = DataVariables.conn
    if conn is not None:
        try:
            conn.sendall(f"{DataVariables.left_button_state}\n".encode())
        except Exception as e:
            print("Error sending:", e)

    if DataVariables.left_button_state == "Stop":
        handle_input_from_java("buttonp")
    else:
        handle_input_from_java("buttons")
        
##############################################
######### Handle TERMINAL input  (New version)
##############################################
def handle_terminal_input_and_talk_to_java():
    DataVariables = get_config()
    if select.select([sys.stdin], [], [], 0)[0]:
        user_input = sys.stdin.readline().strip()
        if user_input:
            if DataVariables.no_socket:
                handle_input_from_java(user_input)  # go directly to face
            else:
                if DataVariables.conn == None : 
                    raise Exception("No connection available. Cannot send data to Java.")
                else :
                    DataVariables.conn.sendall((user_input + "\n").encode())  

##############################################
######### play sound form Audios #############
##############################################
def playsound(input):
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
                    handle_input_from_java(strData)
        except Exception:
            continue
        
##############################################
######### Handle input from Roboter /Java ####
##############################################

def handle_input_from_java(user_input):
    DataVariables = get_config()
    input = user_input.strip().lower()
    print("recived form Robot :", input)
    if DataVariables.SpeakAllowed :
        if input == "gs":
            playsound("gs")
        elif input == "ks":
            playsound("ks")
        elif input == "rs":
            playsound("rs")
        elif input == "gb":
            playsound("gb")
        elif input == "kb":
            playsound("kb")
        elif input == "rb":
            playsound("rb")
        elif input == "ns":
            playsound("ns")
        elif input == "g":
            Random_Num = random.randint(1, 2)
            randomOn = "g" + str(Random_Num)
            playsound(randomOn)
        elif input == "on":
            print("System an")
            playsound("On1");
        elif input == "off":
            print("System aus")
            Random_Num = random.randint(1, 3)
            randomOn = "Aus" + str(Random_Num)
            playsound(randomOn);
        elif input == "buttonp":
            playsound("buttonp")
        elif input == "buttons":
            playsound("buttons")

    if input.isdigit():
        MovtoValue = int(input) - 45
        if MovtoValue > 45:
            print("Invalid: Value too high.")
        elif MovtoValue < -45:
            print("Invalid: Value too low.")
        else:
            EyesGosTo(MovtoValue)

    else:
        print("Unbekannter Befehl (ignore) :", input)


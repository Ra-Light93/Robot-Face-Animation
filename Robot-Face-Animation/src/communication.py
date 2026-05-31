from config import get_config
import select
import sys
import os
import pygame
import random
from Animation import start_speaking, EyesGosTo, EyesGoLeft, EyeGoRight, EyesFoCenter

def update_user(*messages: str):
    DataVariables = get_config()
    message = " ".join(str(m) for m in messages)
    if DataVariables.conn is not None:
        try:
            DataVariables.conn.sendall((message + "\n").encode())
        except Exception as e:
            print(f"Failed to send to Java: {e}")
    else:
        print(message)

def handle_terminal_input_and_talk_to_java():
    DataVariables = get_config()
    if select.select([sys.stdin], [], [], 0)[0]:
        user_input = sys.stdin.readline().strip()
        if user_input:
            if DataVariables.no_socket:
                handle_robot_command(user_input)
            else:
                if DataVariables.conn is None:
                    raise Exception("No connection available. Cannot send data to Java.")
                DataVariables.conn.sendall((user_input + "\n").encode())
                
def playsound(name):

    DataVariables = get_config()
    
    actual_name = getattr(DataVariables.audio_register, name, None)
    if actual_name is None:
        update_user(f"Command '{name}' not found in audio register.")
        return
    
    file_path = os.path.join(DataVariables.audio_dir, actual_name)
    
    DataVariables.STOP_SPEAKING_EVENT = pygame.USEREVENT + 1
    if os.path.exists(file_path):
        sound = pygame.mixer.Sound(file_path)
        length_in_seconds = sound.get_length()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        start_speaking(int(length_in_seconds))
        pygame.time.set_timer(DataVariables.STOP_SPEAKING_EVENT, int(length_in_seconds) * 1000 + 400)
    else:
        update_user(f"Sound not found: {file_path}")
                
def handle_robot_command(user_input):
    DataVariables = get_config()
    command = user_input.strip()
    if (not DataVariables.no_socket):
        print("received command:", command)

    # ── Eye commands ──────────────────────────────────────
    if command.startswith("eye "):
        value = command[4:].strip()
        if value == "left":     EyesGoLeft()
        elif value == "right":  EyeGoRight()
        elif value == "center": EyesFoCenter()
        elif value.isdigit():   EyesGosTo(int(value))
        else: 
            update_user(f"Unknown eye command: {value}")
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

    update_user(f"Unknown command: {command}")
    
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
                    print(f"From Java: '{strData}'")  # ← add this
                    handle_robot_command(strData)
        except Exception as e:
            update_user(f"Thread error: {e}")  # ← and this
            continue
    

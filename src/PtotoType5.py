import pygame
import sys
import socket
import threading
import argparse
from config import init_config, get_config
from Animation import (
    EyeGoRight, EyesGoLeft, EyesFoCenter, EyesGosTo,
    draw_face_border, draw_eyes, draw_mouth, draw_mouth_default, draw_mouth_speaking,
    blink_animation, 
    update_animation, update_mouth_animation,
    start_speaking, stop_speaking,
    draw_top_left_button, draw_top_right_button
) 
from communication import (
    handle_terminal_input_and_talk_to_java,
    playsound,
    robot_listener_thread,
)

 # Initialize config with screen dimensions
parser = argparse.ArgumentParser()
parser.add_argument('--no-socket', '-ns', action='store_true', help='Run without TCP connection (CLI only mode)')
args = parser.parse_args()

# Setup display
screen = pygame.display.set_mode((1000, 1000))
DataVariables = init_config(screen) 
DataVariables.no_socket = args.no_socket
DataVariables.screen = screen

pygame.display.set_caption("Robotic Face")
clock = pygame.time.Clock()


if not args.no_socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 30001))
    server_socket.listen(1)
    print("Waiting for connection...")
    conn, addr = server_socket.accept()
    DataVariables.conn = conn
    DataVariables.addr = addr
    DataVariables.server_socket = server_socket
    
    print("Connection from:", addr)
else:
    conn = None
    print("Running in --no-socket mode (CLI only)")
    
# Initialize pygame
pygame.init()


############################## Main Functions #############################################



##############################################
######### Handel Termination Events ##########
##############################################
def HandleEvents():
    # Handle cancel oder quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if DataVariables.conn is not None:
                DataVariables.conn.close()
                DataVariables.server_socket.close()
            print("Connection closed")
            DataVariables.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                DataVariables.running = False
        elif event.type == DataVariables.STOP_SPEAKING_EVENT:
            stop_speaking()


print("Controls: Type 'left', 'right', or 'center'. Or enter a number (0-90) for precise position.\nYou can Type \"speake\" and \"stop speake\" to move the Mouth")


##############################################
#### start Thread To observe Robot Commands ##
##############################################

threading.Thread(target=robot_listener_thread, daemon=True).start()

# play sonund "Ich bin jetzt an !"
playsound("On1");

##############################################
#### Enter Main Loop ##########################
##############################################
while DataVariables.running or pygame.mixer.music.get_busy():
    HandleEvents()
    handle_terminal_input_and_talk_to_java()

    # Clear screen
    screen.fill(DataVariables.BG)

    # Draw face
    draw_face_border()

    # Update animations
    blink_animation()
    update_animation()
    update_mouth_animation()

    # Draw face components
    draw_eyes()
    draw_mouth()

    # Draw Buttons
    draw_top_left_button()  # Red terminate button
    draw_top_right_button()  # Blue sound button

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()
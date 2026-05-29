import pygame
import sys
import socket
import threading
import argparse
from config import init_config
from Animation import (
    draw_face_border, draw_eyes, draw_mouth,
    blink_animation,
    update_animation, update_mouth_animation,
    stop_speaking,
    draw_top_right_button
)
from communication import (
    handle_terminal_input_and_talk_to_java,
    robot_listener_thread,
)

# ── Args ────────────────────────────────────────────────
parser = argparse.ArgumentParser()
parser.add_argument('--no-socket', '-ns', action='store_true',
                    help='Run without TCP connection (CLI only mode)')
args = parser.parse_args()

# ── Pygame setup ─────────────────────────────────────────
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()

# ── Config ───────────────────────────────────────────────
DataVariables = init_config(screen)
DataVariables.no_socket = args.no_socket
DataVariables.screen = screen
pygame.display.set_caption(DataVariables.pygame_title)

# ── Socket setup ─────────────────────────────────────────
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
    print("Running in --no-socket mode (CLI only)")

# ── Event handler ────────────────────────────────────────
def handle_events():
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

# ── Startup ──────────────────────────────────────────────

print("\n")
print("=" * 55)
print("  ROBOT FACE — CLI MODE")
print("=" * 55)
print("  Use 'eye' commands to control eye movement:")
print("    eye left   — look left")
print("    eye right  — look right")
print("    eye center — look center")
print("    eye 0-90   — precise position (45 = center)")
print("─" * 55)
print("  Use 'sound' commands to play registered audio:")
print("    sound <name> — plays <name>.mp3 from Audios/")
print("─" * 55)
print("  Audio files are registered in Audios/audio_register.json")
print("=" * 55)







# ── Main loop ────────────────────────────────────────────
while DataVariables.running or pygame.mixer.music.get_busy():
    handle_events()
    handle_terminal_input_and_talk_to_java()

    screen.fill(DataVariables.BG)
    draw_face_border()
    blink_animation()
    update_animation()
    update_mouth_animation()
    draw_eyes()
    draw_mouth()
    draw_top_right_button()

    pygame.display.flip()
    clock.tick(60)

# ── Cleanup ──────────────────────────────────────────────
pygame.quit()
sys.exit()
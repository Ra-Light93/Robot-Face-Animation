from config import get_config
import pygame
import math
from communication import StopStartRobot

def draw_top_right_button():
    DataVariables = get_config()
    screen = DataVariables.screen
    button_radius = 25
    button_center = (screen.get_width() - 50, 45)  # Position rechts

    # Hover und Click Effekte
    mouse_pos = pygame.mouse.get_pos()
    distance = math.sqrt((mouse_pos[0] - button_center[0]) ** 2 + (mouse_pos[1] - button_center[1]) ** 2)
    is_hovered = distance <= button_radius
    is_clicked = pygame.mouse.get_pressed()[0] and is_hovered

    # Button Farbe (Blau)
    base_color = (70, 130, 200)
    current_color = (50, 110, 180) if is_clicked else (90, 150, 220) if is_hovered else base_color

    # Button zeichnen
    pygame.draw.circle(screen, (30, 30, 30, 150), (button_center[0] + 3, button_center[1] + 3), button_radius)
    pygame.draw.circle(screen, current_color, button_center, button_radius)

    # Audio Symbol (Wellenform oder durchgestrichen)
    symbol_color = (240, 240, 240)
    if DataVariables.right_button_state == "sound_on":
        # Wellenform Symbol
        wave_points = [
            (button_center[0] - 12, button_center[1] + 5),
            (button_center[0] - 8, button_center[1] - 8),
            (button_center[0] - 4, button_center[1] + 2),
            (button_center[0], button_center[1] - 5),
            (button_center[0] + 4, button_center[1] + 0),
            (button_center[0] + 8, button_center[1] - 3),
            (button_center[0] + 12, button_center[1] + 6)
        ]
        pygame.draw.lines(screen, symbol_color, False, wave_points, 2)
    else:
        # Durchgestrichenes Symbol
        wave_points = [
            (button_center[0] - 12, button_center[1] + 5),
            (button_center[0] - 8, button_center[1] - 8),
            (button_center[0] - 4, button_center[1] + 2),
            (button_center[0], button_center[1] - 5),
            (button_center[0] + 4, button_center[1] + 0),
            (button_center[0] + 8, button_center[1] - 3),
            (button_center[0] + 12, button_center[1] + 6)
        ]
        pygame.draw.lines(screen, symbol_color, False, wave_points, 2)
        pygame.draw.line(screen, (255, 60, 60),
                         (button_center[0] - 15, button_center[1] - 15),
                         (button_center[0] + 15, button_center[1] + 15), 3)

    # Klick-Handler
    if is_clicked and not hasattr(DataVariables, 'right_button_click_time'):
        DataVariables.right_button_click_time = pygame.time.get_ticks()
        DataVariables.right_button_state = "sound_off" if DataVariables.right_button_state == "sound_on" else "sound_on"
        DataVariables.SpeakAllowed = not DataVariables.SpeakAllowed

    # Ripple-Effekt
    if hasattr(DataVariables, 'right_button_click_time'):
        elapsed = pygame.time.get_ticks() - DataVariables.right_button_click_time
        if elapsed < 500:
            ripple_radius = int(elapsed // 5)
            ripple_alpha = max(0, 150 - (elapsed // 3))
            ripple_surf = pygame.Surface((ripple_radius * 2, ripple_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(ripple_surf, (*current_color, ripple_alpha),
                               (ripple_radius, ripple_radius), ripple_radius)
            screen.blit(ripple_surf, (button_center[0] - ripple_radius,
                                      button_center[1] - ripple_radius))
        else:
            delattr(DataVariables, 'right_button_click_time')

def draw_top_left_button():
    DataVariables = get_config()
    screen = DataVariables.screen
    button_radius = 25
    button_center = (50, 45)  # Position links

    # Hover und Click Effekte
    mouse_pos = pygame.mouse.get_pos()
    distance = math.sqrt((mouse_pos[0] - button_center[0]) ** 2 + (mouse_pos[1] - button_center[1]) ** 2)
    is_hovered = distance <= button_radius
    is_clicked = pygame.mouse.get_pressed()[0] and is_hovered

    # Button Farbe (Grün)
    base_color = (80, 180, 80)
    current_color = (60, 160, 60) if is_clicked else (100, 200, 100) if is_hovered else base_color

    # Button zeichnen
    pygame.draw.circle(screen, (30, 30, 30, 150), (button_center[0] + 3, button_center[1] + 3), button_radius)
    pygame.draw.circle(screen, current_color, button_center, button_radius)

    # Play/Pause Symbol
    symbol_color = (240, 240, 240)
    if DataVariables.left_button_state == "Start":
        # Play Symbol (Dreieck)
        play_points = [
            (button_center[0] - 8, button_center[1] - 10),
            (button_center[0] - 8, button_center[1] + 10),
            (button_center[0] + 12, button_center[1])
        ]
        pygame.draw.polygon(screen, symbol_color, play_points)
    else:
        # Pause Symbol
        pygame.draw.rect(screen, symbol_color, (button_center[0] - 12, button_center[1] - 10, 8, 20))
        pygame.draw.rect(screen, symbol_color, (button_center[0] + 4, button_center[1] - 10, 8, 20))

    # Klick-Handler
    if is_clicked and not hasattr(DataVariables, 'left_button_click_time'):
        DataVariables.left_button_click_time = pygame.time.get_ticks()
        StopStartRobot()  # Deine bestehende Funktion
        DataVariables.left_button_state = "Stop" if DataVariables.left_button_state == "Start" else "Start"


    # Ripple-Effekt
    if hasattr(DataVariables, 'left_button_click_time'):
        elapsed = pygame.time.get_ticks() - DataVariables.left_button_click_time
        if elapsed < 500:
            ripple_radius = int(elapsed // 5)
            ripple_alpha = max(0, 150 - (elapsed // 3))
            ripple_surf = pygame.Surface((ripple_radius * 2, ripple_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(ripple_surf, (*current_color, ripple_alpha),
                               (ripple_radius, ripple_radius), ripple_radius)
            screen.blit(ripple_surf, (button_center[0] - ripple_radius,
                                      button_center[1] - ripple_radius))
        else:
            delattr(DataVariables, 'left_button_click_time')
       
       


import pygame
import math
import sys
from types import SimpleNamespace

# Initialize pygame
pygame.init()

# Create namespace for all variables
V = SimpleNamespace()

# Setup display
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Smiling Robotic Face")
clock = pygame.time.Clock()

# Size parameters
V.FaceSize = 1

# Color palette
V.BG = (240, 240, 245)  # Light gray background
V.WHITE = (255, 255, 255)
V.BLACK = (0, 0, 0)
V.EYE_WHITES = (250, 250, 255)
V.IRIS_COLOR = (0, 150, 255)  # Vibrant blue
V.PUPIL_COLOR = (0, 0, 0)
V.MOUTH_COLOR = (220, 70, 80)  # Reddish smile
V.MOUTH_INNER = (180, 50, 60)
V.MOUTH_HIGHLIGHT = (255, 150, 150)

# Eye dimensions
V.BASE_EYE_WIDTH = 120
V.BASE_EYE_HEIGHT = 60
V.BASE_IRIS_RADIUS = 25
V.BASE_PUPIL_RADIUS = 8
V.BASE_MOUTH_WIDTH = 200
V.BASE_MOUTH_HEIGHT = 100

# Calculate scaled dimensions
V.eye_width = int(V.BASE_EYE_WIDTH * V.FaceSize)
V.eye_height = int(V.BASE_EYE_HEIGHT * V.FaceSize)

# Eye positions
eye_spacing = 220 * V.FaceSize
V.left_eye_pos = (screen.get_width() / 2 - eye_spacing / 2,
                  screen.get_height() / 2 - 50 * V.FaceSize)
V.right_eye_pos = (screen.get_width() / 2 + eye_spacing / 2,
                   screen.get_height() / 2 - 50 * V.FaceSize)

# Iris parameters
V.iris_radius = int(V.BASE_IRIS_RADIUS * V.FaceSize)
V.pupil_radius = int(V.BASE_PUPIL_RADIUS * V.FaceSize)
V.iris_shrink = 0.9

# Animation control
V.pupil_offset_x = 0
V.target_offset = 0
V.move_speed = 3
V.blink_duration = 0
V.max_swing = (V.eye_width // 2) - V.iris_radius

# Mouth parameters
V.mouth_width = int(V.BASE_MOUTH_WIDTH * V.FaceSize)
V.mouth_height = int(V.BASE_MOUTH_HEIGHT * V.FaceSize)
V.mouth_pos = (screen.get_width() / 2,
               screen.get_height() / 2 + 80 * V.FaceSize)
V.smile_progress = 1.0  # 0.0 = neutral, 1.0 = full smile

V.running = True


def EyeGoRight():
    V.target_offset = V.max_swing


def EyesGoLeft():
    V.target_offset = -V.max_swing


def EyesFoCenter():
    V.target_offset = 0


def EyesGosTo(topos):
    V.target_offset = topos


def SetSmile(amount):
    V.smile_progress = max(0.0, min(1.0, amount))


def handle_input_in_arg():
    import sys
    import select

    if select.select([sys.stdin], [], [], 0)[0]:
        user_input = sys.stdin.readline().strip().lower()
        if user_input == "left":
            EyesGoLeft()
        elif user_input == "right":
            EyeGoRight()
        elif user_input == "center":
            EyesFoCenter()
        elif user_input == "smile":
            SetSmile(1.0)
        elif user_input == "neutral":
            SetSmile(0.0)
        elif user_input.isdigit():
            MovtoValue = int(user_input) - 45
            if MovtoValue > 45:
                print("Invalid: Value too high.")
            elif MovtoValue < -45:
                print("Invalid: Value too low.")
            else:
                EyesGosTo(MovtoValue)


def quit_if_necessary():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            V.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                V.running = False
            elif event.key == pygame.K_s:
                SetSmile(1.0)
            elif event.key == pygame.K_n:
                SetSmile(0.0)


def blink_animation():
    if V.blink_duration > 0:
        V.blink_duration -= 1
    elif pygame.time.get_ticks() % 120 == 0:
        V.blink_duration = 8


def update_animation():
    # Smooth eye movement
    if V.pupil_offset_x < V.target_offset:
        V.pupil_offset_x = min(V.pupil_offset_x + V.move_speed, V.target_offset)
    elif V.pupil_offset_x > V.target_offset:
        V.pupil_offset_x = max(V.pupil_offset_x - V.move_speed, V.target_offset)

    # Calculate blink progress
    V.blink_progress = min(1, V.blink_duration / 5)
    V.blink_height = max(5, V.eye_height * (1 - V.blink_progress))


def draw_eyes():
    for pos in [V.left_eye_pos, V.right_eye_pos]:
        # Eye container
        eye_rect = pygame.Rect(
            pos[0] - V.eye_width // 2,
            pos[1] - V.blink_height // 2,
            V.eye_width,
            V.blink_height
        )

        # Draw eye white with border
        pygame.draw.rect(screen, V.EYE_WHITES, eye_rect, border_radius=10)
        pygame.draw.rect(screen, V.BLACK, eye_rect, 2, border_radius=10)

        # Calculate iris position and size
        iris_x = pos[0] + V.pupil_offset_x * 0.7
        iris_y = pos[1]
        current_iris_radius = V.iris_radius * (
                1 - (abs(V.pupil_offset_x) / V.max_swing * (1 - V.iris_shrink)))

        # Draw iris
        pygame.draw.circle(screen, V.IRIS_COLOR, (int(iris_x), int(iris_y)),
                           int(current_iris_radius))

        # Draw pupil
        pygame.draw.circle(screen, V.PUPIL_COLOR, (int(iris_x), int(iris_y)),
                           V.pupil_radius)

        # Eye highlight
        highlight_pos = (iris_x - current_iris_radius // 2,
                         iris_y - current_iris_radius // 2)
        pygame.draw.circle(screen, V.WHITE, highlight_pos, current_iris_radius // 3)


def draw_smile():
    # Calculate smile parameters based on progress
    smile_width = V.mouth_width * (0.8 + 0.2 * V.smile_progress)
    curve_height = V.mouth_height * (0.5 + 1.5 * V.smile_progress)
    y_offset = V.mouth_height * (0.3 - 0.3 * V.smile_progress)

    # Draw main smile arc
    smile_rect = [
        V.mouth_pos[0] - smile_width // 2,
        V.mouth_pos[1] - y_offset,
        smile_width,
        curve_height
    ]

    # Draw the smiling mouth with highlights
    pygame.draw.arc(screen, V.MOUTH_COLOR, smile_rect,
                    math.pi * 0.15, math.pi * 0.85, 10)

    # Draw inner mouth (tongue-like area)
    inner_rect = [
        V.mouth_pos[0] - smile_width * 0.4,
        V.mouth_pos[1] - y_offset * 0.5,
        smile_width * 0.8,
        curve_height * 0.7
    ]
    pygame.draw.arc(screen, V.MOUTH_INNER, inner_rect,
                    math.pi * 0.2, math.pi * 0.8, 0)

    # Add highlights to make it shiny
    highlight_rect = [
        V.mouth_pos[0] - smile_width * 0.2,
        V.mouth_pos[1] - y_offset - curve_height * 0.3,
        smile_width * 0.4,
        curve_height * 0.3
    ]
    pygame.draw.arc(screen, V.MOUTH_HIGHLIGHT, highlight_rect,
                    math.pi * 0.2, math.pi * 0.8, 2)


# Main game loop
print("Controls:")
print("Type 'left', 'right', or 'center' to move eyes")
print("Type 'smile' or 'neutral' to change expression")
print("Or enter a number (0-90) for precise eye position")
print("Press 'S' key to smile, 'N' for neutral face")

while V.running:
    quit_if_necessary()
    handle_input_in_arg()

    # Clear screen
    screen.fill(V.BG)

    # Update animations
    blink_animation()
    update_animation()

    # Draw face components
    draw_eyes()
    draw_smile()

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()
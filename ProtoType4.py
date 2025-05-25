import random

import pygame
import math
import sys
from types import SimpleNamespace

# Initialize pygame
pygame.init()

# Create namespace for all variables
DataVariables = SimpleNamespace()

# Setup display
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Robotic Face")
clock = pygame.time.Clock()

# Size parameters
DataVariables.FaceSize = 1

# Color palette
DataVariables.BG = (240, 240, 245)  # Light gray background
DataVariables.WHITE = (255, 255, 255)
DataVariables.BLACK = (0, 0, 0)
DataVariables.EYE_WHITES = (250, 250, 255)
DataVariables.IRIS_COLOR = (0, 150, 255)  # Vibrant blue
DataVariables.PUPIL_COLOR = (0, 0, 0)
DataVariables.MOUTH_COLOR = (0, 140, 255)  # Electric blue
DataVariables.EYEBORDEAR_COLOR = (0, 0, 0)  # Black
DataVariables.MOUTH_INNER = (80, 80, 100)
DataVariables.MOUTH_ACCENT = (150, 150, 170)

# Eye dimensions
DataVariables.BASE_EYE_WIDTH = 120
DataVariables.BASE_EYE_HEIGHT = 60  # More rectangular shape
DataVariables.BASE_IRIS_RADIUS = 25
DataVariables.BASE_PUPIL_RADIUS = 8
DataVariables.BASE_MOUTH_WIDTH = 180
DataVariables.BASE_MOUTH_HEIGHT = 40

# Updated shape parameters and drawing functions
DataVariables.FACE_SHAPE = "hexagon"  # hexagon, octagon, or rectangle
DataVariables.FACE_WIDTH = 550
DataVariables.FACE_HEIGHT = 700
DataVariables.FACE_CORNER_RADIUS = 80
DataVariables.FACE_BORDER_THICKNESS = 12
DataVariables.FACE_COLOR = (220, 225, 235)
DataVariables.FACE_BORDER_COLOR = (80, 90, 110)
DataVariables.FACE_ACCENT_COLOR = (150, 160, 180)

# Calculate scaled dimensions
DataVariables.eye_width = int(DataVariables.BASE_EYE_WIDTH * DataVariables.FaceSize)
DataVariables.eye_height = int(DataVariables.BASE_EYE_HEIGHT * DataVariables.FaceSize)

# Face position
DataVariables.face_pos = (screen.get_width() // 2, screen.get_height() // 2)

# Eye positions
eye_spacing = 220 * DataVariables.FaceSize
DataVariables.left_eye_pos = (screen.get_width() / 2 - eye_spacing / 2,
                              screen.get_height() / 2 - 70 * DataVariables.FaceSize)

DataVariables.right_eye_pos = (screen.get_width() / 2 + eye_spacing / 2,
                               screen.get_height() / 2 - 70 * DataVariables.FaceSize)

# Iris parameters
DataVariables.iris_radius = int(DataVariables.BASE_IRIS_RADIUS * DataVariables.FaceSize)
DataVariables.pupil_radius = int(DataVariables.BASE_PUPIL_RADIUS * DataVariables.FaceSize)
DataVariables.iris_shrink = 0.9  # Less distortion when looking sideways

# Animation control
DataVariables.pupil_offset_x = 0
DataVariables.target_offset = 0
DataVariables.move_speed = 3  # Faster for robotic movement
DataVariables.blink_duration = 0
DataVariables.max_swing = (DataVariables.eye_width // 2) - DataVariables.iris_radius

# Mouth position
DataVariables.mouth_width = int(DataVariables.BASE_MOUTH_WIDTH * DataVariables.FaceSize)
DataVariables.mouth_height = int(DataVariables.BASE_MOUTH_HEIGHT * DataVariables.FaceSize)
DataVariables.mouth_pos = (screen.get_width() / 2,
                           screen.get_height() / 2 + 80 * DataVariables.FaceSize)

DataVariables.running = True


def EyeGoRight():
    DataVariables.target_offset = DataVariables.max_swing
def EyesGoLeft():
    DataVariables.target_offset = -DataVariables.max_swing
def EyesFoCenter():
    DataVariables.target_offset = 0
def EyesGosTo(topos):
    DataVariables.target_offset = topos
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
        elif user_input.isdigit():
            MovtoValue = int(user_input) - 45
            if MovtoValue > 45:
                print("Invalid: Value too high.")
            elif MovtoValue < -45:
                print("Invalid: Value too low.")
            else:
                EyesGosTo(MovtoValue)
        elif user_input == "speake":
            RobotSpeak(duration = 420, intensity = 4)  # 1 sec = 60 duraction

def quit_if_necessary():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            DataVariables.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                DataVariables.running = False


def blink_animation():
    if DataVariables.blink_duration > 0:
        DataVariables.blink_duration -= 1
    elif pygame.time.get_ticks() % 120 == 0:  # Random blinking
        DataVariables.blink_duration = 8  # Shorter blinks


def update_animation():
    # Smooth eye movement
    if DataVariables.pupil_offset_x < DataVariables.target_offset:
        DataVariables.pupil_offset_x = min(DataVariables.pupil_offset_x + DataVariables.move_speed,
                                           DataVariables.target_offset)
    elif DataVariables.pupil_offset_x > DataVariables.target_offset:
        DataVariables.pupil_offset_x = max(DataVariables.pupil_offset_x - DataVariables.move_speed,
                                           DataVariables.target_offset)

    # Calculate blink progress
    DataVariables.blink_progress = min(1, DataVariables.blink_duration / 5)
    DataVariables.blink_height = max(5, DataVariables.eye_height * (1 - DataVariables.blink_progress))


def draw_eyes():
    for pos in [DataVariables.left_eye_pos, DataVariables.right_eye_pos]:
        # Eye container (rectangular with rounded corners)
        eye_rect = pygame.Rect(
            pos[0] - DataVariables.eye_width // 2,
            pos[1] - DataVariables.blink_height // 2,
            DataVariables.eye_width,
            DataVariables.blink_height
        )

        # Draw eye white with metallic border
        pygame.draw.rect(screen, DataVariables.EYE_WHITES, eye_rect, border_radius=10)
        pygame.draw.rect(screen, DataVariables.EYEBORDEAR_COLOR, eye_rect, 2, border_radius=10)

        # Calculate iris position and size
        iris_x = pos[0] + DataVariables.pupil_offset_x * 0.7
        iris_y = pos[1]
        current_iris_radius = DataVariables.iris_radius * (
                1 - (abs(DataVariables.pupil_offset_x) / DataVariables.max_swing *
                     (1 - DataVariables.iris_shrink)))

        # Draw iris with concentric circles for robotic effect
        pygame.draw.circle(screen, DataVariables.IRIS_COLOR,
                           (int(iris_x), int(iris_y)), int(current_iris_radius))
        pygame.draw.circle(screen, (0, 100, 200),
                           (int(iris_x), int(iris_y)), int(current_iris_radius * 0.7), 1)
        pygame.draw.circle(screen, (0, 50, 150),
                           (int(iris_x), int(iris_y)), int(current_iris_radius * 0.4), 1)

        # Draw pupil
        pygame.draw.circle(screen, DataVariables.PUPIL_COLOR,
                           (int(iris_x), int(iris_y)), DataVariables.pupil_radius)

        # Eye highlight (more pronounced)
        highlight_pos = (iris_x - current_iris_radius // 2,
                         iris_y - current_iris_radius // 2)
        pygame.draw.circle(screen, DataVariables.WHITE,
                           highlight_pos, current_iris_radius // 3)


def draw_Sad_mouth():
    # Happy smile parameters
    smile_width = DataVariables.mouth_width * 1.5
    curve_height = 140  # More pronounced curve
    y_offset = 30  # Higher position = happier

    # Draw big, cheerful smile (single arc)
    pygame.draw.arc(
        screen,
        DataVariables.MOUTH_COLOR,
        [
            DataVariables.mouth_pos[0] - smile_width // 2,  # Center horizontally
            DataVariables.mouth_pos[1] - y_offset,  # Higher position
            smile_width,
            curve_height  # Curve height
        ],
        math.pi * 0.15,  # Wider angle (start at ~27 degrees)
        math.pi * 0.85,  # End at ~153 degrees
        6  # Thicker line
    )
def draw_Happy_mouth():
    smile_width = DataVariables.mouth_width * 1.5    # original : 0.8
    curve_height = 140                               # original : 0.8
    y_offset = 125                                 # original : 80

    pygame.draw.arc(
        screen,
        DataVariables.MOUTH_COLOR,
        [
            DataVariables.mouth_pos[0] - smile_width // 2,
            DataVariables.mouth_pos[1] - y_offset,
            smile_width,
            curve_height
        ],
        math.pi * 1.15,
        math.pi * 1.85,
        6
    )


def draw_face_border():
    center_x, center_y = DataVariables.face_pos
    outer_radius = 350
    inner_radius = 320
    tech_ring_radius = 300

    # Main face plate (circular with tech pattern)
    pygame.draw.circle(screen, (40, 45, 50), (center_x, center_y), outer_radius)
    pygame.draw.circle(screen, (30, 35, 40), (center_x, center_y), outer_radius - 3, 3)

    # Inner glowing face plate
    for i in range(3):
        radius = inner_radius - i * 15
        color = (60 + i * 15, 65 + i * 15, 70 + i * 15)
        pygame.draw.circle(screen, color, (center_x, center_y), radius)

    # Hexagonal tech pattern
    hex_size = 25
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        x = center_x + tech_ring_radius * math.cos(rad)
        y = center_y + tech_ring_radius * math.sin(rad)

        points = []
        for i in range(6):
            hex_angle = math.radians(60 * i + 30)
            hex_x = x + hex_size * math.cos(hex_angle)
            hex_y = y + hex_size * math.sin(hex_angle)
            points.append((hex_x, hex_y))

        pygame.draw.polygon(screen, (0, 150, 255, 100), points, 2)

    # Radial energy lines
    for i in range(0, 360, 15):
        rad = math.radians(i)
        start_x = center_x + (inner_radius - 50) * math.cos(rad)
        start_y = center_y + (inner_radius - 50) * math.sin(rad)
        end_x = center_x + (inner_radius - 20) * math.cos(rad)
        end_y = center_y + (inner_radius - 20) * math.sin(rad)

        color = (0, 200 + random.randint(0, 55), 255, 150)
        pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), 2)

    # Central power core glow
    for i in range(1, 4):
        radius = 15 * i
        alpha = 100 - i * 25
        glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (0, 150, 255, alpha),
                           (radius, radius), radius)
        screen.blit(glow_surface, (center_x - radius, center_y - radius))

    # Outer ring with connectors
    connector_points = []
    for i in range(0, 360, 45):
        rad = math.radians(i)
        x = center_x + (outer_radius + 10) * math.cos(rad)
        y = center_y + (outer_radius + 10) * math.sin(rad)
        connector_points.append((x, y))
        pygame.draw.circle(screen, (80, 90, 100), (x, y), 8)
        pygame.draw.circle(screen, (0, 180, 255), (x, y), 4)

    pygame.draw.polygon(screen, (60, 70, 80), connector_points, 3)

    # Bottom status lights
    for i, color in enumerate([(255, 0, 0), (255, 150, 0), (0, 255, 0)]):
        light_x = center_x - 60 + i * 60
        light_y = center_y + outer_radius - 20
        pygame.draw.circle(screen, (30, 30, 30), (light_x, light_y), 12)
        pygame.draw.circle(screen, color, (light_x, light_y), 8)


def RobotSpeak(duration=30, intensity=5):
    """Animate the mouth to simulate speaking"""
    if not hasattr(DataVariables, 'speak_timer'):
        # Initialize speaking variables if they don't exist
        DataVariables.speak_timer = 0
        DataVariables.speak_intensity = 0
        DataVariables.current_mouth_y_offset = 0
        DataVariables.mouth_animation_direction = 1

    DataVariables.speak_timer = duration
    DataVariables.speak_intensity = intensity
    DataVariables.current_mouth_y_offset = 0
    DataVariables.mouth_animation_direction = 1


def update_speaking_animation():
    if hasattr(DataVariables, 'speak_timer') and DataVariables.speak_timer > 0:
        DataVariables.speak_timer -= 1

        # Oscillate mouth position for speaking effect
        DataVariables.current_mouth_y_offset += DataVariables.mouth_animation_direction * 0.5
        if abs(DataVariables.current_mouth_y_offset) > DataVariables.speak_intensity:
            DataVariables.mouth_animation_direction *= -1
    else:
        # Reset values when not speaking
        if hasattr(DataVariables, 'current_mouth_y_offset'):
            DataVariables.current_mouth_y_offset = 0
def draw_speaking_mouth():
    # Use default mouth position if not speaking
    current_y_offset = DataVariables.current_mouth_y_offset if hasattr(DataVariables, 'current_mouth_y_offset') else 0

    # Convert all values to integers
    current_mouth_pos = (
        int(DataVariables.mouth_pos[0]),
        int(DataVariables.mouth_pos[1] + current_y_offset)
    )

    # Calculate mouth height and convert to integer
    mouth_height = int(DataVariables.mouth_height + abs(current_y_offset) * 2)

    # Create mouth rectangle with integer values
    mouth_rect = pygame.Rect(
        int(current_mouth_pos[0] - DataVariables.mouth_width // 2),
        int(current_mouth_pos[1] - mouth_height // 2),
        int(DataVariables.mouth_width),
        int(mouth_height)
    )

    # Draw main mouth shape with integer border radius
    pygame.draw.rect(screen, DataVariables.MOUTH_COLOR, mouth_rect,
                     border_radius=int(mouth_height // 2))
    pygame.draw.rect(screen, DataVariables.MOUTH_ACCENT, mouth_rect,
                     2, border_radius=int(mouth_height // 2))

    # Draw inner mouth details (teeth or lines)
    for i in range(5):
        line_y = int(mouth_rect.y + (i + 1) * (mouth_rect.height / 6))
        pygame.draw.line(screen, DataVariables.MOUTH_INNER,
                         (int(mouth_rect.x + 10), line_y),
                         (int(mouth_rect.x + mouth_rect.width - 10), line_y), 2)

# Main game loop
print("Controls: Type 'left', 'right', or 'center'. Or enter a number (0-90) for precise position.")

while DataVariables.running:
    quit_if_necessary()
    handle_input_in_arg()

    # Clear screen
    screen.fill(DataVariables.BG)

    # Draw face
    draw_face_border()

    # Update animations
    blink_animation()
    update_animation()
    update_speaking_animation()  # This updates the mouth movement

    # Draw face components
    draw_eyes()
    draw_speaking_mouth()  # Draw the animated speaking mouth

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()
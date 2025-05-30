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
DataVariables.MOUTH_COLOR = (100, 100, 120)  # Metallic gray
DataVariables.MOUTH_INNER = (80, 80, 100)
DataVariables.MOUTH_ACCENT = (150, 150, 170)

# Eye dimensions
DataVariables.BASE_EYE_WIDTH = 120
DataVariables.BASE_EYE_HEIGHT = 60  # More rectangular shape
DataVariables.BASE_IRIS_RADIUS = 25
DataVariables.BASE_PUPIL_RADIUS = 8
DataVariables.BASE_MOUTH_WIDTH = 180
DataVariables.BASE_MOUTH_HEIGHT = 40

# Calculate scaled dimensions
DataVariables.eye_width = int(DataVariables.BASE_EYE_WIDTH * DataVariables.FaceSize)
DataVariables.eye_height = int(DataVariables.BASE_EYE_HEIGHT * DataVariables.FaceSize)

# Eye positions
eye_spacing = 220 * DataVariables.FaceSize
DataVariables.left_eye_pos = (screen.get_width() / 2 - eye_spacing / 2,
                              screen.get_height() / 2 - 50 * DataVariables.FaceSize)
DataVariables.right_eye_pos = (screen.get_width() / 2 + eye_spacing / 2,
                               screen.get_height() / 2 - 50 * DataVariables.FaceSize)

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
        pygame.draw.rect(screen, DataVariables.MOUTH_COLOR, eye_rect, 2, border_radius=10)

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


def draw_robotic_smile():
    """Friendly robotic mouth with subtle smile"""
    # Main mouth rectangle
    mouth_rect = pygame.Rect(
        DataVariables.mouth_pos[0] - DataVariables.mouth_width // 2,
        DataVariables.mouth_pos[1] - DataVariables.mouth_height // 3,  # Slightly higher
        DataVariables.mouth_width,
        DataVariables.mouth_height
    )

    # Draw metallic mouth base
    pygame.draw.rect(screen, DataVariables.MOUTH_COLOR, mouth_rect, border_radius=15)
    pygame.draw.rect(screen, DataVariables.MOUTH_INNER, mouth_rect, 2, border_radius=15)

    # Draw smiling indicator line
    smile_width = DataVariables.mouth_width * 0.7
    pygame.draw.arc(screen, DataVariables.MOUTH_ACCENT,
                    [DataVariables.mouth_pos[0] - smile_width / 2,
                     DataVariables.mouth_pos[1] - DataVariables.mouth_height / 3,
                     smile_width,
                     DataVariables.mouth_height],
                    math.pi * 0.2, math.pi * 0.8, 3)

    # Add some small horizontal lines for tech detail
    for i in range(3):
        line_y = DataVariables.mouth_pos[1] + DataVariables.mouth_height // 4 - i * 8
        line_length = DataVariables.mouth_width * (0.4 + i * 0.1)
        pygame.draw.line(screen, DataVariables.MOUTH_ACCENT,
                         (DataVariables.mouth_pos[0] - line_length / 2, line_y),
                         (DataVariables.mouth_pos[0] + line_length / 2, line_y), 2)


# Main game loop
print("Controls: Type 'left', 'right', or 'center'. Or enter a number (0-90) for precise position.")
while DataVariables.running:
    quit_if_necessary()
    handle_input_in_arg()

    # Clear screen
    screen.fill(DataVariables.BG)

    # Update animations
    blink_animation()
    update_animation()

    # Draw face components
    draw_eyes()
    draw_robotic_smile()

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit() 
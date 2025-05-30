import pygame
import math
import sys

pygame.init()

from types import SimpleNamespace

DataVarabels = SimpleNamespace()

# Setup
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Robotic Face")
clock = pygame.time.Clock()

# Varable for assigning the size of the face
DataVarabels.FaceSize = 1

# Colors - more robotic/technical
DataVarabels.BG = (240, 240, 245)  # Even lighter background
DataVarabels.WHITE = (255, 255, 255)
DataVarabels.BLACK = (0, 0, 0)
DataVarabels.EYE_WHITES = (250, 250, 255)  # Brighter whites
DataVarabels.IRIS_COLOR = (0, 150, 255)  # More vibrant blue
DataVarabels.PUPIL_COLOR = (0, 0, 0)
DataVarabels.MOUTH_COLOR = (200, 200, 200)  # Metallic gray for mouth
DataVarabels.MOUTH_INNER = (150, 150, 150)

# Eye parameters - more robotic
DataVarabels.BASE_EYE_WIDTH = 120
DataVarabels.BASE_EYE_HEIGHT = 60  # More rectangular
DataVarabels.BASE_IRIS_RADIUS = 25  # Smaller iris for robotic look
DataVarabels.BASE_PUPIL_RADIUS = 8  # Smaller pupil
DataVarabels.BASE_MOUTH_WIDTH = 180
DataVarabels.BASE_MOUTH_HEIGHT = 40  # More narrow mouth

# Eye parameters
DataVarabels.eye_width = int(DataVarabels.BASE_EYE_WIDTH * DataVarabels.FaceSize)
DataVarabels.eye_height = int(DataVarabels.BASE_EYE_HEIGHT * DataVarabels.FaceSize)

# Adjust eye positions based on FaceSize
eye_spacing = 220 * DataVarabels.FaceSize
DataVarabels.left_eye_pos = (
screen.get_width() / 2 - eye_spacing / 2, screen.get_height() / 2 - 50 * DataVarabels.FaceSize)
DataVarabels.right_eye_pos = (
screen.get_width() / 2 + eye_spacing / 2, screen.get_height() / 2 - 50 * DataVarabels.FaceSize)

# Iris parameters
DataVarabels.iris_radius = int(DataVarabels.BASE_IRIS_RADIUS * DataVarabels.FaceSize)
DataVarabels.pupil_radius = int(DataVarabels.BASE_PUPIL_RADIUS * DataVarabels.FaceSize)
DataVarabels.iris_shrink = 0.9  # Less shrink for more robotic look

# Animation variables
DataVarabels.pupil_offset_x = 0
DataVarabels.target_offset = 0
DataVarabels.move_speed = 3  # Faster movement for robotic feel

# Blinking
DataVarabels.blink_duration = 0

# Mouth parameters
DataVarabels.mouth_width = int(DataVarabels.BASE_MOUTH_WIDTH * DataVarabels.FaceSize)
DataVarabels.mouth_height = int(DataVarabels.BASE_MOUTH_HEIGHT * DataVarabels.FaceSize)
DataVarabels.mouth_pos = (screen.get_width() / 2, screen.get_height() / 2 + 80 * DataVarabels.FaceSize)
DataVarabels.mouth_openness = 0.5

DataVarabels.running = True


def EyeGoRight():
    DataVarabels.target_offset = DataVarabels.max_swing


def EyesGoLeft():
    DataVarabels.target_offset = -DataVarabels.max_swing


def EyesFoCenter():
    DataVarabels.target_offset = 0


def EyesGosTo(topos):
    DataVarabels.target_offset = topos


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
                print("Invalid : Value too high.")
            elif MovtoValue < -45:
                print("Invalid : Value too low.")
            else:
                EyesGosTo(MovtoValue)


def quit_if_necessary():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            DataVarabels.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                DataVarabels.running = False


def blink_animation():
    if DataVarabels.blink_duration > 0:
        DataVarabels.blink_duration -= 1
    elif pygame.time.get_ticks() % 120 == 0:
        DataVarabels.blink_duration = 8  # Shorter blink


def update_animation():
    if DataVarabels.pupil_offset_x < DataVarabels.target_offset:
        DataVarabels.pupil_offset_x = min(DataVarabels.pupil_offset_x + DataVarabels.move_speed,
                                          DataVarabels.target_offset)
    elif DataVarabels.pupil_offset_x > DataVarabels.target_offset:
        DataVarabels.pupil_offset_x = max(DataVarabels.pupil_offset_x - DataVarabels.move_speed,
                                          DataVarabels.target_offset)

    DataVarabels.blink_progress = min(1, DataVarabels.blink_duration / 5)
    DataVarabels.blink_height = max(5, DataVarabels.eye_height * (1 - DataVarabels.blink_progress))


def draw_eyes():
    for pos in [DataVarabels.left_eye_pos, DataVarabels.right_eye_pos]:
        # More rectangular eye shape for robotic look
        eye_rect = pygame.Rect(
            pos[0] - DataVarabels.eye_width // 2,
            pos[1] - DataVarabels.blink_height // 2,
            DataVarabels.eye_width,
            DataVarabels.blink_height
        )

        # Eye whites with sharper corners
        pygame.draw.rect(screen, DataVarabels.EYE_WHITES, eye_rect, border_radius=10)

        # Add metallic border around eyes
        pygame.draw.rect(screen, DataVarabels.MOUTH_COLOR, eye_rect, 2, border_radius=10)

        # Iris - more precise with ring effect
        iris_x = pos[0] + DataVarabels.pupil_offset_x * 0.7
        iris_y = pos[1]
        current_iris_radius = DataVarabels.iris_radius * (
                1 - (abs(DataVarabels.pupil_offset_x) / DataVarabels.max_swing * (1 - DataVarabels.iris_shrink)))

        # Iris with ring effect
        pygame.draw.circle(screen, DataVarabels.IRIS_COLOR, (int(iris_x), int(iris_y)), int(current_iris_radius))
        pygame.draw.circle(screen, (0, 100, 200), (int(iris_x), int(iris_y)), int(current_iris_radius * 0.7), 1)
        pygame.draw.circle(screen, (0, 50, 150), (int(iris_x), int(iris_y)), int(current_iris_radius * 0.4), 1)

        # Pupil
        pygame.draw.circle(screen, DataVarabels.PUPIL_COLOR, (int(iris_x), int(iris_y)), DataVarabels.pupil_radius)

        # Highlight - more pronounced
        highlight_pos = (iris_x - current_iris_radius // 2, iris_y - current_iris_radius // 2)
        pygame.draw.circle(screen, DataVarabels.WHITE, highlight_pos, current_iris_radius // 3)


def draw_robotic_mouth():
    # Robotic mouth - horizontal bars
    bar_count = 5
    bar_height = 8
    spacing = 6
    total_height = (bar_count * bar_height) + ((bar_count - 1) * spacing)
    start_y = DataVarabels.mouth_pos[1] - total_height // 2

    for i in range(bar_count):
        y_pos = start_y + i * (bar_height + spacing)
        bar_width = DataVarabels.mouth_width * (0.7 + 0.3 * (i / (bar_count - 1)))  # Vary width slightly

        # Add some metallic shine
        pygame.draw.rect(screen, DataVarabels.MOUTH_INNER,
                         (DataVarabels.mouth_pos[0] - bar_width // 2, y_pos, bar_width, bar_height))
        pygame.draw.rect(screen, DataVarabels.WHITE,
                         (DataVarabels.mouth_pos[0] - bar_width // 2 + 5, y_pos + 1, 10, 3))


# Initialize max_swing
DataVarabels.max_swing = (DataVarabels.eye_width // 2) - DataVarabels.iris_radius

print("You can move right, left, or center, or type a number between 0 and 90 to specify an exact position.")
while DataVarabels.running:
    quit_if_necessary()
    handle_input_in_arg()

    screen.fill(DataVarabels.BG)

    blink_animation()
    update_animation()

    draw_eyes()
    draw_robotic_mouth()  # Using the new robotic mouth

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
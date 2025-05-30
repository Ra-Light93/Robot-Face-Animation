import pygame
import math
import sys

pygame.init()

from types import SimpleNamespace

DataVarabels = SimpleNamespace()

# Setup
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Controllable Eyes")
clock = pygame.time.Clock()

# Colors
DataVarabels.DARK_BG = (20, 20, 30)
DataVarabels.WHITE = (250, 250, 255)
DataVarabels.BLACK = (15, 15, 15)
DataVarabels.EYE_WHITES = (240, 240, 245)
DataVarabels.IRIS_COLOR = (80, 160, 220)
DataVarabels.PUPIL_COLOR = (10, 10, 20)
DataVarabels.MOUTH_COLOR = (220, 70, 80)
DataVarabels.MOUTH_INNER = (180, 50, 60)

# Eye parameters
DataVarabels.eye_width = 120
DataVarabels.eye_height = 80
DataVarabels.left_eye_pos = (screen.get_width() / 2 - 110, screen.get_height() / 2 - 50)
DataVarabels.right_eye_pos = (screen.get_width() / 2 + 110, screen.get_height() / 2 - 50)

# Iris parameters
DataVarabels.iris_radius = 30
DataVarabels.pupil_radius = 12
DataVarabels.iris_shrink = 0.85

# Animation variables
DataVarabels.pupil_offset_x = 0  # This will control left/right movement
DataVarabels.target_offset = 0  # Target position for smooth movement
DataVarabels.move_speed = 2  # Speed of eye movement

# Blinking
DataVarabels.blink_duration = 0

# Mouth parameters
DataVarabels.mouth_width = 200
DataVarabels.mouth_height = 80
DataVarabels.mouth_pos = (screen.get_width() / 2, screen.get_height() / 2 + 50)
DataVarabels.mouth_openness = 0.5

DataVarabels.running = True


def handle_input():
    # Get console input without blocking
    import sys
    import select

    if select.select([sys.stdin], [], [], 0)[0]:
        user_input = sys.stdin.readline().strip().lower()
        if user_input == "left":
            DataVarabels.target_offset = -DataVarabels.max_swing
        elif user_input == "right":
            DataVarabels.target_offset = DataVarabels.max_swing
        elif user_input == "center":
            DataVarabels.target_offset = 0


def quit_if_necessary():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            DataVarabels.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                DataVarabels.running = False


def blink_animation():
    # Blinking animation
    if DataVarabels.blink_duration > 0:
        DataVarabels.blink_duration -= 1
    elif pygame.time.get_ticks() % 120 == 0:  # Random blinking
        DataVarabels.blink_duration = 10


def update_animation():
    # Smoothly move eyes toward target position
    if DataVarabels.pupil_offset_x < DataVarabels.target_offset:
        DataVarabels.pupil_offset_x = min(DataVarabels.pupil_offset_x + DataVarabels.move_speed,
                                          DataVarabels.target_offset)
    elif DataVarabels.pupil_offset_x > DataVarabels.target_offset:
        DataVarabels.pupil_offset_x = max(DataVarabels.pupil_offset_x - DataVarabels.move_speed,
                                          DataVarabels.target_offset)

    # Update blink progress
    DataVarabels.blink_progress = min(1, DataVarabels.blink_duration / 5)
    DataVarabels.blink_height = max(5, DataVarabels.eye_height * (1 - DataVarabels.blink_progress))


def draw_eyes():
    for pos in [DataVarabels.left_eye_pos, DataVarabels.right_eye_pos]:
        # Eye shape
        eye_rect = pygame.Rect(
            pos[0] - DataVarabels.eye_width // 2,
            pos[1] - DataVarabels.blink_height // 2,
            DataVarabels.eye_width,
            DataVarabels.blink_height
        )

        # Eye whites
        pygame.draw.ellipse(screen, DataVarabels.EYE_WHITES, eye_rect)

        # Iris
        iris_x = pos[0] + DataVarabels.pupil_offset_x * 0.7
        iris_y = pos[1]
        current_iris_radius = DataVarabels.iris_radius * (
                    1 - (abs(DataVarabels.pupil_offset_x) / DataVarabels.max_swing * (1 - DataVarabels.iris_shrink)))

        pygame.draw.circle(screen, DataVarabels.IRIS_COLOR, (int(iris_x), int(iris_y)), int(current_iris_radius))

        # Pupil
        pygame.draw.circle(screen, DataVarabels.PUPIL_COLOR, (int(iris_x), int(iris_y)), DataVarabels.pupil_radius)

        # Highlight
        highlight_pos = (iris_x - current_iris_radius // 3, iris_y - current_iris_radius // 3)
        pygame.draw.circle(screen, DataVarabels.WHITE, highlight_pos, current_iris_radius // 4)


def draw_mouth():
    current_mouth_height = DataVarabels.mouth_height * (0.3 + 0.7 * DataVarabels.mouth_openness)
    mouth_rect = pygame.Rect(
        DataVarabels.mouth_pos[0] - DataVarabels.mouth_width // 2,
        DataVarabels.mouth_pos[1] - current_mouth_height // 2,
        DataVarabels.mouth_width,
        current_mouth_height
    )
    pygame.draw.ellipse(screen, DataVarabels.MOUTH_COLOR, mouth_rect)


# Initialize max_swing (this was missing in original code)
DataVarabels.max_swing = 45

print("Type 'left', 'right', or 'center' to control the eyes")

while DataVarabels.running:
    quit_if_necessary()
    handle_input()

    screen.fill(DataVarabels.DARK_BG)

    blink_animation()
    update_animation()

    draw_eyes()
    draw_mouth()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
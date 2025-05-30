import pygame
import math
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
DARK_BG = (50, 50, 70)
WHITE = (255, 255, 255)
EYE_WHITES = (240, 240, 240)
IRIS_COLOR = (100, 180, 220)
PUPIL_COLOR = (50, 50, 70)
MOUTH_COLOR = (200, 100, 100)

# Eye parameters
eye_width = 100
eye_height = 60
iris_radius = 25
pupil_radius = 10
iris_shrink = 0.2  # How much iris shrinks when looking to sides

# Mouth parameters
mouth_width = 120
mouth_height = 40

# Positions
left_eye_pos = (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
right_eye_pos = (SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2)
mouth_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)

# Eye movement control
pupil_offset_x = 0  # Current horizontal pupil position
max_offset = 30  # Maximum offset for left/right movement

# Blinking control
blink_duration = 0

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Eyes with Direction Control")
clock = pygame.time.Clock()


def quitIfNecessary():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def look_left():
    global pupil_offset_x
    pupil_offset_x = -max_offset


def look_right():
    global pupil_offset_x
    pupil_offset_x = max_offset


def look_center():
    global pupil_offset_x
    pupil_offset_x = 0


def draw_eyes():
    # Blinking animation
    global blink_duration

    if blink_duration > 0:
        blink_duration -= 1
    elif pygame.time.get_ticks() % 120 == 0:  # Random blink every ~2 seconds
        blink_duration = 10

    blink_progress = min(1, blink_duration / 5)
    blink_height = max(5, eye_height * (1 - blink_progress))

    # Draw eyes
    for pos in [left_eye_pos, right_eye_pos]:
        # Eye shape
        eye_rect = pygame.Rect(
            pos[0] - eye_width // 2,
            pos[1] - blink_height // 2,
            eye_width,
            blink_height
        )

        # Eye whites
        pygame.draw.ellipse(screen, EYE_WHITES, eye_rect)

        # Iris
        iris_x = pos[0] + pupil_offset_x * 0.7
        iris_y = pos[1]
        current_iris_radius = iris_radius * (1 - (abs(pupil_offset_x) / max_offset * (1 - iris_shrink)))

        pygame.draw.circle(screen, IRIS_COLOR, (iris_x, iris_y), int(current_iris_radius))

        # Pupil
        pygame.draw.circle(screen, PUPIL_COLOR, (iris_x, iris_y), pupil_radius)

        # Highlight
        highlight_pos = (iris_x - current_iris_radius // 3, iris_y - current_iris_radius // 3)
        pygame.draw.circle(screen, WHITE, highlight_pos, current_iris_radius // 4)


def draw_mouth():
    # Simple mouth - you can modify this to change with direction if you want
    mouth_rect = pygame.Rect(
        mouth_pos[0] - mouth_width // 2,
        mouth_pos[1] - mouth_height // 2,
        mouth_width,
        mouth_height
    )
    pygame.draw.ellipse(screen, MOUTH_COLOR, mouth_rect)


# Main game loop
while True:
    quitIfNecessary()

    # Handle key presses for eye movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        look_left()
    elif keys[pygame.K_RIGHT]:
        look_right()
    elif keys[pygame.K_DOWN]:
        look_center()

    screen.fill(DARK_BG)

    draw_eyes()
    draw_mouth()

    pygame.display.flip()
    clock.tick(60)
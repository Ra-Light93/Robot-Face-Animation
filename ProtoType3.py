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

#Varable for assigning the size of the face
DataVarabels.FaceSize = 1

# Colors
DataVarabels.BG = (230, 230, 230)
DataVarabels.WHITE = (250, 250, 255)
DataVarabels.BLACK = (15, 15, 15)
DataVarabels.EYE_WHITES = (240, 240, 245)
DataVarabels.IRIS_COLOR = (80, 160, 220)
DataVarabels.PUPIL_COLOR = (10, 10, 20)
DataVarabels.MOUTH_COLOR = (220, 70, 80)
DataVarabels.MOUTH_INNER = (180, 50, 60)

DataVarabels.BASE_EYE_WIDTH = 120
DataVarabels.BASE_EYE_HEIGHT = 80
DataVarabels.BASE_IRIS_RADIUS = 30
DataVarabels.BASE_PUPIL_RADIUS = 12
DataVarabels.BASE_MOUTH_WIDTH = 200
DataVarabels.BASE_MOUTH_HEIGHT = 80

# Eye parameters
DataVarabels.eye_width = int(DataVarabels.BASE_EYE_WIDTH * DataVarabels.FaceSize)
DataVarabels.eye_height = int(DataVarabels.BASE_EYE_HEIGHT * DataVarabels.FaceSize)

# Adjust eye positions based on FaceSize
eye_spacing = 220 * DataVarabels.FaceSize  # Scale the distance between eyes
DataVarabels.left_eye_pos = (screen.get_width() / 2 - eye_spacing / 2, screen.get_height() / 2 - 50 * DataVarabels.FaceSize)
DataVarabels.right_eye_pos = (screen.get_width() / 2 + eye_spacing / 2, screen.get_height() / 2 - 50 * DataVarabels.FaceSize)


# Iris parameters
DataVarabels.iris_radius = int(DataVarabels.BASE_IRIS_RADIUS * DataVarabels.FaceSize)
DataVarabels.pupil_radius = int(DataVarabels.BASE_PUPIL_RADIUS * DataVarabels.FaceSize)
DataVarabels.iris_shrink = 0.85

# Animation variables
DataVarabels.pupil_offset_x = 0  # This will control left/right movement
DataVarabels.target_offset = 0  # Target position for smooth movement
DataVarabels.move_speed = 2  # Speed of eye movement

# Blinking
DataVarabels.blink_duration = 0

# Mouth parameters
DataVarabels.mouth_width = int(DataVarabels.BASE_MOUTH_WIDTH * DataVarabels.FaceSize)
DataVarabels.mouth_height = int(DataVarabels.BASE_MOUTH_HEIGHT * DataVarabels.FaceSize)
DataVarabels.mouth_pos = (screen.get_width() / 2, screen.get_height() / 2 + 50 * DataVarabels.FaceSize)
DataVarabels.mouth_openness = 0.5

DataVarabels.running = True

def EyeGoRight() :
    DataVarabels.target_offset = DataVarabels.max_swing
def EyesGoLeft():
    DataVarabels.target_offset = -DataVarabels.max_swing
def EyesFoCenter():
    DataVarabels.target_offset = 0
def EyesGosTo(topos):

    DataVarabels.target_offset = topos

def handle_input_in_arg():
    # Get console input without blocking
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
            # da die value von -45 bis 45 we have to subtract it !
            MovtoValue = int(user_input) - 45

            if MovtoValue > 45:
                print("Invalid : Value too high.")
            elif MovtoValue < -45:
                print("Invalid : Value too low.")
            else:
                EyesGosTo(MovtoValue)


def handle_input_Button():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                DataVarabels.target_offset = -DataVarabels.max_swing
            elif event.key == pygame.K_RIGHT:
                DataVarabels.target_offset = DataVarabels.max_swing
            elif event.key == pygame.K_UP:
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


def draw_Sad_mouth():
    # Happy smile parameters
    smile_width = DataVarabels.mouth_width * 0.8
    curve_height = 80  # More pronounced curve
    y_offset = 20  # Higher position = happier

    # Draw big, cheerful smile (single arc)
    pygame.draw.arc(
        screen,
        DataVarabels.MOUTH_COLOR,
        [
            DataVarabels.mouth_pos[0] - smile_width // 2,  # Center horizontally
            DataVarabels.mouth_pos[1] - y_offset,  # Higher position
            smile_width,
            curve_height  # Curve height
        ],
        math.pi * 0.15,  # Wider angle (start at ~27 degrees)
        math.pi * 0.85,  # End at ~153 degrees
        6  # Thicker line
    )
def draw_Happy_mouth():
    smile_width = DataVarabels.mouth_width * 1.5    # original : 0.8
    curve_height = 200                               # original : 0.8
    y_offset = 120                                 # original : 80

    pygame.draw.arc(
        screen,
        DataVarabels.MOUTH_COLOR,
        [
            DataVarabels.mouth_pos[0] - smile_width // 2,
            DataVarabels.mouth_pos[1] - y_offset,
            smile_width,
            curve_height
        ],
        math.pi * 1.15,
        math.pi * 1.85,
        6
    )


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
    draw_Happy_mouth()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
import pygame
import math
import sys
from types import SimpleNamespace
import socket
import random
import select

# Setup blocking socket server (empfohlen)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('0.0.0.0', 30001))
server_socket.listen(1)
print("Waiting for connection...")

conn, addr = server_socket.accept()
print("Connection from:", addr)

# Initialize pygame
pygame.init()

# Create namespace for all variables
DataVariables = SimpleNamespace()

# Varables for gloable events :
DataVariables.STOP_SPEAKING_EVENT = None
DataVariables.SpeakAllowed = True

# Setup display
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Robotic Face")
clock = pygame.time.Clock()

# Size parameters
DataVariables.FaceSize = 0.7

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

#speaking elemnst
DataVariables.speaking = False
DataVariables.mouth_openness = 0.1  # 0=closed, 1=fully open
DataVariables.target_openness = 0.1
DataVariables.mouth_animation_speed = 0.05

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

############################## Game Functions #############################################

#integer pberprüfer
def is_integer(value):
    return value.strip().isdigit()

#Event Handling functions
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
            start_speaking_test(duration=60)  # 1 sec = 60 duraction
        elif user_input == "stop speake":
            stop_speaking_test()  # 1 sec = 60 duraction
        else :
            playsound(user_input)

def handle_input_from_java(user_input):
    input = user_input.strip().lower()

    if DataVariables.SpeakAllowed :
        if input == "gs":
            playsound("gs")
        elif input == "ks":
            playsound("ks")
        elif input == "rs":
            playsound("rs")
        elif input == "gb":
            playsound("gb")
        elif input == "kb":
            playsound("kb")
        elif input == "rb":
            playsound("rb")
        elif input == "g":
            Random_Num = random.randint(1, 2)
            randomOn = "g" + str(Random_Num)
            playsound(randomOn)

        elif input == "on":
            print("System an")
            playsound("On1");

        elif input == "off":
            print("System aus")
            Random_Num = random.randint(1, 3)
            randomOn = "Aus" + str(Random_Num)
            playsound(randomOn);

    elif input.isdigit():
        MovtoValue = int(input) - 45
        if MovtoValue > 45:
            print("Invalid: Value too high.")
        elif MovtoValue < -45:
            print("Invalid: Value too low.")
        else:
            EyesGosTo(MovtoValue)

    else:
        print("Unbekannter Befehl:", input)
    try:
        conn.sendall(("recived" + "\n").encode())
    except:
        print("Antwort konnte nicht gesendet werden.")
def playsound(input):
    sound_files = {
        "rb": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/rb.mp3",
        "kb": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/kb.mp3",
        "gb": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/gb.mp3",
        "rs": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/rs.mp3",
        "gs": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/gs.mp3",
        "ks": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/ks.mp3",
        "Aus3": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/Aus3.mp3",
        "On8": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/On8.mp3",
        "Aus2": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/Aus2.mp3",
        "On7": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/On7.mp3",
        "On6": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/On6.mp3",
        "On5": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/On5.mp3",
        "On4": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/On4.mp3",
        "On3": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/On3.mp3",
        "g2": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/g2.mp3",
        "g1": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/g1.mp3",
        "boxfull": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/boxfull.mp3",
        "leermagazine": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/leermagazine.mp3",
        "Aus1": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/Aus1.mp3",
        "On1": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/On1.mp3",
        "On2": "/Users/ralight/PycharmProjects/pythonProject/Animation/Audios/On2.mp3"
    }


    DataVariables.STOP_SPEAKING_EVENT = pygame.USEREVENT + 1
    if input in sound_files:
        file_path = sound_files[input]
        sound = pygame.mixer.Sound(file_path)
        length_in_seconds = sound.get_length()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        start_speaking_test(int(length_in_seconds))
        pygame.time.set_timer(DataVariables.STOP_SPEAKING_EVENT, int(length_in_seconds)*1000 + 400)  # 3000 ms = 3 sec

    else:
        print("Input not recognized.")





def HandleEvents():
    # Handle cancel oder quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            conn.close()
            server_socket.close()
            print("Connection closed")
            DataVariables.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                DataVariables.running = False
        elif event.type == DataVariables.STOP_SPEAKING_EVENT:
            stop_speaking_test()

#Eyes function
def EyeGoRight():
    DataVariables.target_offset = DataVariables.max_swing
def EyesGoLeft():
    DataVariables.target_offset = -DataVariables.max_swing
def EyesFoCenter():
    DataVariables.target_offset = 0
def EyesGosTo(topos):
    DataVariables.target_offset = topos



# Drew face
def draw_face_border():
    center_x, center_y = DataVariables.face_pos
    outer_radius = 350 * DataVariables.FaceSize
    inner_radius = 320 * DataVariables.FaceSize
    tech_ring_radius = 300 * DataVariables.FaceSize

    # Main face plate (circular with tech pattern)
    pygame.draw.circle(screen, (40, 45, 50), (center_x, center_y), outer_radius)
    pygame.draw.circle(screen, (30, 35, 40), (center_x, center_y), outer_radius - 3, 3)

    # Inner glowing face plate
    for i in range(3):
        radius = inner_radius - i * 15 * DataVariables.FaceSize
        color = (60 + i * 15, 65 + i * 15, 70 + i * 15)
        pygame.draw.circle(screen, color, (center_x, center_y), radius)

    # Hexagonal tech pattern
    hex_size = 25 * DataVariables.FaceSize
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
        start_x = center_x + (inner_radius - 50 * DataVariables.FaceSize) * math.cos(rad)
        start_y = center_y + (inner_radius - 50 * DataVariables.FaceSize) * math.sin(rad)
        end_x = center_x + (inner_radius - 20 * DataVariables.FaceSize) * math.cos(rad)
        end_y = center_y + (inner_radius - 20 * DataVariables.FaceSize) * math.sin(rad)

        color = (0, 200 + random.randint(0, 55), 255, 150)
        pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), 2)

    # Central power core glow
    for i in range(1, 4):
        radius = 15 * i * DataVariables.FaceSize
        alpha = 100 - i * 25
        glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (0, 150, 255, alpha),
                         (radius, radius), radius)
        screen.blit(glow_surface, (center_x - radius, center_y - radius))

    # Outer ring with connectors
    connector_points = []
    for i in range(0, 360, 45):
        rad = math.radians(i)
        x = center_x + (outer_radius + 10 * DataVariables.FaceSize) * math.cos(rad)
        y = center_y + (outer_radius + 10 * DataVariables.FaceSize) * math.sin(rad)
        connector_points.append((x, y))
        pygame.draw.circle(screen, (80, 90, 100), (x, y), 8 * DataVariables.FaceSize)
        pygame.draw.circle(screen, (0, 180, 255), (x, y), 4 * DataVariables.FaceSize)

    pygame.draw.polygon(screen, (60, 70, 80), connector_points, 3)

    # Bottom status lights
    for i, color in enumerate([(255, 0, 0), (255, 150, 0), (0, 255, 0)]):
        light_x = center_x - 60 * DataVariables.FaceSize + i * 60 * DataVariables.FaceSize
        light_y = center_y + outer_radius - 20 * DataVariables.FaceSize
        pygame.draw.circle(screen, (30, 30, 30), (light_x, light_y), 12 * DataVariables.FaceSize)
        pygame.draw.circle(screen, color, (light_x, light_y), 8 * DataVariables.FaceSize)

# Draw Eyes
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
def blink_animation():
    if DataVariables.blink_duration > 0:
        DataVariables.blink_duration -= 1
    elif pygame.time.get_ticks() % 120 == 0:  # Random blinking
        DataVariables.blink_duration = 8  # Shorter blinks


#Draw Robot Mouth
def draw_mouth():
    """Switch between original and robotic mouth based on speaking state"""
    if DataVariables.speaking:
        #draw_hyper_dynamic_mouth1()
        draw_hyper_dynamic_mouth2()
        #draw_hyper_dynamic_mouth3()
    else:
        # Keep the original happy mouth when not speaking
        draw_dynamic_mouth()
def draw_dynamic_mouth():
    """Next-generation emotional mouth rendering with physics simulation"""
    # Enhanced base parameters
    base_width = DataVariables.mouth_width * 1.2
    base_height = DataVariables.mouth_height * 1.5
    pos_x, pos_y = DataVariables.mouth_pos
    t = pygame.time.get_ticks() * 0.001

    # Physics simulation parameters
    class MouthPhysics:
        def __init__(self):
            self.vertices = []
            self.springs = []
            self.damping = 0.95
            self.tension = 0.2
            self.gravity = 0.1

        def add_vertex(self, x, y):
            self.vertices.append({"x": x, "y": y, "vx": 0, "vy": 0, "ox": x, "oy": y})

        def add_spring(self, a, b, length):
            self.springs.append({"a": a, "b": b, "length": length})

        def update(self, target_points):
            # Apply target positions
            for i, v in enumerate(self.vertices):
                dx = target_points[i][0] - v["x"]
                dy = target_points[i][1] - v["y"]
                v["vx"] += dx * self.tension
                v["vy"] += dy * self.tension

            # Spring forces
            for s in self.springs:
                a = self.vertices[s["a"]]
                b = self.vertices[s["b"]]
                dx = b["x"] - a["x"]
                dy = b["y"] - a["y"]
                dist = max(1, math.sqrt(dx * dx + dy * dy))
                force = (dist - s["length"]) * 0.1
                fx = force * dx / dist
                fy = force * dy / dist

                a["vx"] += fx
                a["vy"] += fy
                b["vx"] -= fx
                b["vy"] -= fy

            # Update positions with damping and gravity
            for v in self.vertices:
                v["vx"] *= self.damping
                v["vy"] *= self.damping
                v["vy"] += self.gravity
                v["x"] += v["vx"]
                v["y"] += v["vy"]

    # Initialize physics once
    if not hasattr(DataVariables, 'mouth_physics'):
        DataVariables.mouth_physics = MouthPhysics()
        segments = 20
        for i in range(segments + 1):
            DataVariables.mouth_physics.add_vertex(pos_x, pos_y)
            if i > 0:
                DataVariables.mouth_physics.add_spring(i - 1, i, base_width / segments)

    # Emotional parameters with enhanced dynamics
    emotion_params = {
        "happy": {
            "curve": 0.8,
            "openness": 0.5 + math.sin(t) * 0.05,
            "lip_bite": 0.0,
            "wrinkles": 1,
            "color": (0, 180, 255),
            "highlight": (120, 220, 255),
            "shadow": (0, 120, 200)
        },
        "speaking_happy": {
            "curve": 0.6,
            "openness": DataVariables.mouth_openness * 1.2,
            "lip_bite": 0.0,
            "wrinkles": 0,
            "color": (100, 200, 255),
            "highlight": (140, 240, 255),
            "shadow": (60, 160, 220)
        }
    }

    # Select current emotion state
    current_emotion = "speaking_happy" if DataVariables.speaking else "happy"
    params = emotion_params[current_emotion]

    # Generate target points with micro-expressions
    segments = len(DataVariables.mouth_physics.vertices) - 1
    target_points = []
    for i in range(segments + 1):
        x = pos_x - base_width / 2 + (base_width * i / segments)
        norm_pos = (i / segments - 0.5) * 2

        curve_factor = params["curve"] * (1 - abs(norm_pos) ** 3)
        openness_factor = params["openness"] * (0.8 + 0.2 * math.sin(t * 5 + i))
        y_offset = curve_factor * base_height * openness_factor

        tremble = math.sin(t * 30 + i) * 0.5 * (1 if DataVariables.speaking else 0.2)

        y = pos_y + y_offset + tremble
        target_points.append((x, y))

    # Update physics simulation
    DataVariables.mouth_physics.update(target_points)

    # Extract current points
    current_points = [(v["x"], v["y"]) for v in DataVariables.mouth_physics.vertices]

    # Render mouth
    if len(current_points) > 1:
        mouth_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)

        # Draw main lips
        for i in range(len(current_points) - 1):
            p1 = current_points[i]
            p2 = current_points[i + 1]

            thickness = int(10 + 6 * (1 - abs(i / segments - 0.5) * 2))
            color_progress = i / segments
            base_color = (
                min(255, max(0, params["color"][0] + int(30 * math.sin(color_progress * math.pi)))),
                min(255, max(0, params["color"][1] + int(20 * math.sin(color_progress * math.pi)))),
                min(255, max(0, params["color"][2] + int(10 * math.sin(color_progress * math.pi * 2))))
            )

            pygame.draw.line(mouth_surface, base_color, p1, p2, thickness)

            # Add highlight
            highlight_p1 = (p1[0], p1[1] - thickness * 0.2)
            highlight_p2 = (p2[0], p2[1] - thickness * 0.2)
            pygame.draw.line(mouth_surface, params["highlight"], highlight_p1, highlight_p2, int(thickness * 0.3))

            # Add shadow
            shadow_p1 = (p1[0], p1[1] + thickness * 0.3)
            shadow_p2 = (p2[0], p2[1] + thickness * 0.3)
            pygame.draw.line(mouth_surface, params["shadow"], shadow_p1, shadow_p2, int(thickness * 0.4))

        # Draw inner mouth when open
        if params["openness"] > 0.4:
            inner_points = []
            inner_segments = max(3, int(segments * 0.7))
            for j in range(inner_segments + 1):
                src_i = int(j / inner_segments * segments)
                p = current_points[src_i]
                offset = (base_height * 0.2 * params["openness"] *
                          (1 - abs(j / inner_segments - 0.5) * 2))
                inner_points.append((p[0], p[1] + offset))

            if len(inner_points) > 1:
                pygame.draw.lines(mouth_surface, (60, 80, 120, 200), False, inner_points, 6)

                if DataVariables.speaking and params["openness"] > 0.6:
                    for k in range(0, len(inner_points) - 1, 2):
                        p1 = inner_points[k]
                        p2 = inner_points[k + 1]
                        tooth_height = int(base_height * 0.3 * params["openness"])
                        pygame.draw.polygon(mouth_surface, (240, 250, 255), [
                            p1, p2,
                            (p2[0], p2[1] + tooth_height),
                            (p1[0], p1[1] + tooth_height)
                        ])

        screen.blit(mouth_surface, (0, 0))

def draw_hyper_dynamic_mouth1():
    """Simplified robotic mouth for speaking"""
    base_width = DataVariables.mouth_width
    base_height = DataVariables.mouth_height
    pos_x, pos_y = DataVariables.mouth_pos

    # Determine openness - more binary for robotic effect
    openness = 0.2
    if DataVariables.speaking:
        if DataVariables.mouth_openness > 0.5:
            openness = 0.7  # Open position
        else:
            openness = 0.2  # Closed position
    else:
        openness = DataVariables.mouth_openness

    # Simple rectangular mouth with clean lines
    mouth_rect = pygame.Rect(
        pos_x - base_width / 2,
        pos_y - base_height * openness / 2,
        base_width,
        base_height * openness
    )

    # Draw with metallic colors
    if DataVariables.speaking:
        # Metallic blue for speaking
        mouth_color = (80, 180, 255)
        inner_color = (40, 100, 180)
    else:
        # Original happy color
        mouth_color = (0, 180, 255)
        inner_color = (0, 120, 200)

    # Main mouth rectangle
    pygame.draw.rect(screen, mouth_color, mouth_rect, 0, 5)

    # Add some simple robotic details when speaking
    if DataVariables.speaking:
        # Horizontal bars to suggest mechanical parts
        for i in range(1, 4):
            bar_y = mouth_rect.y + i * (mouth_rect.height // 4)
            pygame.draw.line(
                screen,
                (200, 230, 255),
                (mouth_rect.x, bar_y),
                (mouth_rect.x + mouth_rect.width, bar_y),
                2
            )

        # Add some "teeth" or separators
        for i in range(1, 5):
            tooth_x = mouth_rect.x + i * (mouth_rect.width // 5)
            pygame.draw.line(
                screen,
                (255, 255, 255),
                (tooth_x, mouth_rect.y),
                (tooth_x, mouth_rect.y + mouth_rect.height),
                1
            )
    else:
        # Original happy mouth details
        pygame.draw.rect(screen, inner_color, mouth_rect, 2, 5)
        pygame.draw.line(
            screen,
            (120, 220, 255),
            (mouth_rect.x, mouth_rect.y + mouth_rect.height // 2),
            (mouth_rect.x + mouth_rect.width, mouth_rect.y + mouth_rect.height // 2),
            3
        )
def draw_hyper_dynamic_mouth2():
    """Ultra-responsive mouth animation with dramatic speed increase during speech"""
    # Base parameters
    base_width = DataVariables.mouth_width * 1.2
    base_height = DataVariables.mouth_height * 1.5
    pos_x, pos_y = DataVariables.mouth_pos
    t = pygame.time.get_ticks() * 0.001

    # Speech detection - add slight delay for more natural transitions
    speaking = DataVariables.speaking
    SPEECH_SPEED_BOOST = 3.5  # How much faster during speech (was ~1.5 before)

    class MouthPhysics:
        def __init__(self):
            self.vertices = []
            self.springs = []
            # Base physics values
            self.base_damping = 0.92
            self.base_tension = 0.25
            self.gravity = 0.1

        def add_vertex(self, x, y):
            self.vertices.append({"x": x, "y": y, "vx": 0, "vy": 0, "ox": x, "oy": y})

        def add_spring(self, a, b, length):
            self.springs.append({"a": a, "b": b, "length": length})

        def update(self, target_points):
            # Dramatic physics changes during speech
            current_damping = self.base_damping * (0.6 if speaking else 1.0)  # More extreme damping reduction
            current_tension = self.base_tension * (SPEECH_SPEED_BOOST if speaking else 1.0)

            # Apply target positions with velocity boost
            for i, v in enumerate(self.vertices):
                dx = target_points[i][0] - v["x"]
                dy = target_points[i][1] - v["y"]
                boost = 1.5 if speaking else 1.0  # Additional direct velocity boost
                v["vx"] += dx * current_tension * boost
                v["vy"] += dy * current_tension * boost

            # Spring forces - make springs more active during speech
            for s in self.springs:
                a = self.vertices[s["a"]]
                b = self.vertices[s["b"]]
                dx = b["x"] - a["x"]
                dy = b["y"] - a["y"]
                dist = max(1, math.sqrt(dx * dx + dy * dy))
                force_multiplier = 0.15 if speaking else 0.1  # Stronger spring forces
                force = (dist - s["length"]) * force_multiplier
                fx = force * dx / dist
                fy = force * dy / dist

                a["vx"] += fx
                a["vy"] += fy
                b["vx"] -= fx
                b["vy"] -= fy

            # Update positions - apply speed factors
            for v in self.vertices:
                v["vx"] *= current_damping
                v["vy"] *= current_damping
                v["vy"] += self.gravity
                # Direct speed multiplier during speech
                speed_boost = 1.8 if speaking else 1.0
                v["x"] += v["vx"] * speed_boost
                v["y"] += v["vy"] * speed_boost

    # Initialize physics
    if not hasattr(DataVariables, 'mouth_physics'):
        DataVariables.mouth_physics = MouthPhysics()
        segments = 20
        for i in range(segments + 1):
            DataVariables.mouth_physics.add_vertex(pos_x, pos_y)
            if i > 0:
                DataVariables.mouth_physics.add_spring(i - 1, i, base_width / segments)

    # Emotional parameters with extreme speech dynamics
    emotion_params = {
        "happy": {
            "curve": 0.8,
            "openness": 0.5 + math.sin(t) * 0.05,
            "color": (0, 180, 255),
            "highlight": (120, 220, 255),
            "shadow": (0, 120, 200)
        },
        "speaking_happy": {
            "curve": 0.6,
            "openness": DataVariables.mouth_openness * (1.3 + 0.3 * math.sin(t * 15)),  # Much faster oscillation
            "color": (100, 200, 255),
            "highlight": (140, 240, 255),
            "shadow": (60, 160, 220)
        }
    }

    current_emotion = "speaking_happy" if speaking else "happy"
    params = emotion_params[current_emotion]

    # Generate target points with ultra-dynamic speech effects
    segments = len(DataVariables.mouth_physics.vertices) - 1
    target_points = []
    for i in range(segments + 1):
        x = pos_x - base_width / 2 + (base_width * i / segments)
        norm_pos = (i / segments - 0.5) * 2

        # Extreme curve changes during speech
        curve_factor = params["curve"] * (1 - abs(norm_pos) ** 3)
        freq = 12 if speaking else 3  # Much higher frequency when speaking
        openness_factor = params["openness"] * (0.8 + 0.2 * math.sin(t * freq + i * 0.5))
        y_offset = curve_factor * base_height * openness_factor

        # Aggressive tremble effect during speech
        tremble_freq = 50 if speaking else 20
        tremble = math.sin(t * tremble_freq + i * 2) * (1.2 if speaking else 0.2)

        y = pos_y + y_offset + tremble
        target_points.append((x, y))

    # Update physics simulation
    DataVariables.mouth_physics.update(target_points)

    # Render mouth (same as before but with speedier movements)
    current_points = [(v["x"], v["y"]) for v in DataVariables.mouth_physics.vertices]
    if len(current_points) > 1:
        mouth_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)

        # Draw main lips
        for i in range(len(current_points) - 1):
            p1 = current_points[i]
            p2 = current_points[i + 1]

            thickness = int(10 + 6 * (1 - abs(i / segments - 0.5) * 2))
            color_progress = i / segments
            base_color = (
                min(255, max(0, params["color"][0] + int(30 * math.sin(color_progress * math.pi)))),
                min(255, max(0, params["color"][1] + int(20 * math.sin(color_progress * math.pi)))),
                min(255, max(0, params["color"][2] + int(10 * math.sin(color_progress * math.pi * 2))))
            )

            pygame.draw.line(mouth_surface, base_color, p1, p2, thickness)

            # Add highlight
            highlight_p1 = (p1[0], p1[1] - thickness * 0.2)
            highlight_p2 = (p2[0], p2[1] - thickness * 0.2)
            pygame.draw.line(mouth_surface, params["highlight"], highlight_p1, highlight_p2, int(thickness * 0.3))

            # Add shadow
            shadow_p1 = (p1[0], p1[1] + thickness * 0.3)
            shadow_p2 = (p2[0], p2[1] + thickness * 0.3)
            pygame.draw.line(mouth_surface, params["shadow"], shadow_p1, shadow_p2, int(thickness * 0.4))

        # Draw inner mouth when open
        if params["openness"] > 0.4:
            inner_points = []
            inner_segments = max(3, int(segments * 0.7))
            for j in range(inner_segments + 1):
                src_i = int(j / inner_segments * segments)
                p = current_points[src_i]
                offset = (base_height * 0.2 * params["openness"] *
                          (1 - abs(j / inner_segments - 0.5) * 2))
                inner_points.append((p[0], p[1] + offset))

            if len(inner_points) > 1:
                pygame.draw.lines(mouth_surface, (60, 80, 120, 200), False, inner_points, 6)



        screen.blit(mouth_surface, (0, 0))
def draw_hyper_dynamic_mouth3():
    """Ultra-responsive mouth animation with dramatic speed increase during speech"""
    # Base parameters
    base_width = DataVariables.mouth_width * 1.2
    base_height = DataVariables.mouth_height * 1.5
    pos_x, pos_y = DataVariables.mouth_pos
    t = pygame.time.get_ticks() * 0.001

    # Speech detection - add slight delay for more natural transitions
    speaking = DataVariables.speaking
    SPEECH_SPEED_BOOST = 3.5  # How much faster during speech (was ~1.5 before)

    class MouthPhysics:
        def __init__(self):
            self.vertices = []
            self.springs = []
            # Base physics values
            self.base_damping = 0.92
            self.base_tension = 0.25
            self.gravity = 0.1

        def add_vertex(self, x, y):
            self.vertices.append({"x": x, "y": y, "vx": 0, "vy": 0, "ox": x, "oy": y})

        def add_spring(self, a, b, length):
            self.springs.append({"a": a, "b": b, "length": length})

        def update(self, target_points):
            # Dramatic physics changes during speech
            current_damping = self.base_damping * (0.6 if speaking else 1.0)  # More extreme damping reduction
            current_tension = self.base_tension * (SPEECH_SPEED_BOOST if speaking else 1.0)

            # Apply target positions with velocity boost
            for i, v in enumerate(self.vertices):
                dx = target_points[i][0] - v["x"]
                dy = target_points[i][1] - v["y"]
                boost = 1.5 if speaking else 1.0  # Additional direct velocity boost
                v["vx"] += dx * current_tension * boost
                v["vy"] += dy * current_tension * boost

            # Spring forces - make springs more active during speech
            for s in self.springs:
                a = self.vertices[s["a"]]
                b = self.vertices[s["b"]]
                dx = b["x"] - a["x"]
                dy = b["y"] - a["y"]
                dist = max(1, math.sqrt(dx * dx + dy * dy))
                force_multiplier = 0.15 if speaking else 0.1  # Stronger spring forces
                force = (dist - s["length"]) * force_multiplier
                fx = force * dx / dist
                fy = force * dy / dist

                a["vx"] += fx
                a["vy"] += fy
                b["vx"] -= fx
                b["vy"] -= fy

            # Update positions - apply speed factors
            for v in self.vertices:
                v["vx"] *= current_damping
                v["vy"] *= current_damping
                v["vy"] += self.gravity
                # Direct speed multiplier during speech
                speed_boost = 1.8 if speaking else 1.0
                v["x"] += v["vx"] * speed_boost
                v["y"] += v["vy"] * speed_boost

    # Initialize physics
    if not hasattr(DataVariables, 'mouth_physics'):
        DataVariables.mouth_physics = MouthPhysics()
        segments = 20
        for i in range(segments + 1):
            DataVariables.mouth_physics.add_vertex(pos_x, pos_y)
            if i > 0:
                DataVariables.mouth_physics.add_spring(i - 1, i, base_width / segments)

    # Emotional parameters with extreme speech dynamics
    emotion_params = {
        "happy": {
            "curve": 0.8,
            "openness": 0.5 + math.sin(t) * 0.05,
            "color": (0, 180, 255),
            "highlight": (120, 220, 255),
            "shadow": (0, 120, 200)
        },
        "speaking_happy": {
            "curve": 0.6,
            "openness": DataVariables.mouth_openness * (1.3 + 0.3 * math.sin(t * 15)),  # Much faster oscillation
            "color": (100, 200, 255),
            "highlight": (140, 240, 255),
            "shadow": (60, 160, 220)
        }
    }

    current_emotion = "speaking_happy" if speaking else "happy"
    params = emotion_params[current_emotion]

    # Generate target points with ultra-dynamic speech effects
    segments = len(DataVariables.mouth_physics.vertices) - 1
    target_points = []
    for i in range(segments + 1):
        x = pos_x - base_width / 2 + (base_width * i / segments)
        norm_pos = (i / segments - 0.5) * 2

        # Extreme curve changes during speech
        curve_factor = params["curve"] * (1 - abs(norm_pos) ** 3)
        freq = 12 if speaking else 3  # Much higher frequency when speaking
        openness_factor = params["openness"] * (0.8 + 0.2 * math.sin(t * freq + i * 0.5))
        y_offset = curve_factor * base_height * openness_factor

        # Aggressive tremble effect during speech
        tremble_freq = 50 if speaking else 20
        tremble = math.sin(t * tremble_freq + i * 2) * (1.2 if speaking else 0.2)

        y = pos_y + y_offset + tremble
        target_points.append((x, y))

    # Update physics simulation
    DataVariables.mouth_physics.update(target_points)

    # Render mouth (same as before but with speedier movements)
    current_points = [(v["x"], v["y"]) for v in DataVariables.mouth_physics.vertices]
    if len(current_points) > 1:
        mouth_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)

        # Draw main lips
        for i in range(len(current_points) - 1):
            p1 = current_points[i]
            p2 = current_points[i + 1]

            thickness = int(10 + 6 * (1 - abs(i / segments - 0.5) * 2))
            color_progress = i / segments
            base_color = (
                min(255, max(0, params["color"][0] + int(30 * math.sin(color_progress * math.pi)))),
                min(255, max(0, params["color"][1] + int(20 * math.sin(color_progress * math.pi)))),
                min(255, max(0, params["color"][2] + int(10 * math.sin(color_progress * math.pi * 2))))
            )

            pygame.draw.line(mouth_surface, base_color, p1, p2, thickness)

            # Add highlight
            highlight_p1 = (p1[0], p1[1] - thickness * 0.2)
            highlight_p2 = (p2[0], p2[1] - thickness * 0.2)
            pygame.draw.line(mouth_surface, params["highlight"], highlight_p1, highlight_p2, int(thickness * 0.3))

            # Add shadow
            shadow_p1 = (p1[0], p1[1] + thickness * 0.3)
            shadow_p2 = (p2[0], p2[1] + thickness * 0.3)
            pygame.draw.line(mouth_surface, params["shadow"], shadow_p1, shadow_p2, int(thickness * 0.4))

        # Draw inner mouth when open
        if params["openness"] > 0.4:
            inner_points = []
            inner_segments = max(3, int(segments * 0.7))
            for j in range(inner_segments + 1):
                src_i = int(j / inner_segments * segments)
                p = current_points[src_i]
                offset = (base_height * 0.2 * params["openness"] *
                          (1 - abs(j / inner_segments - 0.5) * 2))
                inner_points.append((p[0], p[1] + offset))

            if len(inner_points) > 1:
                pygame.draw.lines(mouth_surface, (60, 80, 120, 200), False, inner_points, 6)

                if DataVariables.speaking and params["openness"] > 0.6:
                    for k in range(0, len(inner_points) - 1, 2):
                        p1 = inner_points[k]
                        p2 = inner_points[k + 1]
                        tooth_height = int(base_height * 0.3 * params["openness"])
                        pygame.draw.polygon(mouth_surface, (240, 250, 255), [
                            p1, p2,
                            (p2[0], p2[1] + tooth_height),
                            (p1[0], p1[1] + tooth_height)
                        ])


        screen.blit(mouth_surface, (0, 0))


def draw_Sad_mouth():
    """Dynamic sad mouth with subtle animation and detailed rendering"""
    base_width = DataVariables.mouth_width * 1.2
    base_height = DataVariables.mouth_height * 1.5
    pos_x, pos_y = DataVariables.mouth_pos
    t = pygame.time.get_ticks() * 0.001  # Time in seconds for animation

    # Mouth physics simulation (for subtle trembling)
    tremble_intensity = 0.5 if DataVariables.speaking else 0.2
    tremble_x = math.sin(t * 8) * 2 * tremble_intensity
    tremble_y = math.sin(t * 6.3) * 1.5 * tremble_intensity

    # Create mouth points with dynamic curvature
    points = []
    segments = 20
    for i in range(segments + 1):
        # Normalized position (-1 to 1 across mouth width)
        norm_pos = (i / segments - 0.5) * 2

        # Base curvature (sad shape)
        curve_factor = -0.6 * (1 - abs(norm_pos) ** 3)

        # Add subtle animation
        anim_factor = 0.9 + 0.1 * math.sin(t * 3 + i * 0.3)

        x = pos_x - base_width / 2 + (base_width * i / segments) + tremble_x
        y = (pos_y + base_height * curve_factor * anim_factor +
             10 * math.sin(norm_pos * 2) + tremble_y)

        points.append((x, y))

    # Draw mouth with gradient and highlights
    if len(points) > 1:
        # Main mouth line (with thickness variation)
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]

            # Vary thickness for more organic look
            thickness = int(8 + 4 * (1 - abs(i / segments - 0.5) * 2))

            # Color gradient from center to edges
            color_progress = i / segments
            base_color = (
                int(50 + 100 * (1 - color_progress)),  # R: 50–150
                int(150 + 80 * (1 - color_progress)),  # G: 150–230
                255  # B: always bright blue
            )

            pygame.draw.line(screen, base_color, p1, p2, thickness)

            # Add highlight
            highlight_color = (180, 220, 255)
            highlight_p1 = (p1[0], p1[1] - thickness * 0.3)
            highlight_p2 = (p2[0], p2[1] - thickness * 0.3)
            pygame.draw.line(screen, highlight_color, highlight_p1, highlight_p2, max(1, thickness // 3))

            # Draw drooping corners (more pronounced when sad)
            corner_length = 20 * DataVariables.FaceSize
            left_corner = (points[0][0] - corner_length * 0.7,
                           points[0][1] + corner_length * 0.5)
            right_corner = (points[-1][0] + corner_length * 0.7,
                            points[-1][1] + corner_length * 0.5)

            # Draw drooping corners (cool blue)
            pygame.draw.line(screen, (100, 150, 255), points[0], left_corner, 4)
            pygame.draw.line(screen, (100, 150, 255), points[-1], right_corner, 4)

            # Optional: Add subtle shadow beneath mouth
            shadow_surface = pygame.Surface((1000, 1000), pygame.SRCALPHA)
            shadow_points = [(p[0], p[1] + 5) for p in points]
            pygame.draw.lines(shadow_surface, (0, 0, 0, 30), False, shadow_points, 10)
            screen.blit(shadow_surface, (0, 0))


#Animation Updating
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
def update_mouth_animation():
    """Update the mouth openness based on speaking state and time"""
    # Smoothly transition to target openness
    if DataVariables.mouth_openness < DataVariables.target_openness:
        DataVariables.mouth_openness = min(DataVariables.mouth_openness + DataVariables.mouth_animation_speed,
                                           DataVariables.target_openness)
    elif DataVariables.mouth_openness > DataVariables.target_openness:
        DataVariables.mouth_openness = max(DataVariables.mouth_openness - DataVariables.mouth_animation_speed,
                                           DataVariables.target_openness)

    # If speaking, create a robotic talking motion
    if DataVariables.speaking:
        # Simple binary open/close pattern for robotic speech
        t = pygame.time.get_ticks() * 0.001
        # Square wave pattern for more mechanical movement
        if int(t * 10) % 2 == 0:
            DataVariables.target_openness = 0.7  # Fully open
        else:
            DataVariables.target_openness = 0.2  # Mostly closed


# Speaking Animation
def start_speaking_test(duration=60):
    """Start speaking animation for the given duration (in frames)"""
    DataVariables.speaking = True
    # Start with slightly open mouth
    DataVariables.target_openness = 0.5
def stop_speaking_test():
    """Stop speaking animation and return mouth to neutral state"""
    DataVariables.speaking = False
    # Return to slightly open mouth for happy expression
    DataVariables.target_openness = 0.1

##### buttons ####
DataVariables.left_button_name = "Start"
def draw_top_left_button():
    button_rect = pygame.Rect(20, 20, 150, 50)  # Slightly larger size

    # Add hover and click effects
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = button_rect.collidepoint(mouse_pos)
    is_clicked = pygame.mouse.get_pressed()[0] and is_hovered

    # Base colors
    base_color = (200, 50, 60)  # Red for terminate
    hover_color = (230, 70, 80)
    click_color = (170, 30, 40)

    # Determine current color based on state
    current_color = base_color
    if is_clicked:
        current_color = click_color
    elif is_hovered:
        current_color = hover_color

    # Draw button with shadow and rounded corners
    pygame.draw.rect(screen, (30, 30, 30, 150), button_rect.move(3, 3), border_radius=8)  # Shadow
    pygame.draw.rect(screen, current_color, button_rect, border_radius=8)  # Main button

    # Add border glow effect when hovered
    border_color = (255, 255, 255, 100 + (100 if is_hovered else 0))
    pygame.draw.rect(screen, border_color, button_rect, 2, border_radius=8)

    # Draw text with shadow
    font = pygame.font.SysFont("Arial", 24, bold=True)
    text = font.render(DataVariables.left_button_name, True, (240, 240, 240))
    text_rect = text.get_rect(center=button_rect.center)

    # Text shadow
    shadow_text = font.render(DataVariables.left_button_name, True, (0, 0, 0, 150))
    screen.blit(shadow_text, text_rect.move(1, 1))
    screen.blit(text, text_rect)

    # Handle click with ripple effect
    if is_clicked and not hasattr(DataVariables, 'button_click_time'):
        DataVariables.button_click_time = pygame.time.get_ticks()
        DataVariables.button_click_pos = mouse_pos
        print("Terminate clicked!")
        StopStartRobot()
        if DataVariables.left_button_name == "Stop" :
            DataVariables.left_button_name = "Start"
        else :
            DataVariables.left_button_name = "Stop"

    # Draw ripple effect if recently clicked
    if hasattr(DataVariables, 'button_click_time'):
        elapsed = pygame.time.get_ticks() - DataVariables.button_click_time
        if elapsed < 500:  # Show ripple for 500ms
            ripple_radius = elapsed // 5
            ripple_alpha = max(0, 150 - (elapsed // 3))

            ripple_surf = pygame.Surface((ripple_radius * 2, ripple_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(ripple_surf, (*click_color, ripple_alpha),
                               (ripple_radius, ripple_radius), ripple_radius)
            screen.blit(ripple_surf, (DataVariables.button_click_pos[0] - ripple_radius,
                                      DataVariables.button_click_pos[1] - ripple_radius))
        else:
            delattr(DataVariables, 'button_click_time')


DataVariables.right_button_name = "Stop Sound"
def draw_top_right_button():
    button_rect = pygame.Rect(screen.get_width() - 170, 20, 150, 50)  # Positioned on right

    # Add hover and click effects
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = button_rect.collidepoint(mouse_pos)
    is_clicked = pygame.mouse.get_pressed()[0] and is_hovered

    # Base colors (blue for sound)
    base_color = (60, 100, 200)
    hover_color = (90, 130, 230)
    click_color = (30, 70, 170)

    # Determine current color based on state
    current_color = base_color
    if is_clicked:
        current_color = click_color
    elif is_hovered:
        current_color = hover_color

    # Draw button with shadow and rounded corners
    pygame.draw.rect(screen, (30, 30, 30, 150), button_rect.move(3, 3), border_radius=8)  # Shadow
    pygame.draw.rect(screen, current_color, button_rect, border_radius=8)  # Main button

    # Add border glow effect when hovered
    border_color = (255, 255, 255, 100 + (100 if is_hovered else 0))
    pygame.draw.rect(screen, border_color, button_rect, 2, border_radius=8)

    # Draw text with shadow
    font = pygame.font.SysFont("Arial", 24, bold=True)
    text = font.render(DataVariables.right_button_name, True, (240, 240, 240))
    text_rect = text.get_rect(center=button_rect.center)

    # Text shadow
    shadow_text = font.render(DataVariables.right_button_name, True, (0, 0, 0, 150))
    screen.blit(shadow_text, text_rect.move(1, 1))
    screen.blit(text, text_rect)

    # Handle click with ripple effect
    if is_clicked and not hasattr(DataVariables, 'sound_button_click_time'):
        DataVariables.sound_button_click_time = pygame.time.get_ticks()
        DataVariables.sound_button_click_pos = mouse_pos
        print("Sound button clicked!")
        DataVariables.SpeakAllowed = not DataVariables.SpeakAllowed
        if DataVariables.SpeakAllowed :
            DataVariables.right_button_name = "Stop Sound"
            draw_top_right_button()
        else :
            DataVariables.right_button_name = "Sound On"
            draw_top_right_button()

        # Add your sound stop logic here

    # Draw ripple effect if recently clicked
    if hasattr(DataVariables, 'sound_button_click_time'):
        elapsed = pygame.time.get_ticks() - DataVariables.sound_button_click_time
        if elapsed < 500:  # Show ripple for 500ms
            ripple_radius = elapsed // 5
            ripple_alpha = max(0, 150 - (elapsed // 3))

            ripple_surf = pygame.Surface((ripple_radius * 2, ripple_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(ripple_surf, (*click_color, ripple_alpha),
                               (ripple_radius, ripple_radius), ripple_radius)
            screen.blit(ripple_surf, (DataVariables.sound_button_click_pos[0] - ripple_radius,
                                      DataVariables.sound_button_click_pos[1] - ripple_radius))
        else:
            delattr(DataVariables, 'sound_button_click_time')




# Main loop
print("Controls: Type 'left', 'right', or 'center'. Or enter a number (0-90) for precise position.\nYou can Type \"speake\" and \"stop speake\" to move the Mouth")



def handle_terminal_input_and_talk_to_java():
    import select
    import sys

    if select.select([sys.stdin], [], [], 0)[0]:
        user_input = sys.stdin.readline().strip()
        if user_input:
            conn.sendall((user_input + "\n").encode())  # send to Java
            try:
                ready, _, _ = select.select([conn], [], [], 0.2)
                if ready:
                    response = conn.recv(1024).decode().strip()
                    if response:
                        print("Antwort von Java:", response)
            except:
                pass

def StopStartRobot():
    try:
        command = DataVariables.left_button_name
        conn.sendall(f"{command}\n".encode())
        print("Stop-Befehl an Java gesendet.")
    except Exception as e:
        print("Fehler beim Senden des Stop-Befehls:", e)

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
    draw_top_left_button()  # Red terminate button
    draw_top_right_button()  # Blue sound button


    try:
        ready, _, _ = select.select([conn], [], [], 0)
        if ready:
            data = conn.recv(1024)
            if data:
                strData = data.decode().strip()
                handle_input_from_java(strData)
    except (BlockingIOError, ConnectionResetError):
        pass
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()

    # Update display
    pygame.display.flip()
    clock.tick(60)

    if len(sys.argv) > 1:
        print("Übergebene Argumente:", sys.argv[1:])


# Clean up
pygame.quit()
sys.exit()
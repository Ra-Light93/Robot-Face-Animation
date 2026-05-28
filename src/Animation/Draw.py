from config import get_config 
import pygame
import math
import random

# Drew face
def draw_face_border():
    DataVariables = get_config()
    screen = DataVariables.screen
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
    DataVariables = get_config()
    screen = DataVariables.screen
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

# Blink animation
def blink_animation():
    DataVariables = get_config()
    if DataVariables.blink_duration > 0:
        DataVariables.blink_duration -= 1
    elif pygame.time.get_ticks() % 120 == 0:  # Random blinking
        DataVariables.blink_duration = 8  # Shorter blinks

#Draw Robot Mouth
def draw_mouth():
    DataVariables = get_config()
    """Switch between original and robotic mouth based on speaking state"""
    if DataVariables.speaking:
        #draw_hyper_dynamic_mouth1()
        draw_mouth_speaking()
        #draw_hyper_dynamic_mouth3()
    else:
        # Keep the original happy mouth when not speaking
        draw_mouth_default()

# These 5 functions are used to test variants of the dynamic mouth and can be called from the draw_mouth() function.
def draw_mouth_default():
    DataVariables = get_config()
    screen = DataVariables.screen
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

def draw_mouth_speaking():
    DataVariables = get_config()
    screen = DataVariables.screen
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

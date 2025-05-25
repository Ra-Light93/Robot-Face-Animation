import pygame
import math

pygame.init()

# Setup
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 102, 204)
RED = (255, 0, 0)

# Eye parameters
eye_radius = 30
iris_radius = 15
pupil_radius = 7
left_eye_center = (120, 120)
right_eye_center = (280, 120)

# Mouth parameters
mouth_width = 120
mouth_height = 60
mouth_pos = (140, 180)

running = True

print("Locked Mouse")
while running:
    screen.fill(WHITE)

    # Get mouse position for eye tracking
    mouse_pos = pygame.mouse.get_pos()

    # Calculate pupil offset based on mouse position
    pupil_offset = [0, 0]
    for center in [left_eye_center, right_eye_center]:
        # Vector from eye center to mouse position
        dx = mouse_pos[0] - center[0]
        dy = mouse_pos[1] - center[1]
        distance = max(1, math.sqrt(dx * dx + dy * dy))

        # Normalize and scale to max offset
        scale = min(eye_radius - iris_radius - 2, distance)
        pupil_offset = [
            int(dx * scale / distance),
            int(dy * scale / distance)
        ]

        # Draw eyes with dynamic pupils
        pygame.draw.circle(screen, WHITE, center, eye_radius, 2)  # white part with outline
        pygame.draw.circle(screen, BLUE,
                           (center[0] + pupil_offset[0] // 3, center[1] + pupil_offset[1] // 3),
                           iris_radius)  # iris
        pygame.draw.circle(screen, BLACK,
                           (center[0] + pupil_offset[0], center[1] + pupil_offset[1]),
                           pupil_radius)  # pupil

    # Smiling mouth (more detailed)
    mouth_rect = pygame.Rect(mouth_pos[0], mouth_pos[1], mouth_width, mouth_height)
    pygame.draw.ellipse(screen, BLACK, mouth_rect, 2)  # outline

    # Draw lips (upper lip is invisible, lower lip is red)
    pygame.draw.arc(screen, RED, mouth_rect, math.pi, 2 * math.pi, 3)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
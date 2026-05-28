from config import get_config
import pygame


def update_animation():
    DataVariables = get_config()
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
    DataVariables = get_config()
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

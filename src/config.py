from types import SimpleNamespace
from typing import Optional
import pygame
import os
import json


_instance: Optional[SimpleNamespace] = None

def get_config() -> SimpleNamespace:
    """Returns the existing config instance. Must call init_config() first."""
    if _instance is None:
        raise RuntimeError("Config not initialized. Call init_config(screen) first.")
    return _instance

def init_config(screen: pygame.Surface) -> SimpleNamespace:
    """Initialize config with screen dimensions. Call once from main.py."""
    global _instance
    if _instance is not None:
        return _instance  
    
    # Create namespace for all variables
    DataVariables = SimpleNamespace()

    # Varables for gloable events :
    DataVariables.STOP_SPEAKING_EVENT = None
    DataVariables.SpeakAllowed = True
    
    # Size parameters
    DataVariables.FaceSize = 0.9

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
    DataVariables.FACE_SHAPE = "hexagon"
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
    
    # Buttons state
    DataVariables.left_button_state = "Start"  # "play" oder "pause"
    DataVariables.right_button_state = "sound_on"  # "sound_on" oder "sound_off"
    
    # connection variable for communication
    DataVariables.conn = None
    DataVariables.addr = None
    
    # Socket communication
    DataVariables.no_socket = False  # Set to True to disable socket communication (for testing without Java)
    
    DataVariables.screen = None
    
    DataVariables.audio_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Audios")
    
    DataVariables.pygame_title = "Robotic Face" 
    
    DataVariables.audio_register = load_audio_register(DataVariables.audio_dir)

    _instance = DataVariables
    return _instance
  


def load_audio_register(audio_dir: str) -> SimpleNamespace:
    register_path = os.path.join(audio_dir, "audio_register.json")
    
    # Check if register file exists
    if not os.path.exists(register_path):
        raise FileNotFoundError(f"Audio register not found at: {register_path}, please create it with the correct command-to-filename mappings.")
    
    # Load JSON
    try:
        with open(register_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in audio_register.json: {e}")
    
    # Validate each entry
    register = SimpleNamespace()
    for command, filename in data.items():
        # Ensure flat structure - no nested JSON
        if not isinstance(command, str):
            try:
                command = str(command)
            except Exception as e:
                raise TypeError(f"Warning: Non-string command key '{command}' cannot be converted to string: {e}")
            
        if not isinstance(filename, str):
            try:
                filename = str(filename)
            except Exception as e:
                raise TypeError(f"Value for '{command}' must be a string filename, cannot be converted: {e}")
            
        file_path = os.path.join(audio_dir, filename)
        
        if not os.path.exists(file_path):
            print(f"######˜\nRegistering command '{command}' with file '{file_path}'")
            raise FileNotFoundError(f"Audio file missing for command '{command}': {file_path}")

        setattr(register, command, filename)
    
    return register
    
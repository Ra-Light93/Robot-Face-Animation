from types import SimpleNamespace
from typing import Optional
import pygame
import os
import json

# ── Singleton instance ───────────────────────────────────
_instance: Optional[SimpleNamespace] = None


def get_config() -> SimpleNamespace:
    """Returns the existing config instance. Must call init_config() first."""
    if _instance is None:
        raise RuntimeError("Config not initialized. Call init_config(screen) first.")
    return _instance


def init_config(screen: pygame.Surface) -> SimpleNamespace:
    """
    Initialize the global config with screen dimensions.
    Must be called once from main.py before anything else.
    Returns the singleton DataVariables namespace.
    """
    global _instance
    if _instance is not None:
        return _instance

    dv = SimpleNamespace()

    # ── Events ───────────────────────────────────────────
    dv.STOP_SPEAKING_EVENT = None
    dv.SpeakAllowed = True

    # ── Face scale ───────────────────────────────────────
    dv.FaceSize = min(screen.get_width(), screen.get_height()) / 1000 * 0.9

    # ── Color palette ────────────────────────────────────
    dv.BG               = (240, 240, 245)   # Light gray background
    dv.WHITE            = (255, 255, 255)
    dv.BLACK            = (0,   0,   0  )
    dv.EYE_WHITES       = (250, 250, 255)
    dv.IRIS_COLOR       = (0,   150, 255)   # Vibrant blue
    dv.PUPIL_COLOR      = (0,   0,   0  )
    dv.MOUTH_COLOR      = (0,   140, 255)   # Electric blue
    dv.EYEBORDEAR_COLOR = (0,   0,   0  )   # Eye border
    dv.MOUTH_INNER      = (80,  80,  100)
    dv.MOUTH_ACCENT     = (150, 160, 170)

    # ── Eye dimensions (base, before scaling) ────────────
    dv.BASE_EYE_WIDTH    = 120
    dv.BASE_EYE_HEIGHT   = 60
    dv.BASE_IRIS_RADIUS  = 25
    dv.BASE_PUPIL_RADIUS = 8
    dv.BASE_MOUTH_WIDTH  = 180
    dv.BASE_MOUTH_HEIGHT = 40

    # ── Face shape parameters ────────────────────────────
    dv.FACE_SHAPE            = "hexagon"
    dv.FACE_WIDTH            = 550
    dv.FACE_HEIGHT           = 700
    dv.FACE_CORNER_RADIUS    = 80
    dv.FACE_BORDER_THICKNESS = 12
    dv.FACE_COLOR            = (220, 225, 235)
    dv.FACE_BORDER_COLOR     = (80,  90,  110)
    dv.FACE_ACCENT_COLOR     = (150, 160, 180)

    # ── Mouth / speaking state ───────────────────────────
    dv.speaking              = False
    dv.mouth_openness        = 0.1   # 0 = closed, 1 = fully open
    dv.target_openness       = 0.1
    dv.mouth_animation_speed = 0.05

    # ── Scaled eye dimensions ────────────────────────────
    dv.eye_width  = int(dv.BASE_EYE_WIDTH  * dv.FaceSize)
    dv.eye_height = int(dv.BASE_EYE_HEIGHT * dv.FaceSize)

    # ── Face position (screen center) ────────────────────
    dv.face_pos = (screen.get_width() // 2, screen.get_height() // 2)

    # ── Eye positions ────────────────────────────────────
    eye_spacing       = 220 * dv.FaceSize
    dv.left_eye_pos   = (screen.get_width() / 2 - eye_spacing / 2,
                         screen.get_height() / 2 - 70 * dv.FaceSize)
    dv.right_eye_pos  = (screen.get_width() / 2 + eye_spacing / 2,
                         screen.get_height() / 2 - 70 * dv.FaceSize)

    # ── Iris / pupil parameters ──────────────────────────
    dv.iris_radius  = int(dv.BASE_IRIS_RADIUS  * dv.FaceSize)
    dv.pupil_radius = int(dv.BASE_PUPIL_RADIUS * dv.FaceSize)
    dv.iris_shrink  = 0.9   # Less distortion when looking sideways

    # ── Eye animation control ────────────────────────────
    dv.pupil_offset_x = 0
    dv.target_offset  = 0
    dv.move_speed     = 3   # Pixels per frame
    dv.blink_duration = 0
    dv.max_swing      = (dv.eye_width // 2) - dv.iris_radius

    # ── Mouth position ───────────────────────────────────
    dv.mouth_width  = int(dv.BASE_MOUTH_WIDTH  * dv.FaceSize)
    dv.mouth_height = int(dv.BASE_MOUTH_HEIGHT * dv.FaceSize)
    dv.mouth_pos    = (screen.get_width()  / 2,
                       screen.get_height() / 2 + 80 * dv.FaceSize)

    # ── Runtime state ────────────────────────────────────
    dv.running = True

    # ── Button states ────────────────────────────────────
    dv.left_button_state  = "Start"     # "Start" or "Stop"
    dv.right_button_state = "sound_on"  # "sound_on" or "sound_off"
    dv.button_radius = int(25 * dv.FaceSize)
    
    # ── Socket / connection ──────────────────────────────
    dv.conn      = None
    dv.addr      = None
    dv.port      = None
    dv.server_socket = None
    dv.no_socket = False   # Overridden by --no-socket flag in main.py


    # ── Screen reference ─────────────────────────────────
    dv.screen = None

    # ── Audio ────────────────────────────────────────────
    dv.audio_dir      = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Audios")
    dv.pygame_title   = "Robotic Face"
    dv.audio_register = load_audio_register(dv.audio_dir)

    _instance = dv
    return _instance


def load_audio_register(audio_dir: str) -> SimpleNamespace:
    """
    Loads and validates the audio_register.json file from the Audios folder.
    Each entry maps a command name to an audio filename (including extension).
    Raises clear errors if the file is missing, malformed, or references missing audio files.
    """
    register_path = os.path.join(audio_dir, "audio_register.json")

    # Check register file exists
    if not os.path.exists(register_path):
        raise FileNotFoundError(
            f"Audio register not found at: {register_path}\n"
            f"Please create it with command-to-filename mappings."
        )

    # Parse JSON
    try:
        with open(register_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in audio_register.json: {e}")

    # Validate and build register
    register = SimpleNamespace()
    for command, filename in data.items():

        # Ensure flat structure — no nested objects
        if not isinstance(command, str):
            try:
                command = str(command)
            except Exception as e:
                raise TypeError(f"Command key '{command}' cannot be converted to string: {e}")

        if not isinstance(filename, str):
            try:
                filename = str(filename)
            except Exception as e:
                raise TypeError(f"Filename for '{command}' cannot be converted to string: {e}")

        # Verify audio file exists on disk
        file_path = os.path.join(audio_dir, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Audio file missing for command '{command}': {file_path}"
            )

        setattr(register, command, filename)

    return register
from config import get_config 

# --- Eye Movement Controls ---
# Eyes move horizontally by adjusting target_offset in config.
# The animation system smoothly interpolates toward this target each frame.

def EyeGoRight():
    """Move both eyes to the far right position."""
    cf = get_config()
    cf.target_offset = cf.max_swing

def EyesGoLeft():
    """Move both eyes to the far left position."""
    cf = get_config()
    cf.target_offset = -cf.max_swing

def EyesFoCenter():
    """Center both eyes."""
    get_config().target_offset = 0

def EyesGosTo(value: int):
    """
    Move eyes to a specific position on a 0-90 scale.
    0  = far left
    45 = center
    90 = far right
    """
    if value < 0:
        print(f"Invalid eye position: {value} — must be 0 or higher.")
        return
    if value > 90:
        print(f"Invalid eye position: {value} — must be 90 or lower.")
        return

    cf = get_config()
    cf.target_offset = (value - 45) * cf.max_swing / 45


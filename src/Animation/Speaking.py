from config import get_config

def start_speaking(duration=60):
    DataVariables = get_config()
    """Start speaking animation for the given duration (in frames)"""
    DataVariables.speaking = True
    # Start with slightly open mouth
    DataVariables.target_openness = 0.5
    
def stop_speaking():
    DataVariables = get_config()
    """Stop speaking animation and return mouth to neutral state"""
    DataVariables.speaking = False
    # Return to slightly open mouth for happy expression
    DataVariables.target_openness = 0.1
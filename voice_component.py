
import streamlit.components.v1 as components
from pathlib import Path

_COMPONENT_DIR = Path(__file__).parent / "voice_recorder"

voice_recorder = components.declare_component(
    "shree_ai_voice_recorder",
    path=str(_COMPONENT_DIR)
)


def record_voice(reset_token=0):

    return voice_recorder(
        reset_token=reset_token,
        default=None,
        key="shree_ai_voice_component",
        height=64,
    )

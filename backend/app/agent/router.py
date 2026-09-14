import re
from typing import Literal

def detect_intent(message: str) -> Literal["qa", "ship30", "artifact", "challenge"]:
    msg = message.lower()
    if re.search(r'\b(write|essay|ship30)\b', msg):
        return "ship30"
    if re.search(r'\b(create|document|artifact)\b', msg):
        return "artifact"
    if re.search(r'\b(challenge|disagree|critical)\b', msg):
        return "challenge"
    return "qa"

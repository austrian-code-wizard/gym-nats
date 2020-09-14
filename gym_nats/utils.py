import numpy as np
import base64
from enum import Enum

class Channels(Enum):
    UPDATE: str = 'rl.update'
    REWARD: str = 'rl.reward'
    ACTION: str = 'rl.action'
    RESET: str = 'rl.reset'
    ACTIONS: str = 'rl.actions'
    DONE: str = 'r.done'

def numpy_encode(array: np.ndarray) -> bytes:
    assert array.dtype == np.float64
    return base64.b64encode(array)

def numpy_decode(raw_array: bytes) -> np.ndarray:
    return np.frombuffer(base64.b64decode(raw_array), dtype=np.float64)

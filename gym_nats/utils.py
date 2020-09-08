import numpy as np
import base64
from enum import Enum

class Channels(Enum):
    update: str = 'rl.update'
    reward: str = 'rl.reward'
    action: str = 'rl.action'
    reset: str = 'rl.reset'
    actions: str = 'rl.actions'
    done: str = 'r.done'

def numpy_encode(array: np.ndarray) -> bytes:
    assert array.dtype == np.float64
    return base64.b64encode(array)

def numpy_decode(raw_array: bytes) -> np.ndarray:
    return np.frombuffer(base64.b64decode(raw_array), dtype=np.float64)

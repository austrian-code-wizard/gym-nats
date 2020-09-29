import base64
import asyncio
from typing import Tuple, Dict
import numpy as np
from gym import Env, spaces
from nats.aio.client import Client as NATS
from gym_nats.utils import Channels, numpy_decode, numpy_encode

class NatsEnv(Env):

    metadata = {'render.modes': ['human']}

    def __init__(self, host: str = "0.0.0.0", port: str = "4222", user: str = None, password: str = None):
        self.num_steps = 0
        self.nats = NATS()
        self.loop = asyncio.get_event_loop()
        self.loop.set_exception_handler(None)

        self.connect(host, port, user, password)

        number_inputs = self._next_observation().shape[0]

        raw_number_actions = self.request(Channels.ACTIONS)
        raw_number_actions = numpy_decode(raw_number_actions)
        number_actions = raw_number_actions.shape[0]
        
        self.observation_space = spaces.MultiBinary(number_inputs)
        self.action_space = spaces.Discrete(number_actions)

    def request(self, channel: str, data: bytes = b'') -> bytes:
        return self.loop.run_until_complete(self.nats.request(channel.value, data)).data

    def connect(self, host: str, port: str, user: str, password: str):
        connection_string = "nats://"
        if user is not None and password is not None:
            connection_string += f"{user}:{password}@"
        connection_string += f"{host}:{port}"
        self.loop.run_until_complete(self.nats.connect(connection_string, io_loop=self.loop, connect_timeout=1, max_reconnect_attempts=1, allow_reconnect=False))

    def _get_reward(self) -> int:
        reward_vector = numpy_decode(self.request(Channels.REWARD))
        return reward_vector.sum()

    def _take_action(self, action: int):
        action_vector = np.array([action], dtype=np.float64)
        self.request(Channels.ACTION, numpy_encode(action_vector))

    def _next_observation(self) -> np.array:
        return numpy_decode(self.request(Channels.UPDATE))

    def _is_done(self) -> bool:
        response = self.request(Channels.DONE)
        return numpy_decode(response).sum() > 0

    def step(self, action: int) -> Tuple[np.array, int, bool, Dict]:
        self._take_action(action)
        reward = self._get_reward()
        self.cur_state = self._next_observation()
        done = self._is_done()
        return self.cur_state, reward, done, {}

    def reset(self) -> np.array:
        self.request(Channels.RESET)
        return self._next_observation()

    def render(self, mode: str = 'human'):
        if mode != 'human':
            raise ValueError("Invalid rendering mode")
        print(f"Current state: {self.cur_state}")
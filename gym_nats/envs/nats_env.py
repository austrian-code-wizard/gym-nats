import base64
import asyncio
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

        self.connect(host, port, user, password)

        raw_number_inputs = self.request(Channels.UPDATE)
        raw_number_inputs = numpy_decode(raw_number_inputs)
        number_inputs = raw_number_inputs.shape[0] * raw_number_inputs.shape[1]

        raw_number_actions = self.request(Channels.ACTIONS)
        raw_number_actions = numpy_decode(raw_number_actions)
        number_actions = raw_number_actions.shape[0] * raw_number_actions.shape[1]
        
        self.observation_space = spaces.MultiBinary(number_inputs)
        self.action_space = spaces.Discrete(number_actions)

    def request(self, channel: str, data: bytes = b''):
        return self.loop.run_until_complete(self.nats.request(channel.value, data)).data

    def publish(self, channel: str, data: bytes = b''):
        self.loop.run_until_complete(self.nats.publish(channel.value, data))

    def connect(self, host, port, user, password):
        connection_string = "nats://"
        if user is not None and password is not None:
            connection_string += f"{user}:{password}@"
        connection_string += f"{host}:{port}"
        self.loop.run_until_complete(self.nats.connect(connection_string))

    def _get_reward(self):
        reward_vector = numpy_decode(self.request(Channels.REWARD))
        return reward_vector.sum()

    def _take_action(self, action):
        action_vector = np.array([action], dtype=np.float64)
        self.publish(Channels.ACTION, numpy_encode(action_vector))

    def _next_observation(self):
        return numpy_decode(self.request(Channels.UPDATE))

    def _is_done(self):
        response = self.request(Channels.DONE)
        return numpy_decode(response).sum() > 0

    def step(self, action):
        self._take_action(action)
        reward = self._get_reward()
        self.cur_state = self._next_observation()
        done = self._is_done()
        return self.cur_state, reward, done, {}

    def reset(self):
        self.publish(Channels.RESET)
        return self._next_observation()

    def render(self, mode='human'):
        if mode != 'human':
            raise ValueError("Invalid rendering mode")
        print(f"Current state: {self.cur_state}")
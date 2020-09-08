from gym import Env, spaces
import asyncio
import numpy as np
import base64
from gym_nats.utils import Channels, numpy_decode, numpy_encode
from nats.aio.client import Client as NATS

class NatsEnv(Env):

    metadata = {'render.modes': ['human']}

    def __init__(self, host="0.0.0.0", port="4222", user=None, password=None):
        self.num_steps = 0
        self.nats = NATS()
        self.loop = asyncio.get_event_loop()
        
        connection_string = "nats://"
        if user is not None and password is not None:
            connection_string += f"{user}:{password}@"
        self.loop.run_until_complete(self.nats.connect(connection_string))

        raw_number_inputs = self.loop.run_until_complete(self.nats.request(Channels.update, None)).data
        raw_number_inputs = numpy_decode(raw_number_inputs)
        number_inputs = raw_number_inputs.shape[0] * raw_number_inputs.shape[1]

        raw_number_actions = self.loop.run_until_complete(self.nats.request(Channels.actions, None)).data
        raw_number_actions = numpy_decode(raw_number_actions)
        number_actions = raw_number_actions.shape[0] * raw_number_actions.shape[1]
        
        self.observation_space = spaces.MultiBinary(number_inputs)
        self.action_space = spaces.Discrete(number_actions)

    def _get_reward(self):
        reward_vector = numpy_decode(self.loop.run_until_complete(self.nats.request(Channels.reward, None)).data)
        return reward_vector.sum()

    def _take_action(self, action):
        action_vector = np.array([action], dtype=np.float64)
        self.loop.run_until_complete(self.nats.publish(Channels.action, numpy_encode(action_vector)))

    def _next_observation(self):
        return numpy_decode(self.loop.run_until_complete(self.nats.request(Channels.update, None)).data)

    def _is_done(self):
        response = self.loop.run_until_complete(self.nats.request(Channels.done, None)).data
        return numpy_decode(response).sum() > 0

    def step(self, action):
        self._take_action(action)
        reward = self._get_reward()
        self.cur_state = self._next_observation()
        done = self._is_done()
        return self.cur_state, reward, done, {}

    def reset(self):
        self.loop.run_until_complete(self.nats.request(Channels.reset, None))
        return self._next_observation()

    def render(self, mode='human'):
        if mode != 'human':
            raise ValueError("Invalid rendering mode")
        print(f"Current state: {self.cur_state}")
import gym
import subprocess
import numpy as np
from unittest import TestCase

"""
Assumes that the nats-server was started on port 127.0.0.1 with "nats-server -a 127.0.0.1".
Assumes that simulation_test.py is running with NATS connection to port 127.0.0.1, "python simulation_test.py -o 127.0.0.1".
"""

class Test(TestCase):


    def setUp(self):
        """try:
            result = subprocess.run(["pkill",  "nats-server"])
            self.assertEqual(result.returncode, 0)
        except:
            raise ValueError("Could not kill the running nats-server")

        try:
            result = subprocess.run(["nats-server", "-a", "127.0.0.1 &"])
            self.assertEqual(result.returncode, 0)
        except:
            raise ValueError("Could not restart nats-server. Is nats-server installed on this system or is 127.0.0.1:4222 already in use?")"""
        self.env = gym.make('gym_nats:nats-v0', host="127.0.0.1")
        self.assertEqual(self.env.observation_space.n, 3)
        self.assertEqual(self.env.action_space.n, 2)

    def test_step(self):
        ACTION = 1
        state, reward, done, _ = self.env.step(ACTION)
        correct = np.array([1, 2, 3]).astype(np.float64)
        for value in zip(state, correct):
            self.assertEqual(value[0], value[1])

        correct = 10.0
        self.assertEqual(reward, correct)

        correct = False
        self.assertEqual(done, correct)

    def test_reset(self):
        obs = self.env.reset()
        correct = np.array([1, 2, 3]).astype(np.float64)
        print(obs)
        print(correct)
        for value in zip(obs, correct):
            self.assertEqual(value[0], value[1])

        
        


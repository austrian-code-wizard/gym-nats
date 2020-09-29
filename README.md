# gym-nats
----------
Connect reinforcement learning agents to your existing systems easily.

[![Build Status](https://travis-ci.com/austrian-code-wizard/gym-nats.svg?branch=master)](https://travis-ci.com/austrian-code-wizard/gym-nats) ![PyPI - License](https://img.shields.io/pypi/l/gym-nats) ![PyPI](https://img.shields.io/pypi/v/gym-nats) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gym-nats) 

Gym-nats is a package that helps connect existing systems to a reinforcement learning agent. Often time in RL, creating the apropriate environment to train an agent is a major obstacle, especially when working with distributed architectures. Gym-nats confirms to the [OpenAI Gym interface](https://github.com/openai/gym/blob/master/docs/creating-environments.md) and uses [Nats.io](https://nats.io) to connect to an existing system. If you want to apply reinforcement learning to a system that already uses [Nats.io](https://nats.io) this package is perfect for you! If your system currently does not use [Nats.io](https://nats.io), it is still easy to add that functionality – an example is given [HERE](https://github.com/austrian-code-wizard/gym-nats/tree/master/examples). Before using gym-nats, it might be useful to learn how the OpenAI Gym interface generally works, as described [HERE](https://ai-mrkogao.github.io/reinforcement%20learning/openaigymtutorial/)


## Supported platforms
Should be compatible with at least [Python +3.6](https://docs.python.org/3.6/library/asyncio.html).

## Prerequesites

Make sure you have [NATS installed](https://nats.io/download/nats-io/nats-server/) and are running a system with the necessary callbacks for this environment as described [HERE]()

## Considerations

At the moment, this environment only supports a MultiBinary observation space and a discrete action space. Learn more about OpenAI Gym spaces [HERE](https://gym.openai.com/docs/#spaces). If you want to add functionality to support more types of spaces, feel free to contribute to this project!

## Installation

Install from PyPi with:

```bash
pip install gym-nats
```

Alternatively, clone this repository, navigate inside of it and install locally with:
```bash
python setup.py install
```

## Setup

In order to use gym-nats, you need to have a system running that listens on the necessary NATS messaging channels, so that the environment can get the information it needs. The channel names are defined as an enum in [gym_nats.utils](https://github.com/austrian-code-wizard/gym-nats/blob/master/gym_nats/utils.py). The callbacks registered on these channels MUST all publish a response to the reply channel, so that they conform the NATS [request / response protocol](). The returned messages should be be followed (all Numpy ndarrays should be encoded before sending and decoded after receiving with [the provided utils functions](https://github.com/austrian-code-wizard/gym-nats/blob/master/gym_nats/utils.py)) and must be of dtype np.float64.

- Callback UPDATE: Ignores data sent. Reponds with ndarray of size (N,) with binary entries that corresponding to the current state of the system.
- Callback REWARD: Ignores data sent. Responds with ndarray of size (N,) with arbitrary entries where the sum of all entries represents the current reward for the model.
- Callback ACTION: Receives ndarray of size (1,) where the entry is a number specifying the next action to take. Responds with an empty byte (b'').
- Callback RESET: Ignores data sent. Resets the system for a new simulation run. Responds with an empty byte (b'').
- Callback ACTIONS: Ignores data sent. Responds with ndarray of size (N,) where N is the number of possible actions for this system. The values in this array are arbitrary.
- Callback DONE: Ignores data sent. Responds with ndarray of size (N,). If the sum of all entries is greater than 0, this signifies that the system is in the desired state (e.g. robot reached it's goal).

An example implementation for all these callbacks can be found [HERE](https://github.com/austrian-code-wizard/gym-nats/blob/master/examples/sample_simulation.py)

## Basic Usage

Make sure you have a compatible environment and a NATS server running at the correct host and port with the correct user and password credentials.

```python
import gym
import gym_nats
import numpy as np
from rl.agents.dqn import DQNAgent
from rl.memory import SequentialMemory
from tensorflow.keras.models import Sequential
from rl.policy import BoltzmannQPolicy, EpsGreedyQPolicy
from tensorflow.keras.optimizers import Adadelta, SGD, Adam
from tensorflow.keras.layers import Dense, Activation, Flatten

# specify environment name
ENV_NAME = 'gym_nats:nats-v0'

# This will instantiate the environment and connect to the Nats server, then query 
env = gym.make(ENV_NAME, host="127.0,0,1", port="4222", user=None, password=None)

```

Then you can create a simple model.

```python
nb_actions = env.action_space.n

# Next, we build a very simple model.
model = Sequential()
model.add(Flatten(input_shape=(1,env.observation_space.n)))
model.add(Dense(8))
model.add(Activation('relu'))
model.add(Dense(8))
model.add(Activation('relu'))
model.add(Dense(8))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))
print(model.summary())
```

Next, you can configure and create an agent.
```python
memory = SequentialMemory(limit=300, window_length=1)
policy = EpsGreedyQPolicy()
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=5,
        target_model_update=1e-2, policy=policy)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])
```

Finally, you can pass the environment to the agent, start training, test the agent, and save the trained model.
```python
dqn.fit(env, nb_steps=5000, visualize=True, verbose=2)
dqn.test(env, nb_episodes=1, visualize=True)
#Save the weights and model
dqn.save_weights(f"dqn_{ENV_NAME}_weights.h5f", overwrite=True)
model.save(f"dqn_{ENV_NAME}_model")
```

## Contribute

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

We Use [Github Flow](https://guides.github.com/introduction/flow/index.html), So All Code Changes Happen Through Pull Requests
Pull requests are the best way to propose changes to the codebase (we use [Github Flow](https://guides.github.com/introduction/flow/index.html)). We actively welcome your pull requests:

1. Fork the repo and create your branch from `master`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the docstrings and README.
4. Ensure the unittests pass.
5. Issue that pull request!
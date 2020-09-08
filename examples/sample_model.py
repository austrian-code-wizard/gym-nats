import gym
import gym_nats
import argparse
import numpy as np
from rl.agents.dqn import DQNAgent
from rl.memory import SequentialMemory
from tensorflow.keras.models import Sequential
from rl.policy import BoltzmannQPolicy, EpsGreedyQPolicy
from tensorflow.keras.optimizers import Adadelta, SGD, Adam
from tensorflow.keras.layers import Dense, Activation, Flatten

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--host', default='0.0.0.0', required=False)
    parser.add_argument('-p', '--port', default='4222', required=False)
    parser.add_argument('-u', '--user', default=None, required=False)
    parser.add_argument('-a', '--password', default=None, required=False)

    args = parser.parse_args()

    ENV_NAME = 'gym_nats:nats-v0'
    # Get the environment and extract the number of actions.
    env = gym.make(ENV_NAME, host=args.host, port=args.port, user=args.user, password=args.password)
    np.random.seed(123)
    env.seed(123)
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
    # Finally, we configure and compile our agent. You can use every built-in tensorflow.keras optimizer and
    # even the metrics!
    memory = SequentialMemory(limit=1000, window_length=1)
    policy = EpsGreedyQPolicy()
    dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=5,
            target_model_update=1e-2, policy=policy)
    dqn.compile(Adam(lr=1e-3), metrics=['mae'])

    dqn.fit(env, nb_steps=500, visualize=True, verbose=2)

    #Save the weights and model
    dqn.save_weights(f"dqn_{ENV_NAME}_weights.h5f", overwrite=True)
    model.save(f"dqn_{ENV_NAME}_model")
    dqn.test(env, nb_episodes=0, visualize=True)

if __name__ == "__main__":
    main()
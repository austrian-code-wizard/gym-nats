from gym.envs.registration import register

register(
    id='nats-v0',
    entry_point='gym_nats.envs:NatsEnv',
    kwargs={
        "host": "0.0.0.0", 
        "port": "4222", 
        "user": None, 
        "password": None
    }
)
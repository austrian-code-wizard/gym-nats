from setuptools import setup

setup(name='gym_nats',
      version='0.1',
      install_requires=['gym', 'asyncio-nats-client', 'numpy']  # And any other dependencies foo needs
)
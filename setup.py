from setuptools import setup

setup(
  name = 'gym-nats',         
  packages = ['gym_nats'],   
  version = '0.1.2',     
  license='MIT',
  description='OpenAI Gym environment interfacing with NATS.io',    
  long_description = 'Implements an OpenAI gym environment using NATS.io. Using this environment, a reinforcement learning agent can use the environment to learn from any source \
        of data since NATS.io can feed arbitrary data into the environment. For further information on the interface check out the README file.',
  author = 'Moritz Pascal Stephan',
  author_email = 'moritz.stephan@gmx.at',
  url = 'https://github.com/austrian-code-wizard/gym-nats',
  download_url = 'https://github.com/austrian-code-wizard/gym-nats/archive/v_01.tar.gz',
  keywords = ['nats', 'reinforcement learning', 'openai'],  
  install_requires=['gym', 'asyncio-nats-client', 'numpy'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)
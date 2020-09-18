from distutils.core import setup

setup(
  name = 'gym-nats',         
  packages = ['gym_nats'],   
  version = '0.1',     
  license='MIT',        
  description = 'Implements an OpenAI gym environment using NATS.io. Using this environment, a reinforcement learning agent can use the environment to learn from any source \
        of data since NATS.io can feed arbitrary data into the environment. For further information on the interface check out the README file.',
  author = 'Moritz Pascal Stephan',                   # Type in your name
  author_email = 'moritz.stephan@gmx.at',      # Type in your E-Mail
  url = 'https://github.com/austrian-code-wizard/gym-nats',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/austrian-code-wizard/gym-nats/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=['gym', 'asyncio-nats-client', 'numpy'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Reinforcement Learning',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)
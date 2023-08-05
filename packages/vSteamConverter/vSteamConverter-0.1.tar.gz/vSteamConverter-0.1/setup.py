from distutils.core import setup
setup(
  name = 'vSteamConverter',         # How you named your package folder (MyLib)
  packages = ['vSteamConverter'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = "Steam Games id's to Game names",   # Give a short description about your library
  author = 'Vitor Henrique Costa Ferreira',                   # Type in your name
  author_email = 'vitor.ferreira@oraculodecisor.com.br',      # Type in your E-Mail
  url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/STHEe/vSteamConverter/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Steam', 'GameID', 'Games'],   # Keywords that define your package best
  install_requires=[
          'json',
          'Thread',
          'requests',
          'json',
          'time'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',

    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
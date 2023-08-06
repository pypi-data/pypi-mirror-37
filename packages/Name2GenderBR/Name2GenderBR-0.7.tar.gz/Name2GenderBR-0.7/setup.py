from setuptools import setup

setup(
  name = 'Name2GenderBR',         # How you named your package folder (MyLib)
  packages = ['Name2GenderBR'],   # Chose the same as "name"
  version = '0.7',      # Start with a small number and increase it with every change you make
  license='GNU GPL v3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Data analysis of name and gender of Brazilian population. Enables gender definition by name.',   # Give a short description about your library
  author = 'Leonardo A. de Jesus',                   # Type in your name
  author_email = 'leonardoaraujo@id.uff.br',      # Type in your E-Mail
  url = 'https://github.com/leonardoaj/name2gender-br',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/leonardoaj/name2gender-br/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['gender', 'genero', 'brazillian', 'brazil', 'censo', 'census'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'python-levenshtein',
      ],
  include_package_data=True,
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
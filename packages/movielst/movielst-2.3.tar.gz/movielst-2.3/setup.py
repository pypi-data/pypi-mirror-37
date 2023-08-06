from setuptools import setup

setup(name='movielst',
      version='2.3',
      description='Everything about your movies within the command line.',
      long_description=open('README.md', 'r').read(),
      long_description_content_type='text/markdown',
      url='https://github.com/Mozzo1000/movielst',
      author='Andreas Backström',
      author_email='andreas@simplymozzo.se',
      license='MIT',
      include_package_data=True,
      packages=['movielst', 'web'],
      entry_points={
                'console_scripts': ['movielst=movielst:main', 'movielst_web=web.main:main']
           },
      install_requires=[
          'guessit',
          'terminaltables',
          'tqdm',
          'colorama',
          'xlsxwriter',
          'flask',
          'Flask-WTF'
      ],
      keywords=['movies', 'CLI', 'movies-within-CLI', 'python'],
      classifiers=[
          'Environment :: Console',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.4',
          'Topic :: Utilities',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development :: User Interfaces',
          'Topic :: Software Development :: Version Control',
      ],)

from setuptools import setup

setup(name='algovent_utils',
      version='0.11',
      description='utils to support django-algovent framework',
      url='https://github.com/algovent/algovent_utils',
      author='Naveen Bollimpalli',
      keywords='rest utilities utils django algovent',
      author_email='naveenbollimpalli@gmail.com',
      license='MIT',
      packages=['algovent_utils'],
      install_requires=[
          'django-rest-framework',
      ],
      zip_safe=False)
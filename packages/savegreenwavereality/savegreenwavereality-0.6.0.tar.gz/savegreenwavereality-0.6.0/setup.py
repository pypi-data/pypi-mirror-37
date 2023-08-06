from setuptools import setup

setup(
    name='savegreenwavereality',
    version='0.6.0',
    packages=['savegreenwavereality'],
    install_requires=[
          'requests',
          'xmltodict',
          'urllib3',
      ],
    url='https://github.com/lukewakeford/greenwavereality',
    license='MIT',
    author='David Fiel',
    author_email='github@dfiel.com',
    description='Re-upload of David Fiels repo with fixes for TCP light control on Hassio - Control of Greenwave Reality Lights'
)

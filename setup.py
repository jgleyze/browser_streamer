from setuptools import setup

setup(
    name='browser_streamer',
    version='0.1',
    packages=['browser_streamer'],
    package_data={'browser_streamer': ['templates/*']},
    install_requires=[
        'flask',
        'opencv-python',
        'numpy',
    ],
    
)
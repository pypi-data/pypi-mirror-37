from setuptools import setup, find_packages

setup(
    name='nhlapi',
    version='0.0.3',
    description='an API used to parse JSON data from the NHL website',
    license='MIT',
    author='Ryan Christilaw',
    author_email='ryan.christilaw@gmail.com',
    keywords=['nhl scores'],
    url='https://github.com/rchristilaw/nhlapi',
    packages=find_packages(),
    install_requires=[
        'requests',
        'python-dateutil',
        'pytz'
    ]
)

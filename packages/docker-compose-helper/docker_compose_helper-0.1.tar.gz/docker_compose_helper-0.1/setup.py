from distutils.core import setup

setup(
    name='docker_compose_helper',
    version='0.1',
    author='Lauri Hintsala',
    author_email='lauri.hintsala@verkkopaja.fi',
    description='Docker compose helper',
    entry_points={
        'console_scripts': [
            'dc=docker_compose_helper.main:main',
        ],
    },
    packages=['docker_compose_helper'],
    install_requires=['docker_compose'],
)

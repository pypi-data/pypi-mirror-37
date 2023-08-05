from setuptools import setup

setup(
    name='muxminos',
    version='0.2.4',
    author='hujianxin',
    author_email='hujianxin@xiaomi.com',
    include_package_data=True,
    install_requires=['fire', 'gitpython', 'pyyaml', 'configobj'],
    license='Apache License',
    packages=['muxminos'],
    description='A cmd tool for tmuxinator generating configuration file for minos',
    entry_points={
        'console_scripts': [
            'muxminos=muxminos.cmd:main',
            'mm=muxminos.cmd:main'
        ]
    }
)

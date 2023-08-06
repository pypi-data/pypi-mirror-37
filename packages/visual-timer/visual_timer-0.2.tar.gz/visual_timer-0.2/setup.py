try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='visual_timer',  
    version='0.2',
    description="Visual timer is a simple terminal based timer",
    author="nerd1pypi",
    authoremail="nerd1pypi@cock.li",
    license="MIT",
    url="https://github.com/nerd-1/visual_timer",
    keywords=[
        "console",
        "countdown",
        "curses",
        "terminal",
        "timer",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console :: Curses",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    install_requires=[],
    py_modules=['visual_timer'],
)

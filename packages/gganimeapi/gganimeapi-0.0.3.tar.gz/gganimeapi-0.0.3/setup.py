from setuptools import setup
import setuptools
setup(
    name='gganimeapi',
    version='0.0.3',
    author='Ahmed Khatab',
    author_email='h.e.t.a.k.m@gmail.com',
    scripts=['bin/anime.py'],
    #url="http://pypi.python.org/pypi/gganime/",
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='Anime Unoffical Api',
     packages=setuptools.find_packages(),
     install_requires=[
        "bs4",
        "requests",
    ],

)

from setuptools import find_packages, setup

long_description="This library's source code lives at https://github.com/jrheard/madison_axi and its documentation lives at http://madison-axi.readthedocs.io/."

setup(
    name="madison_axi",
    version="0.1.0",
    description="A library that allows users to directly control an AxiDraw by writing Python code.",
    long_description=long_description,
    url="http://github.com/jrheard/madison_axi",
    author="JR Heard",
    author_email="jrrrheard@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=['requests'],
)

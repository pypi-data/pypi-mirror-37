from setuptools import setup

setup(
    name='novamud',
    version='0.0.2',
    description='Simple and flexible mud framework for people with only basic '
                'knowledge of python',
    author='Sam Hopkins',
    author_email='sam@daredata.engineering',
    url='https://gitlab.com/hershaw/novamud',
    long_description=open('README.md').read(),
    packages=['novamud'],
    install_requires=[
        'websockets==6.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)

"""
The setup package to install TensorPy dependencies.
*> This does NOT include TensorFlow installation.
*> To install TensorFlow, use "./install.sh"
"""

from setuptools import setup, find_packages  # noqa

setup(
    name='tensorpy',
    version='1.3.0',
    url='http://tensorpy.com',
    author='Michael Mintz',
    author_email='mdmintz@gmail.com',
    maintainer='Michael Mintz',
    description='Easy Image Classification with TensorFlow!',
    license='The MIT License',
    install_requires=[
        'six',
        'requests==2.20.0',
        'Pillow==4.1.1',
        'BeautifulSoup4>=4.6.0',
    ],
    packages=['tensorpy'],
    entry_points={
        'console_scripts': [
            'classify = tensorpy.classify:main',
        ],
    },
)

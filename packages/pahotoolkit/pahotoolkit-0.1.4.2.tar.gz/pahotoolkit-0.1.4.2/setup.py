import codecs
import os

from setuptools import setup


__version__ = os.getenv('TAG', '0.1.4.2')


URL = 'https://bitbucket.org/kiotsystem/paho-toolkit'

download_url = '{url}/get/{version}.tar.gz'.format(url=URL,
                                                   version=__version__)


def open_local(paths, mode='r', encoding='utf8'):
    path = os.path.join(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            *paths
        )
    )

    return codecs.open(path, mode, encoding)


with open_local(['README.md']) as readme:
    long_description = readme.read()


with open_local(['requirements.txt']) as req:
    install_requires = req.read().split("\n")


keywords = ['paho', 'eclipse', 'mqtt', 'toolkit', 'framework']


# http://peterdowns.com/posts/first-time-with-pypi.html
# https://bitbucket.org/kiotsystem/paho-toolkit/get/0.1b2.tar.gz
setup(
    name='pahotoolkit',
    packages=['pahotoolkit'],
    version=__version__,
    description='Paho\'s MQTT dev Toolkit',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Arnulfo Solis',
    author_email='arnulfojr94@gmail.com',
    url=URL,
    download_url=download_url,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=install_requires,
    keywords=keywords,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)

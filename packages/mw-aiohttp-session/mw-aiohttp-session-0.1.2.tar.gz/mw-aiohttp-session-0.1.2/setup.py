from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='mw-aiohttp-session',
    version='0.1.2',
    description='maxwin aiohttp-session ',
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://bitbucket.org/maxwin-inc/mw-aiohttp-session/src',  # Optional
    author='candyabc',  # Optional
    author_email='hfcandyabc@163.com',  # Optional
    packages=find_packages(),  # Required
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['aiohttp>=3.0.1','aiohttp_session']
)


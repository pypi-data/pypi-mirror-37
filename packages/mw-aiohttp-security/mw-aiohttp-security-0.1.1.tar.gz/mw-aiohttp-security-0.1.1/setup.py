from setuptools import setup, find_packages
from codecs import open
import os

def read(f):
    return open(os.path.join(os.path.dirname(__file__), f),encoding='utf8').read().strip()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    # And where it will live on PyPI: https://pypi.org/project/mw-aiohttp-security/
    name='mw-aiohttp-security',  # Required
    version='0.1.1',  # Required
    description='maxwin aiohttp security',  # Required
    long_description='\n\n'.join((read('README.rst'), read('CHANGES.txt'))),
    url='https://bitbucket.org/maxwin-inc/mw-aiohttp-security/src',  # Optional
    author='cxhjet',  # Optional
    author_email='cxhjet@qq.com',  # Optional
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='maxwin commonlib security check_auth check_permission',  # Optional
    # packages=find_packages(exclude=['test','test.*']),  # Required
    packages=find_packages(),  # Required
    install_requires=['aiohttp-security>=0.4.0','mw-aiohttp-session>=0.1.2','mwsdk>=0.2.0'],  # Optional
    include_package_data=True,
    project_urls={  # Optional
        'Bug Reports':'https://bitbucket.org/maxwin-inc/auth/issues?status=new&status=open',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://bitbucket.org/maxwin-inc/mw_aiohttp_security/src',
    },
)


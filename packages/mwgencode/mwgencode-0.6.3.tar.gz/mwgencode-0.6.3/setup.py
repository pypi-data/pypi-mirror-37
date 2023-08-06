from setuptools import setup, find_packages
from codecs import open
from os import path
import os

def read(f):
    return open(os.path.join(os.path.dirname(__file__), f),encoding='utf8').read().strip()


setup(
    name='mwgencode',
    version='0.6.3',
    author='cxhjet',
    author_email='cxhjet@qq.com',
    description="根据starUML文档产生flask专案的代码",
    long_description='\n\n'.join((read('README.rst'), read('CHANGES.txt'))),
    url='https://bitbucket.org/maxwin-inc/gencode/src/',  # Optional

    py_modules=['manage'],
    packages=['gencode',
              'gencode.gencode',
              'gencode.importxmi',
              'gencode.importmdj',
              'gencode.gencode.sample',
              'gencode.gencode.template',
              'gencode.gencode.template.tests',
              'gencode.gencode.sample.seeds'
           ],
    package_data={
        '': ['*.*']
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
                      'mwutils>=0.1.24',
                      'mwauth>=0.4.24',
                      'mwsdk>=0.2.5',
                      'mwpermission>=0.1.21',
                      'mw-aiohttp-session>=0.1.2',
                      'mw-aiohttp-babel>=0.1.7',
                      'mw-aiohttp-security>=0.1.1',
                      'SQLAlchemy','pyJWT',
                      'python-consul',
                      'flask_migrate','pyjwt',
                      'flask-babel',
                      'Flask-Cors','Flask-Redis'

                      ],
    include_package_data=True,
    # 可以在cmd 执行产生代码
    entry_points={
        'console_scripts': ['gencode=manage:main']
    }
)

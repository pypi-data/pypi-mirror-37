from setuptools import setup, find_packages
from codecs import open
from os import path
import os

def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


setup(
    name='mwgencode',
    version='0.6.0',
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
    install_requires=['mw-aiohttp-security>=0.1.0','mwutils>=0.1.23',
                      'mwauth>=0.4.23','flask_migrate','pyjwt','mwsdk>=0.2.3',
                      'python-consul', 'flask-babel','mw-aiohttp-babel>=0.1.3',
                      'SQLAlchemy','pyJWT','Flask-Cors','Flask-Redis',
                      'mwpermission>=0.1.19',
                      'mw-aiohttp-session>=0.1.2'],
    include_package_data=True,
    # 可以在cmd 执行产生代码
    entry_points={
        'console_scripts': ['gencode=manage:main']
    }
)

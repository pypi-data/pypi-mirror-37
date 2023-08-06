import os
from setuptools import setup, find_packages


version = '0.2.1'
README = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = open(README).read()
setup(
    name='Flask-Yolo2API',
    version=version,
    description='Simply the best Flask API library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Programming Language :: Python'
    ],
    keywords='flask api flapi yoloapi',
    author='Sander Ferdinand, Daniel Ternyak',
    author_email='sa.ferdinand@gmail.com',
    url='https://github.com/skftn/flask-yoloapi',
    install_requires=[
        'animal-case',
        'flask',
        'python-dateutil'
    ],
    extra_requires=[
        'pytest',
        'pytest-flask',
        'pytest-cov'
    ],
    setup_requires=['setuptools>=38.6.0'],
    packages=find_packages(),
    include_package_data=True,
)

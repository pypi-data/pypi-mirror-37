import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='photos-picker',
    version='0.1.2',
    description='Pick photos following a given strategy and upload them to various destinations',
    author='Laurent VOULLEMIER',
    author_email='laurent.voullemier@gmail.com',
    url='https://github.com/l-vo/photos-picker',
    packages=find_packages(),
    install_requires=['Pillow', 'zope.event', 'dropbox'],
    include_package_data=True,
    zip_safe=False,
    long_description=read('README.md'),
    license='MIT',
    keywords='photos upload photoframe',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2'
    ]
)

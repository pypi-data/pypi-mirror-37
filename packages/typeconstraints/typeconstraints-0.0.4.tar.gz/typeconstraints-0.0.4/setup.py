from setuptools import setup, find_packages
from os import path

setup(
    name='typeconstraints',
    version='0.0.4',
    description='Type Constraints Decorator',
    long_description="""A decorator for aserting function argument type constraints.

    Python decorator for adding function argument type constraint checks to finction invocations.
    """,
    url='https://github.com/pibara-utopian/typeconstraints',
    author='Rob J Meijer',
    author_email='pibara@gmail.com',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Environment :: Other Environment',
    ],
    keywords='assert type constraints',
    packages=find_packages(),
)

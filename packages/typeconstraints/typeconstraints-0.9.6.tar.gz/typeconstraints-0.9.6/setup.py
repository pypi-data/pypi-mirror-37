from setuptools import setup, find_packages
from os import path

setup(
    name='typeconstraints',
    version='0.9.6',
    description='Type Constraints Decorator',
    long_description="""Type Constraints Decorator.
==============================

Python decorator for adding function argument type constraint checks to function invocations.

Using the typeconstraints decorator allows you to defensively use asertions of argument types

and return value types of functions and methods. 

The module allows the use of custom type constraint asertion classes and comes with a small set

of pre-defined type constaint asertion classes.

Basic usage:

..code python
  from typeconstraints import typeconstraints,ARRAYOF
  
  @typeconstraints([int,str,ARRAYOF(int)])
  
  def simple_function(foo,bar,baz):
  
  pass
  
  simple_function(42,"hi there",[1,1,2,3,5,8,13,21])


For more information on usage, consult the `tutorial`_.

.. _tutorial: https://steemit.com/@mattockfs

""",
    url='https://steemit.com/@mattockfs',
    download_url='https://github.com/pibara-utopian/typeconstraints',
    bugtrack_url='https://github.com/pibara-utopian/typeconstraints/issues',
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

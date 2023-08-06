from distutils.core import setup

import pysexp

setup(
    name='pysexp',
    version=pysexp.__version__,
    py_modules=['pysexp'],
    author=pysexp.__author__,
    author_email='jdboyd@jdboyd.net',
    url='https://github.com/jd-boyd/pysexp',
    license=pysexp.__license__,
    description='S-expression parser for Python',
    long_description=pysexp.__doc__,
    keywords='s-expression, lisp, parser',
    classifiers=[
        "Development Status :: 3 - Alpha",
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Lisp",
        "Programming Language :: Emacs-Lisp",
        # see: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
)

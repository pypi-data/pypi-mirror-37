from setuptools import setup, find_packages

version = '0.0.16'
name = 'japanmap'
short_description = '`japanmap` is a package for Japanese map.'
long_description = """\
`japanmap` is a package for Japanese map.
::

   import matplotlib.pyplot as plt
   from japanmap import picture, get_data, pref_map
   pct = picture({'北海道': 'blue'})  # numpy.ndarray
   # pct = picture({1: 'blue'})  # same to above
   plt.imshow(pct)  # show graphics
   plt.savefig('map.png')  # save to PNG file
   svg = pref_map(range(1,48), qpqo=get_data())  # IPython.display.SVG
   print(svg.data)  # SVG source

Requirements
------------
* Python 3, Numpy

Features
--------
* nothing

Setup
-----
::

   $ pip install japanmap

History
-------
0.0.1 (2016-6-7)
~~~~~~~~~~~~~~~~~~
* first release

"""

classifiers = [
   "Development Status :: 1 - Planning",
   "License :: OSI Approved :: Python Software Foundation License",
   "Programming Language :: Python",
   "Topic :: Software Development",
   "Topic :: Scientific/Engineering",
]

setup(
    name=name,
    version=version,
    description=short_description,
    long_description=long_description,
    classifiers=classifiers,
    #py_modules=['japanmap'],
    package_data = {
        'japanmap': ['japan.pkl', 'japan0.16.pkl', 'japan.png'],
    },
    packages=find_packages(),
    keywords=['japanmap',],
    author='Saito Tsutomu',
    author_email='tsutomu.saito@beproud.jp',
    url='https://pypi.python.org/pypi/japanmap',
    license='PSFL',
    install_requires=['numpy'],
)

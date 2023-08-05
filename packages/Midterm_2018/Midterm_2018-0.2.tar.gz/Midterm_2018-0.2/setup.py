from distutils.core import setup
 
setup(
    name = 'Midterm_2018', # a unique name for PyPI
    version = '0.2',
    description = 'Webscraper to develope unitest skills',
    author= 'Mitchell Sheep',
    author_email='mlsheep226@students.ecsu.edu',
    url='http://lin-chen-va.github.io', # http://location or https://location
    packages=['helper', ], # packages and subpackages containing .py files
    package_dir={'':'src'},
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    package_data={'helper':['other/*']}, # other needed files will be installed for user
    py_modules=[], # individual modules
    scripts=['src/main',], # the executable files will be installed for user
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README').read(),
    # more meta-data for repository
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: X11 Applications :: GTK',
      'Intended Audience :: End Users/Desktop',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License (GPL)',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python',
      'Topic :: Desktop Environment',
      'Topic :: Text Processing :: Fonts'
      ],
)

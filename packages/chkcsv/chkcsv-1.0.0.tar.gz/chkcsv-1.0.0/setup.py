from distutils.core import setup

setup(name='chkcsv',
	version='1.0.0',
	description="Checks the format of a CSV file with respect to a specifed set of column names and types.",
	author='Dreas Nielsen',
	author_email='dreas.nielsen@gmail.com',
	url='https://bitbucket.org/rdnielsen/chkcsv/',
	scripts=['chkcsv/chkcsv.py'],
	requires=[],
	python_requires = '>=2.7',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Environment :: Console',
		'Intended Audience :: End Users/Desktop',
		'License :: OSI Approved :: GNU General Public License (GPL)',
		'Natural Language :: English',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 2.7',
		'Operating System :: OS Independent',
		'Topic :: Text Processing :: General',
		'Topic :: Office/Business',
		'Topic :: Scientific/Engineering',
		'Topic :: Text Processing',
		'Topic :: Utilities'
		],
	long_description="""``chkcsv.py`` is a Python module and program 
that checks the format of data in a CSV file.  It can check whether required
columns and data are present, and the type of data in each column.  Pattern
matching using regular expressions is supported.

Complete documentation is at http://chkcsv.readthedocs.io/."""
	)

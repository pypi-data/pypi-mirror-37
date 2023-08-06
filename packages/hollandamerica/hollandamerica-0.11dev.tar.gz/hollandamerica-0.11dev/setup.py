from distutils.core import setup

setup(
	name='hollandamerica',
	version='0.11dev',
	packages=['holam',],
	license='MIT',
	long_description=open('README.txt').read(),	
	install_requires=[
		'beautifulsoup4',
		'pandas',
		'selenium',
		'langdetect',
		'urllib'
	],
)

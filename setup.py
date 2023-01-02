#!/usr/env/bin python3

from setuptools import setup

description = 'A Minimal python-vlc Tkinter Helper Library'
__version__ = '1.0.0'

try:
	long_description = open('README.md', 'r').read()
except IOError:
	long_description = description

setup(
	name='tkvlc',
	version=__version__,
	packages=['tkvlc'],
	author='Safwan Ljd',
	license_files=('LICENSE',),
	description=description,
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://gitlab.com/SafwanLjd/PyTkinterVLC',
	download_url='https://gitlab.com/SafwanLjd/PyTkinterVLC/-/archive/' + __version__ + '/PyTkinterVLC-' + __version__ + '.tar.gz',
	install_requires=['python-vlc'],
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Natural Language :: English',
		'Programming Language :: Python :: 3',
	],
)

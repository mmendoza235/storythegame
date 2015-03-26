import os
from setuptools import setup, find_packages

# Utility function for README.md file
def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name = "storythegame",
	version = "0.0.1",
	author = "Miguel Mendoza",
	author_email = "miguel.an.mendoza@gmail.com",
	description = ("A story driven text game focused on customization "
					"and built on dreams."),
	keywords = "story game",
	packages = find_packages(),
	long_description = read("README.md")
)
from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in pp_addon/__init__.py
from pp_addon import __version__ as version

setup(
	name="pp_addon",
	version=version,
	description="PP Addon",
	author="magdyabouelatta",
	author_email="mabualata1@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

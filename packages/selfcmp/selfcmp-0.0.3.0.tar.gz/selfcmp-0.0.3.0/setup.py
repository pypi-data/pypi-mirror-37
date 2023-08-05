from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call
import platform

class PostDevelopCommand(develop):
	"""Post-installation for development mode."""
	def run(self):
		develop.run(self)

class PostInstallCommand(install):
	"""Post-installation for installation mode."""
	def run(self):
		install.run(self)

requires = []

setup(
	name = 'selfcmp',
	version = '0.0.3.0',
	packages = find_packages(),
	author = 'VictoryCzt',
	author_email = '1251939098@qq.com',
	url = 'https://gitlab.com/VictoryCzt/selfcmp',
	license = '',
	description = 'find the error in your program! For OIer and ACMer',
	cmdclass = {
		'develop': PostDevelopCommand,
		'install': PostInstallCommand,
	},
	install_requires = requires,
	setup_requires = requires,
	packages_data = {
		'selfcmp': ['selcmp/*.*','sample/*.*']
	}
)

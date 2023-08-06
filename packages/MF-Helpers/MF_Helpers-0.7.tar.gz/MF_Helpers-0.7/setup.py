from setuptools import setup, find_packages
import version

setup(name='MF_Helpers',
	version=version.get_version(),
	description='Modeling Factory Utilities',
	url='https://vc-bds002.vimpelcom.global/model-factory/MF_Helpers',
	author='Natalia Galanova',
	author_email='NGalanova@nsk.beeline.ru',
	packages=find_packages(),
	install_requires=[ 'numpy', 'pandas', 'sklearn', 'datetime'])
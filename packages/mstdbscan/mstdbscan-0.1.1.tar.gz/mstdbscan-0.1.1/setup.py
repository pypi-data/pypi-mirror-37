from distutils.core import setup

setup(
	name = 'mstdbscan',
	packages = ['mstdbscan'],
	install_requires = [
		"pandas",
		"geopandas",
		"python-louvain",
		"numpy",
		"scipy",
		"shapely",
		"imageio"],
	version = '0.1.1',
	description = 'An algorithm for space-time transmission clustering.',
	author = 'Fei-Ying Felix Kuo',
	author_email = 'fykuofelix@gmail.com',
	keywords = ['MST_DBSCAN', "Space-time", "transmission", "cluster"]
)

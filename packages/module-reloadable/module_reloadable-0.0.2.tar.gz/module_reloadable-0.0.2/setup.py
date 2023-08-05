import setuptools

with open("README.md", "r") as readme_:
	long_description = readme_.read()

setuptools.setup(
	name="module_reloadable",
	version="0.0.2",
	author="Leon Maksim",
	author_email="le_ma_@mail.ru",
	description="Module Reloadable",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/leonmaks/module_reloadable",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)

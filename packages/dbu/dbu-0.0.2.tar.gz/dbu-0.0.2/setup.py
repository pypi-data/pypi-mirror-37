import setuptools

with open("README.md", "r") as readme_:
	long_description = readme_.read()

setuptools.setup(
	name="dbu",
	version="0.0.2",
	author="Leon Maksim",
	author_email="le_ma_@mail.ru",
	description="DB Utils",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/leonmaks/dbu",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)

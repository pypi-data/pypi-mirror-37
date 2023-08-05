if __name__ == '__main__':
	import setuptools

	with open("README.md", "r") as fh:
	    long_description = fh.read()

	setuptools.setup(
	    name="the1owl",
	    version="0.0.7",
	    author="the1owl",
	    author_email="the1owlML@hotmail.com",
	    license='MIT',
	    description="the1owl Python module",
	    long_description=long_description,
	    long_description_content_type="text/markdown",
	    url="http://the1owl.com",
	    packages=setuptools.find_packages(),
	    classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	    ],
	    py_modules=[
		"scipy",
		"numpy",
		"pandas",
		"matplotlib",
		"sklearn",
		"xgboost",
		"lightgbm",
		"catboost"
	    ],
	    install_requires=[
		"scipy",
		"numpy",
		"pandas",
		"matplotlib",
		"sklearn"
	    ]
	)

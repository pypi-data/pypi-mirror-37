import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bibtex_format_rita",
    version="0.0.7",
    author="Matheus Cruz",
    author_email="mlcruz@inf.ufrgs.br",
    description="Implements simple bibtex bibliography file formating functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mlcruz/TeXArticleFormater",
    packages=setuptools.find_packages(),
	include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	 install_requires=[
		  'regex',
		  'click',
		  'requests',
      ],
	      dependency_links=[
		'https://pypi.org/project/regex/', 
        'https://pypi.org/project/click/',
		'https://pypi.org/project/requests/',
    ],
	scripts=['bibformat.py','unix_bibformat.py'],
	
)
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name="inquant",
    version="1.1.9",
    author="inquant",
    author_email="sunliusi@hotmail.com",
    description="inquant future quant api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.inquantstudio.com/",
    packages=setuptools.find_packages(),
    install_requires=['pythonnet>=2.3.0',],
    package_data = {
        '': ['*.dll','*.json','*.bat'],
    },
    classifiers=['Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],)

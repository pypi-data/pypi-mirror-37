import setuptools

setuptools.setup(
        name='digitextractor',
        version='0.0.1',
        author='Feng Liu',
        author_email='feng3245@gmail.com',
        description='Simple package for extracting digits',
        long_description='Extract computer uniform digits from plain white background with utilities for grouping rows and columns',
        long_description_content_type="text/markdown",
        packages=setuptools.find_packages(),
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",]
        )

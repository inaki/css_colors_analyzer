from setuptools import setup, find_packages

setup(
    name="css-color-analyzer",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'css-color-analyzer=css_color_analyzer.analyzer:main',
        ],
    },
    author="inaki",
    author_email="iiaranzadi@gmail.com",
    description="A tool to analyze colors in CSS and other web files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/inaki/css-color-analyzer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
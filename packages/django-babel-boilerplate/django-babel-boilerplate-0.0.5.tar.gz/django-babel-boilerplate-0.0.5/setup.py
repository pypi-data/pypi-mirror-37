import setuptools
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-babel-boilerplate",
    version="0.0.5",
    author="Navaneeth Nagesh",
    author_email="navaneethnagesh56@gmail.com",
    description="A package which create django babel boilerplate.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'Django>=2.1.1',
        'django-inline-svg>=0.1.1'
        ],
    url="https://www.navaneethnagesh.com",
    
    entry_points = {
        'console_scripts': ['django-babel=django_babel_boilerplate.command_line:main'],
    },
    keywords="Django, babel, sass",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
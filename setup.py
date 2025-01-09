'''
Setup.py file is an essential part of packaging and distributing python 
projects. It is used by setupTools to define the configuration of the project
such as its meta-data, dependencies, and more.
'''
from typing import List
from setuptools import find_packages, setup 

def get_requirements() -> List[str]:

    requirement_list:List[str] = []

    try:
        with open('requirements.txt','r') as file:
            # read the lines from the file
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()

                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("Requirements.txt file not found")
    
    return requirement_list

setup(
    name="NetworkSecurity",
    version="0.0.0.1",
    author="Nitin Flavier",
    author_email="nitinflavier13@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)


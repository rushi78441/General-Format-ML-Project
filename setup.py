from setuptools import setup, find_packages 
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path:str)-> List[str]:
    """
    This function reads a requirements file and returns a list of packages.
    It removes any comments or empty lines.
    """
    with open(file_path, 'r') as fileobj:
        requirements = fileobj.readlines()
    
    # Clean up the requirements list
    requirements = [req.replace('n','') for req in requirements]
    if HYPHEN_E_DOT in requirements:
        requirements.remove(HYPHEN_E_DOT)
    return requirements

setup(
    name='General_Format_ML_Project',
    version='0.0.1',
    author='RUSHI',
    author_email='rushi78441@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
)
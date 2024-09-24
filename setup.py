from setuptools import find_packages,setup
from typing import List

HYPHEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    This will return requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements= file_obj.readlines()
        requirements = [req.replace("/n","") for req in requirements]
        # Hyphen E dot triggers the setup.py file but need to remove it 
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

        return requirements

setup(
name = 'ml_app',
version='0.0.1',
author ='Andy',
author_email='drewm8080@gmail.com',
packages=find_packages(),
install_requires =get_requirements('requirements.txt')
)
from setuptools import find_packages,setup
from typing import List

HYPER_E_DOT = "-e ."
#If you omit the -> List[str] part, Python will still execute the code without any issues 
# because type hints are not required for the code to run.
def get_requirements(file_paht:str)->List[str]:
    """ 
        This function will return the list of requirements in requirements.txt file
    """
    requirements=[]
    with open(file_paht) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","")for req in requirements]

        if HYPER_E_DOT in requirements:
            requirements.remove(HYPER_E_DOT)
    
    return requirements

setup(
    name="mlproject",
    version="0.0.1",
    author="Chamika",
    author_email="edcdanuruddha@gmail.com",
    packages=find_packages(),
    install_requires= get_requirements("requirements.txt")
)
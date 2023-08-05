# -*- coding: utf-8 -*-
"""
@author: djclavero@yahoo.com

setup.py must be in the root of the project
"""

from setuptools import setup

setup(
      name=     'template_python_projects',
      version=  '1.3', 
      
      # find_packages() can be imported and used here
      packages= ['sound', 'sound.effects', 'sound.formats', 'sound.filters'],
      
      scripts= ['bin/testing_sound.py'],
      
      author= 'djclavero',
      author_email= 'djclavero@yahoo.com',
      
      license= 'MIT',
      long_description= open('README.md').read(),
      
      keywords = ['projects', 'test'],
      
      url= 'https://pypi.org/project/template_python_projects',
      
      description= 'Template Project in Python',
      
      # Dependences
      install_requires= ['', ''],
      
)


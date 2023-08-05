# -*- coding: utf-8 -*-
"""
@author: djclavero@yahoo.com

Python Module
"""

# Projects: contain setup.py and packages 
# Packages: contain __init__.py and modules (.py files)

# Define a function
def test_waveread():
    print('Just answering your call to test_waveread function')
    

# Define a variable
EXTENSION = 'wav'


# Define a class
class WaveFile:
    def __init__(self, name, sample_rate):
        self.sample_rate = sample_rate
        self.name = name

    def wavefile_info(self):
        print("Wave file name is " + self.name)
        print(self.name + " sample rate is " + str(self.sample_rate))
        



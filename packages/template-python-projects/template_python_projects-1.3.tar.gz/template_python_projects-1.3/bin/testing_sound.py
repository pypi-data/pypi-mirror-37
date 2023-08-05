# -*- coding: utf-8 -*-
"""
@author: djclavero@yahoo.com

Script for testing 'sound' package
"""

# Projects: contain setup.py and packages 
# Packages: contain __init__.py and modules (.py files)

from sound.formats import waveread

# Call function
waveread.test_waveread()

# Call variable
print('EXTENSION is ' + waveread.EXTENSION)

# Create object
soundfile = waveread.WaveFile('violin', 44100)
soundfile.wavefile_info()





"""
Example of section endpoints
definition, loading and saving
"""

import pypago.pyio
import pypago.sections

# initialisation list of sections
listofsec = []

# creation a new section
name = 'mysection'
lon = [-70., -43.5]
lat = [54.5, 68.]
dire = ['NW']
section = pypago.sections.Section(name, lon, lat, dire)
print(section)

# adding the section to the list
listofsec.append(section)

# saving the list of section into a file
pypago.pyio.save(listofsec, 'data/sample_section.pygo')

# loading the previously saved file
listofsec = pypago.pyio.load('data/sample_section.pygo')
print(listofsec[0])

# Charlie Hanner - 2022
# This code is for Wilcat Mountain in the White Mountains of New Hampshire
# and will attempt to create a trail map for the mountain with color coding 
# for the present open/closed status of trails and lifts.

# Import the necessary modules
import os
import requests
import pandas as pd
from PIL import Image

# Get current working directory
cwd = os.getcwd()
assets = cwd + '/MountainTrails/Wildcat_Assets/'
maps = cwd + '/MountainTrails/Daily_Trail_Maps/'

# Create classes for lift and trail statuses
class LiftStatus:
    def __init__(self, name, status):
        self.name = name # Name of lift
        self.status = status # Open, Closed, On Hold, or Scheduled

class TrailStatus:
    def __init__(self, ID, name, status, groomed):
        self.ID = ID # ID of trail
        self.name = name # Name of trail
        self.status = status # Open, or Closed
        self.groomed = groomed # Booleon

URL = "https://www.skiwildcat.com/the-mountain/mountain-conditions/lift-and-terrain-status.aspx"
page = requests.get(URL)
# Separate lines in page by /n
page = page.text.split('\n')

# Iterate through page and find if any line has FR.TerrainStatusFeed in it and save the line
for line in page:
    if 'FR.TerrainStatusFeed' in line:
        terrain = line

# Remove FR.TerrainStatusFeed = from the line
terrain = terrain.replace('FR.TerrainStatusFeed = ', '')
# Remove leading spaces
terrain = terrain.lstrip()

# Pull the date from the first few lines of terrain
date = terrain.find('"Date":')
# Find the next comma
comma = terrain.find(',', date)
# Pull the date
date = terrain[date+8:comma-1]

# Find the index for "GroomingAreas"
grooming = terrain.find('"Trails":')
# Remove everything before "GroomingAreas"
terrain = terrain[grooming+9:]

# Find the index for "Lifts"
lifts_id = terrain.find('"Lifts":')
# Put everything after lifts into own string
lifts = terrain[lifts_id+8:]
# Remove everything after lifts
terrain = terrain[:lifts_id-2]

# Remove evrything after the last ] in lifts
lifts = lifts[:lifts.rfind(']')+1]

# Add ] at end of terrain
terrain = terrain + ']'

# Remove the repeated "Lifts" in lifts and all data after
repet = lifts.find('"Lifts":')
lifts = lifts[:repet-3]

# Convert terrain and lifts to json
terrain = pd.read_json(terrain)
lifts = pd.read_json(lifts)

# Remove TrailType and IsTrailWork from terrain pd
terrain = terrain.drop(['TrailType', 'IsTrailWork', 'TrailInfo', 'TrailLength'], axis=1)

# Remove  Type, WaitTimeInMinutes, Capacity, SortOrder, Mountain from lifts pd
lifts = lifts.drop(['Type', 'WaitTimeInMinutes', 'Capacity', 'SortOrder', 'Mountain'], axis=1)

# Do replacement on the pd frames for being able to pull the png files
terrain['Name'] = terrain['Name'].str.replace(' ', '_')
terrain['Name'] = terrain['Name'].str.replace("'", '')
terrain['Name'] = terrain['Name'].str.replace('&', 'n')

# Adjust the names of the lifts to match the png files
lifts['Name'] = lifts['Name'].str.replace(' ', '_')
lifts['Name'] = lifts['Name'].str.replace("Snowcat", 'Snowcat_Triple')
lifts['Name'] = lifts['Name'].str.replace("Bobcat", 'Bobcat_Triple')
lifts['Name'] = lifts['Name'].str.replace("Tomcat", 'Tomcat_Triple')

# Iterate through the terrain pd and stack images on top of each other to create the map
# If the terrain is open use the original image
# If the terrain is closed, make the image gray and change opacity

# Begin with the base map
background = Image.open(assets + 'Wildcat_Base_WhiteBackground.png')

for index, row in terrain.iterrows():
    # Get the name of the trail
    name = row['Name']
    # Get the status of the trail
    status = row['IsOpen']
    # Get the groomed status of the trail
    groomed = row['IsGroomed']
    # Get the image of the trail
    img = Image.open(assets + name + '.png')

    # If the trail is closed, make the image gray and change opacity
    if status == False:
        # img = img.convert('LA')
        img = img.point(lambda x: x*0.125)

    # Stack the image on top of the base map
    background.paste(img, (0, 0), img)

# Iterate through the lifts pd and stack images on top of each other to create the map
# If the lift is open use the original image
# If the lift is closed, make the image gray and change opacity

for index, row in lifts.iterrows():
    # Get the name of the lift
    name = row['Name']
    # Get the status of the lift
    status = row['Status']
    # Get the image of the lift
    img = Image.open(assets + name + '.png')

    # If the lift is closed, make the image gray and change opacity
    if status == "Closed":
        # img = img.convert('LA')
        img = img.point(lambda x: x*0.125)

    # Stack the image on top of the base map
    background.paste(img, (0, 0), img)

background.show()
# Create a saved name for the image
# Change the name to not have - and to have _ instead
date = date.replace('-', '_')
date = date.replace('/', '_')
date = date.replace(':', '_')
date = date.replace('.', '_')

name = 'Wildcat_' + date
# Save the image
background.save(maps + name + '.png')
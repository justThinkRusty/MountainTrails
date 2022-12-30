# This file will open the readme, and adjust the photo link to the most recent files in the Daily_Trail_Maps folder
# It will also adjust some text to state the current date of the trail map

import os

# Get current working directory
cwd = os.getcwd()
cwd = cwd + '/MountainTrails/'
Maps = cwd + 'Daily_Trail_Maps/'

# Find all files that end with ".png"
file_list = [f for f in os.listdir(Maps) if f.endswith(".png")]

# Sort the list of files by the date of creation
file_list.sort(key=lambda x: os.path.getmtime(os.path.join(Maps, x)))

# Get the most recent file
most_recent_file = file_list[-1]

# Get the date of the most recent file
# Find the first underscore
first_underscore = most_recent_file.find('_')
# Find the second underscore
second_underscore = most_recent_file.find('_', first_underscore + 1)
# Find the third underscore
third_underscore = most_recent_file.find('_', second_underscore + 1)

Year = most_recent_file[first_underscore + 1:second_underscore]
Month = most_recent_file[second_underscore + 1:third_underscore]
Day = most_recent_file[third_underscore + 1:len(most_recent_file) - 4]

# Now open the readme file and adjust the most recent date
with open(cwd + "README.md", "r") as f:
    lines = f.readlines()

# Find the line that contains the most recent date
for i in range(len(lines)):
    if lines[i].startswith("![Generated Image](Daily_Trail_Maps/"):
        lines[i-1] = "Example snow report for " + Month + "/" + Day + "/" + Year + "! (May take a moment to load in the browser) \n"
        lines[i] = "![Generated Image](Daily_Trail_Maps/Wildcat_" + Year + "_" + Month + "_" + Day + ".png) \n " 

# Now write the new lines to the readme file
with open(cwd + "README.md", "w") as f:
    f.writelines(lines)

# Now move all older files to the Old folder
Old = Maps + 'Old/'
if not os.path.exists(Old):
    os.makedirs(Old)

for i in range(len(file_list) - 1):
    os.rename(Maps + file_list[i], Old + file_list[i])




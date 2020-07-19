# ----------------------------------------------------------------------------------------------------------------------
'''
author:翁玮熙
create time：2020-7-13
update time:2020-7-18
'''
import os

# ----------------------------------------------------------------------------------------------------------------------

files = os.listdir('./annotations/')
files.sort()

for file in files:
    if file.endswith('xml'):
        output = open("./names.txt", "a")
        output.write('./images/' + file.split('.')[0] + '.jpg')
        output.write("\n")
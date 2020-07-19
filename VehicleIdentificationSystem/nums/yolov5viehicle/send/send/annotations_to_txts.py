# ----------------------------------------------------------------------------------------------------------------------
# 将xml文件转成符合要求的txt文件
# ----------------------------------------------------------------------------------------------------------------------
'''
author:翁玮熙
create time：2020-7-13
update time:2020-7-18
'''
import xml.etree.ElementTree as ET
import os
import cv2

# ----------------------------------------------------------------------------------------------------------------------

l = os.listdir("./annotations/")
l.sort()
out = []
for i in range(0, len(l)):
    if l[i].endswith("xml"):
        out.append(l[i])

# ----------------------------------------------------------------------------------------------------------------------

for j in range(0, len(out)):
    root = ET.parse("./annotations/" + out[j]).getroot()
    object_num = len(root.getchildren())
    name = out[j].split(".")[0]
    output = open("./txts/" + name + ".txt", "a")

    image = cv2.imread("./images/" + name + ".jpg")
    (H, W) = image.shape[:2]
    print(H, W)

    count_1 = 0
    for k in range(0, object_num - 5):
        children_node = root.getchildren()[5 + k]

        length = len(list(children_node))
        print(length)
        location = []
        for i in range(0, length):
            if i == 0:
                CLASS = list(children_node)[i].text.strip()

            if i == 4:
                for item in list(children_node)[i]:
                    location.append(item.text.strip())

                label = ''
                if CLASS == "heavy truck":
                    label = "0"

                elif CLASS == "bus":
                    label = "1"

                elif CLASS == "racing car":
                    label = "2"

                elif CLASS == "SUV":
                    label = "3"

                elif CLASS == "minibus":
                    label = "4"

                elif CLASS == "fire engine":
                    label = "5"

                elif CLASS == "jeep":
                    label = "6"

                elif CLASS == "truck":
                    label = "7"

                elif CLASS == "family sedan":
                    label = "8"

                elif CLASS == "taxi":
                    label = "9"

                elif CLASS == "motor":
                    label = "10"

                elif CLASS == "tricycle":
                    label = "11"

                num_1 = int(location[0]) / W
                num_2 = int(location[1]) / H
                num_3 = int(location[2]) / W
                num_4 = int(location[3]) / H

                center_x = num_1 + ((num_3 - num_1) / 2.0)
                center_y = num_2 + ((num_4 - num_2) / 2.0)

                print(int(location[0]) / W)

                output.write(label + " "
                             + str(center_x) + " "
                             + str(center_y) + " "
                             + str(num_3 - num_1) + " "
                             + str(num_4 - num_2) + "\n")


# ----------------------------------------------------------------------------------------------------------------------





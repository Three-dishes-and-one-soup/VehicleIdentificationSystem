import cv2
import os

# ----------------------------------------------------------------------------------------------------------------------

writer = None
files = os.listdir('./data/dataset/images/')
count = 0
for file in files:
    image_path = './data/dataset/images/' + str(file)
    print(image_path)
    image = cv2.imread(image_path)
    image = cv2.resize(image, (720, 480))

    if writer is None:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter("./out/out.mp4", fourcc, 20,
                                 (image.shape[1], image.shape[0]), True)

    writer.write(image)

    cv2.imshow('', image)
    if count < 10:
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break
    else:
        if cv2.waitKey(500) & 0xFF == ord('q'):
            break

    count += 1

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------

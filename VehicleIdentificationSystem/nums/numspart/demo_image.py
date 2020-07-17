# ----------------------------------------------------------------------------------------------------------------------
# 检测图片
# ----------------------------------------------------------------------------------------------------------------------

from utils.datasets import *
from utils.utils import *
import argparse
import cv2
import os

# ----------------------------------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument('--weights', type=str, default='weights/best.pt', help='path to weights file')
parser.add_argument('--conf-thres', type=float, default=0.3, help='object confidence threshold')
parser.add_argument('--nms-thres', type=float, default=0.5, help='iou threshold for non-maximum suppression')
opt = parser.parse_args()
print(opt)


# ----------------------------------------------------------------------------------------------------------------------


class Yolo():
    def __init__(self):
        self.writer = None
        self.prepare()

    def prepare(self):
        global model, device, classes, colors, names
        device = torch_utils.select_device(device='cpu')

        google_utils.attempt_download(opt.weights)
        model = torch.load(opt.weights, map_location=device)['model'].float()

        model.to(device).eval()

        names = model.names if hasattr(model, 'names') else model.modules.names
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]

    def apiDetect(self, frame):
        im0 = imutils.resize(frame, width=720)
        img = letterbox(frame, new_shape=416)[0]

        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img, dtype=np.float32)
        img /= 255.0

        img = torch.from_numpy(img).to(device)
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        pred = model(img)[0]
        #print(pred)
        pred = non_max_suppression(pred, opt.conf_thres, opt.nms_thres)

        boxes = []
        confidences = []
        classIDs = []
        requestData = {}

        for i, det in enumerate(pred):

            if det is not None and len(det):
                #print((len(det)))
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                i=1;

                for *xyxy, score, cls in det:
                    requestData[str(i)]={"type":(names[int(cls)]), "position": {}, "probability":str(float(score))}
                    requestData[str(i)]["position"]={"width":int(xyxy[0]),"top":int(xyxy[1]),"left": int(xyxy[2] - xyxy[0]),"height":int(xyxy[3] - xyxy[1])}
                    i=i+1

            return requestData

    def onlineDetect(self, frame):
        im0 = imutils.resize(frame, width=720)
        img = letterbox(frame, new_shape=416)[0]

        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img, dtype=np.float32)
        img /= 255.0

        img = torch.from_numpy(img).to(device)
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        pred = model(img)[0]
        #print(pred)
        pred = non_max_suppression(pred, opt.conf_thres, opt.nms_thres)

        boxes = []
        confidences = []
        classIDs = []
        requestData = {}

        for i, det in enumerate(pred):

            if det is not None and len(det):
                #print((len(det)))
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                i=1;

                for *xyxy, score, cls in det:

                    label = '%s ' % (names[int(cls)]) + ':' + str(float(score))[:5]
                    plot_one_box(xyxy, im0, label=label, color=colors[int(cls)])

                    # ----------------------------------------------------------------------------------------------------------------------

                    boxes.append([int(xyxy[0]), int(xyxy[1]), int(xyxy[2] - xyxy[0]), int(xyxy[3] - xyxy[1])])
                    confidences.append(float(score))
                    classIDs.append(int(cls))

            return im0


# ----------------------------------------------------------------------------------------------------------------------
#测试函数
def test():
    yolo = Yolo()
    files = os.listdir('./inference/images/')
    files.sort()

    for file in files:
        if file.endswith('jpg') or file.endswith('png'):
            image_path = './inference/images/' + file
            #print(image_path)
            image = cv2.imread(image_path)
            image = yolo.onlineDetect(image)
            cv2.imshow('', image)
            cv2.waitKey(0)

# ----------------------------------------------------------------------------------------------------------------------
#api调用使用的函数
def apiRequest(image_path):
    yolo = Yolo()
    image = cv2.imread(image_path)
    requestData = yolo.apiDetect(image)
    return requestData;

#在线识别调用的函数
def onlineRequest(image_path):
    yolo = Yolo()
    image = cv2.imread(image_path)
    image = yolo.onlineDetect(image)
    return image
    #cv2.imshow('', image)
    #cv2.waitKey(0)

test()
#onlineRequest(image_path)
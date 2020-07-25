'''
author: 周行健
create time: 2020/7/21
update time: 2020/7/23
'''


import argparse
import os
import random
import shutil
import time
import warnings
from PIL import Image

import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
import torch.utils.data.distributed
import torchvision.transforms as transforms
from efficientnet_pytorch import EfficientNet
from scipy import io as mat_io


car_mat_file = "carmodels/CarInfoTeller/dataprocessing/datasets/cars_metas/cars_meta"
labels_meta = mat_io.loadmat(car_mat_file)
labels_map = [name[0] for name in labels_meta['class_names'][0]]
device = torch.device('cpu')
        # #.attempt_download('nweights/best.pt')
        # model = torch.load('nums/numspart/weights/best.pt', map_location=torch.device('cpu'))['model'].float()
use_gpu = torch.cuda.is_available()

resume_file = "carmodels/CarInfoTeller/checkpoints/model_best.pth.tar"
num_classes = len(labels_map)

model_name = 'efficientnet-b4'
batch_size = 2
num_wokers = 4
lr = 0.1
weight_decay = 1e-4
momentum = 0.9
device = ('cuda' if torch.cuda.is_available() else 'cpu')

def tell(img):
    img = Image.open(img)
        # 创建网络模型
    model = EfficientNet.from_pretrained(model_name, num_classes=num_classes)
    if use_gpu:
        model.cuda()

    # 损失函数和优化器
    criterion = nn.CrossEntropyLoss().cuda()
    optimizer = torch.optim.SGD(model.parameters(), lr,
                                momentum=momentum,
                                weight_decay=weight_decay)

    # 是加载已有的模型
    checkpoint = torch.load(resume_file,map_location='cpu')
    model.load_state_dict(checkpoint['state_dict'])
    cudnn.benchmark = True

    image_size = EfficientNet.get_image_size(model_name)
    tfms = transforms.Compose([
                transforms.Resize(image_size, interpolation=Image.BICUBIC),
                transforms.CenterCrop(image_size),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])
    img = tfms(img).unsqueeze(0)

    # 训练得到结果

    # switch to train mode
    model.train()

    with torch.no_grad():
        logits = model(img.to(device))
    preds = torch.topk(logits, k=5)[1].squeeze(0).tolist()

    # for idx in preds:
    #     label = labels_map[idx]
    #     prob = torch.softmax(logits, dim=1)[0, idx].item()
    #     print('{:<75} ({:.2f}%)'.format(label, prob * 100))
    label0 = labels_map[0]
    prob0 = torch.softmax(logits, dim=1)[0, 0].item()
    label1 = labels_map[1]
    prob1 = torch.softmax(logits, dim=1)[0, 1].item()
    label2 = labels_map[2]
    prob2 = torch.softmax(logits, dim=1)[0, 2].item()
    label3 = labels_map[3]
    prob3 = torch.softmax(logits, dim=1)[0, 3].item()
    label4 = labels_map[4]
    prob4 = torch.softmax(logits, dim=1)[0, 4].item()
    result = {
        '1': {'label': label0, 'prob': prob0*100},
        '2': {'label': label1, 'prob': prob1*100},
        '3': {'label': label2, 'prob': prob2*100},
        '4': {'label': label3, 'prob': prob3*100},
        '5': {'label': label4, 'prob': prob4*100},
    }
    return result



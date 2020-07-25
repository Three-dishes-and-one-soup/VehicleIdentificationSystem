'''
author: 郑志强
create time: 2020/7/22
update time: 2020/7/22
'''
from io import BytesIO

import requests
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from ..demo.demo_behavior import apiRequest
import time
import os

def tran_name(image):
    curr_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    suffix = image.name.split('.')[-1]
    image.name = curr_time + '.' + suffix

def save_image(image):
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media')
    full_path = image_path + '/' + image.name
    with open(full_path, 'wb') as f:
        for c in image.chunks():
            f.write(c)
    return full_path

@csrf_exempt
@api_view(['POST'])
def get_license_result(request):
    response = {}
    try:
        if (request.data['path']):
            url = request.data['path']
            session = requests.session()
            pic = session.get(url)
            f = BytesIO()
            f.write(pic.content)
            curr_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
            suffix = url.split('.')[-1]
            image_name = curr_time + '.' + suffix
            image = InMemoryUploadedFile(f, None, image_name, None, len(pic.content), None, None)
        else:
            image = request.data['image']
            tran_name(image)
        full_path = save_image(image)
        result = apiRequest(full_path)
        response['msg'] = result
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return Response(response)
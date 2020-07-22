'''
author: 郑志强
create time: 2020/7/15
update time: 2020/7/19
'''
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
import time
import os
from ..License_plate.final_solution import get_result

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
        image = request.data['image']
        tran_name(image)
        full_path = save_image(image)
        #result = get_result(full_path)
        result = {
            'pro': {
                'first': {'result': '闽', 'probability': 0.8774},
                'second': {'result': '苏', 'probability': 0.0343},
                'third': {'result': '浙', 'probability': 0.0068}},
            'let': {
                'first': {'result': 'O', 'probability': 1},
                'second': {'result': 'Y', 'probability': 0},
                'third': {'result': 'K', 'probability': 0}},
            'dig': {
                'first': {'result': '1', 'probability': 1},
                'second': {'result': 'W', 'probability': 0.9999},
                'third': {'result': 'Y', 'probability': 0.9963},
                'forth': {'result': 'A', 'probability': 0.9999},
                'fifth': {'result': 'A', 'probability': 0.9971}}
        }
        response['msg'] = result
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return Response(response)
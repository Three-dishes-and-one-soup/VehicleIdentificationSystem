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
    return full_path.replace('\\', '/')

@csrf_exempt
@api_view(['POST'])
def get_license_result(request):
    response = {}
    try:
        image = request.data['image']
        tran_name(image)
        full_path = save_image(image)
        result = get_result(full_path)
        response['msg'] = result
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return Response(response)
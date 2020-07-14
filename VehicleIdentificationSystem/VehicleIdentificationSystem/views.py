'''
author: 郑志强
create time: 2020/7/10
update time: 2020/7/12
'''
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from license_identification import img_pretreatment
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import requests
import time


def index(request):
    return render(request, 'MainPage.html')


def download_packages(request):
    return HttpResponse("还未完成！")

def download_doc(request):
    return HttpResponse("还未完成！")

def get_picture(request):
    if request.POST:
        pic_url = request.POST.get('pic-url')
        curr_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        if pic_url:
            suffix = pic_url.split('.')[-1]
            pic_name = curr_time + '.' + suffix
            session = requests.session()
            response = session.get(pic_url)
            pic_data = response.content
            f = BytesIO()
            f.write(pic_data)
            pic = InMemoryUploadedFile(f, None, pic_name, None, len(pic_data), None, None)
        else:
            pic = request.FILES.get('picture')
            suffix = pic.name.split('.')[-1]
            pic.name = curr_time + '.' + suffix
        return pic
    else:
        return None

def save_pic(pic):
    pic_path = settings.MEDIA_ROOT
    full_path = pic_path + '/' + pic.name
    with open(full_path, 'wb') as f:
        for c in pic.chunks():
            f.write(c)
    return full_path

def online_identification_model(request):
    ctx = {}
    ctx['path'] = 0
    if request.POST:
        pic = get_picture(request)
        full_path = save_pic(pic)
        ctx['path'] = pic.name
    return render(request, 'FunctionPage.html', ctx)


def online_identification_license(request):
    ctx = {}
    ctx['path'] = 0
    if request.POST:
        pic = get_picture(request)
        full_path = save_pic(pic)
        ctx['path'] = pic.name
    return render(request, 'license.html', ctx)


def online_identification_nums(request):
    ctx = {}
    ctx['path'] = 0
    if request.POST:
        pic = get_picture(request)
        full_path = save_pic(pic)
        ctx['path'] = pic.name
    return render(request, 'nums.html', ctx)


def online_identification_attributes(request):
    ctx = {}
    ctx['path'] = 0
    if request.POST:
        pic = get_picture(request)
        full_path = save_pic(pic)
        ctx['path'] = pic.name
    return render(request, 'attributes.html', ctx)


def online_identification_destroy(request):
    ctx = {}
    ctx['path'] = 0
    if request.POST:
        pic = get_picture(request)
        full_path = save_pic(pic)
        ctx['path'] = pic.name
    return render(request, 'destroy.html', ctx)


def online_identification_drive(request):
    ctx = {}
    ctx['path'] = 0
    if request.POST:
        pic = get_picture(request)
        full_path = save_pic(pic)
        ctx['path'] = pic.name
    return render(request, 'drive.html', ctx)


def model_download_packages(request):
    return HttpResponse("还未完成！")


def model_download_doc(request):
    return HttpResponse("还未完成！")


def license_download_packages(request):
    return HttpResponse("还未完成！")


def license_download_doc(request):
    return HttpResponse("还未完成！")


def nums_download_packages(request):
    return HttpResponse("还未完成！")


def nums_download_doc(request):
    return HttpResponse("还未完成！")


def drive_download_packages(request):
    return HttpResponse("还未完成！")


def drive_download_doc(request):
    return HttpResponse("还未完成！")


def destroy_download_packages(request):
    return HttpResponse("还未完成！")


def destroy_download_doc(request):
    return HttpResponse("还未完成！")


def attributes_download_packages(request):
    return HttpResponse("还未完成！")


def attributes_download_doc(request):
    return HttpResponse("还未完成！")
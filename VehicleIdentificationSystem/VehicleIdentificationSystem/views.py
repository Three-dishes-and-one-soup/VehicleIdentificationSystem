from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

def index(request):
    return render(request, 'MainPage.html')

def online_identification(request):
    return render(request, 'FunctionPage.html')

def download_packages(request):
    return HttpResponse("还未完成！")

def download_doc(request):
    return HttpResponse("还未完成！")


def online_identification_model(request):
    ctx = {}
    ctx['path'] = 0
    if request.POST:
        pic = request.FILES.get('picture')
        pic_path = settings.MEDIA_ROOT
        allow_upload = settings.ALLOW_UPLOAD
        if pic.name.split('.')[-1] not in allow_upload:
            tmp=''
        # ctx['warn'] = "请输入正确的图片格式！"
        with open(pic_path+'/'+pic.name, 'wb') as f:
            for c in pic.chunks():
                f.write(c)
        ctx['path'] = pic.name
    return render(request, 'FunctionPage.html', ctx)


def online_identification_license(request):
    return None


def online_identification_nums(request):
    return None


def online_identification_attributes(request):
    return None


def online_identification_destroy(request):
    return None


def online_identification_drive(request):
    return None
from django.shortcuts import render
from .forms import QrcodeForm
from django.conf import settings
from django.http import HttpResponse
from django.core.files.storage import default_storage
from .pdf_generator_function import image_adder

def index(request):
    if request.method == 'POST':  
        qrcodevalues = QrcodeForm(request.POST, request.FILES)  
        if qrcodevalues.is_valid():  
            files = request.FILES.getlist('file')

            page_dimension = (float(request.POST.get('page_size_x')), float(request.POST.get('page_size_y')))

            frame_dimension = (float(request.POST.get('frame_size_x')), float(request.POST.get('frame_size_y')))

            padding_btw_frames = (float(request.POST.get('padding_btw_frames_x')), float(request.POST.get('padding_btw_frames_y')))

            image_resize = (float(request.POST.get('image_size_x')), float(request.POST.get('image_size_y')))
            
            # print("circle_required: ", request.POST.get('circle_required'))

            circle_required = (lambda x: x == 'on')(request.POST.get('circle_required'))

            repetition = int(request.POST.get('repetition'))

            print("page dimension: ", page_dimension)
            print("padding: ", padding_btw_frames)
            for f in files:
                default_storage.save(None, f)
            image_adder(page_dimension =  page_dimension, frame_dimension = frame_dimension, image_resize= image_resize, padding_btw_frames=padding_btw_frames, circle_required= circle_required, repetition=repetition)
            
            # print(request.FILES['file'])
            # default_storage.save(None, file)  
            return HttpResponse("File uploaded successfuly")
    else:
        qrcodevalues = QrcodeForm()
    return render(request,"index.html",{'form':qrcodevalues})  
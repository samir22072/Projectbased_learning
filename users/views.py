from typing import Sized
from django.shortcuts import render,redirect
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm,ScanningForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .utils import get_shoulder_width
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import cv2
import random 
import numpy as np
import urllib
import hashlib

import base64
links_dict = {"small":'https://www.amazon.in/s?k=shirts&i=apparel&bbn=1968094031&rh=n%3A1968094031%2Cp_n_size_browse-vebin%3A1975393031&dc&qid=1626586577&rnid=1974882031&ref=sr_nr_p_n_size_browse-vebin_7','medium':'https://www.amazon.in/s?k=shirts&i=apparel&bbn=1968094031&rh=n%3A1968094031%2Cp_n_size_browse-vebin%3A1975394031&dc&qid=1623333628&rnid=1974882031&ref=sr_nr_p_n_size_browse-vebin_7','large':'https://www.amazon.in/s?k=shirts&i=apparel&bbn=1968094031&rh=n%3A1968094031%2Cp_n_size_browse-vebin%3A1975395031&dc&qid=1623333726&rnid=1974882031&ref=sr_nr_p_n_size_browse-vebin_7','xlarge':'https://www.amazon.in/s?k=shirts&rh=n%3A1968094031%2Cp_n_size_browse-vebin%3A1975396031&dc&qid=1626510186&rnid=1974882031&ref=sr_nr_p_n_size_browse-vebin_9','xxlarge':'https://www.amazon.in/s?k=shirts&i=apparel&bbn=1968094031&rh=n%3A1968094031%2Cp_n_size_browse-vebin%3A1975395031%7C1975397031&dc&qid=1626510314&rnid=1974882031&ref=sr_nr_p_n_size_browse-vebin_10','sizenotfound':'/camtest'}

def register(request):#registration page
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account has been created for {username}')
            return redirect('login')
    else:
        form=UserRegisterForm()
    return render(request,'users/registration.html',{'form':form})





def home(request):#homepage
    return render(request,'users/index.html')


@login_required

def profile(request):#profile page
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

def scan(request):
    if request.method=='POST':
        
        s_form=ScanningForm(request.POST,request.FILES,instance=request.user.profile)
        

        if s_form.is_valid:
            s_form.save()
            messages.success(request,f'Your Scanning is complete')
            return redirect('Scanpage')
    else:
        s_form=ScanningForm()

    context={
        's_form':s_form
    }
    return render(request,'users/instructions.html',context)


    
    #Running the OpenCv code
    #global size
    #size = get_shoulder_width(image_path,287)

    
    

    
def show_shoulder_width():
    """Reconstructing the image path"""
    try:
        from users.models import x
    except:
        return HttpResponse("No image uploaded yet")
   
    image_string = str(x)

    image_path = os.path.join(r'C:\Users\samir\pbl\media\images',image_string)

    
    #Running the OpenCv code
    global size
    size = get_shoulder_width(image_path,287)
    # image = cv2.imread(image_path)
    
    with open(image_path, "rb") as image2string:
        global b
        a = base64.b64encode(image2string.read())
        z = str(a,'UTF-8')
        b = f'data:image/png;base64,{z}'       
    
   

#Thank you page takes multi input from image upload as well as webcam

def save_image(request):
    """This function is here just for the namesake of it. Don't touch it..it makes other stuff work :) """
  

@csrf_exempt
def site_load(request):
    if  request.POST:
        a = request.body
        global b 
        b = str(a,'UTF-8')
        url_to_image(b)
    return render(request,"users/scanning.html")


def url_to_image(url):
    """Function to convert the recieved url string from frontend into an actual image and store it in the media files"""
   
    
    x= hashlib.sha256(("".join(map(str,[random.randint(0,9) for i in range(10)]))).encode('utf-8')).hexdigest()[0:52]
    x_butcooler = f'{x}.jpeg'
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    global store
    store = image
    global img_path
    img_path = os.path.join(r'C:\Users\samir\pbl\media\images',x_butcooler)
    
    cv2.imwrite(img_path,image)
    global size
   
    size = get_shoulder_width(img_path,287)


def typage(request):
   
    return render(request,'users/endpage.html',{'size':size,'image_path':b})
 

def ty_redirect(request):
    """Function to do the final redirect """
    
    redirect_link = links_dict[size]
    return HttpResponseRedirect(redirect_link)




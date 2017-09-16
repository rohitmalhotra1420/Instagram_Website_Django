# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.shortcuts import HttpResponseRedirect
from django.core.mail import send_mail
from forms import SignUpForm
from forms import LoginForm
from forms import PostForm
from forms import LikeForm,CommentForm,OtpForm
from models import UserModel
from models import PostModel
from models import LikeModel,CommentModel
from models import SessionToken
from imgurpython import ImgurClient
from django.http import HttpResponse
from Instagram.settings import BASE_DIR
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from twilio.rest import Client
import pyotp
import sendgrid
import os
from sendgrid.helpers.mail import *



TWILIO_ACCOUNT_SID = 'AC10f5e164b1e86db138c25be3019ee199'
TWILIO_AUTH_TOKEN = '61816dc5a5701775b63caf590adb8756'
num=7607904382
my_twilio="+1"+str(num)
#totp = pyotp.TOTP('JBSWY3DPEHPK3PXP')
#pin=totp.now()


# Create your views here.

def signup_view(request):
    if request.method == "POST":
        form= SignUpForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            name=form.cleaned_data['name']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            # saving data to DB
            user = UserModel(name=name, password=make_password(password), email=email, username=username)
            user.is_active=False
            user.save()
            send_mail('E-Mail Verification',
                      ' HEY...Welcome To Instagram.'
                      '.click on the link below to get your account activated \n\n '
                      'http://127.0.0.1:8000/email_activate/?user_email=' + email
                      ,
                      'rohit.malhotra1420@gmail.com',
                      [email],
                      fail_silently=False)

            return render(request, 'success.html')
        else:
            return HttpResponse("Invalid form data.")
    else:
        form = SignUpForm()
        return render(request, 'index.html', {'form' : form})

def email_activate(request):
    email=request.GET.get('user_email')
    user_email_all=UserModel.objects.filter(email=email).all()
    user_email_reqd=user_email_all.first()
    if user_email_all:
        if user_email_reqd.is_active == False:
            user_email_reqd.is_active = True
            user_email_reqd.save()
            return HttpResponseRedirect('/otp_verification/')
        else:
            print ' user has been already activated'
            print user_email_reqd.is_active
            return HttpResponseRedirect('/login/')
    else:
        print "No objects returned"

def otp_send(request):
    if request.method=="POST":
        form=OtpForm(request.POST)
        if form.is_valid():
            number=form.cleaned_data['number']
            user_number="+91"+str(number)
            # saving data to DB
            user = UserModel(number=number)
            user.save()

            totp = pyotp.TOTP('JBSWY3DPEHPK3PXP')
            pin=totp.now()
            global pin

            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            client.messages.create(to=user_number, from_=my_twilio,body=pin)

            return HttpResponseRedirect('/otp_receive/')
        else:
            return HttpResponse("Invalid Number.")
    elif request.method=="GET":
        form = OtpForm()
        return render(request, 'otp.html', {'form' : form})

def otp_receive(request):
    if request.method == "POST":
        otp_number=request.POST['otp_number']
        if otp_number==pin:
            return HttpResponseRedirect('/feed/')
        else:
            return HttpResponseRedirect('/otp_verification/')

    elif request.method == "GET":
        return render(request, 'enter_otp.html')




def login_view(request):
    response_data = {}
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = UserModel.objects.filter(username=username).first()

            if user:
                if user.is_active==True:
                    print user.is_active
                    if check_password(password, user.password):
                        token = SessionToken(user=user)
                        token.create_token()
                        token.save()
                        response = HttpResponseRedirect('/feed/')
                        response.set_cookie(key='session_token', value=token.session_token)
                        print "success"
                        return response

                    else:
                        response_data['message'] = 'Incorrect Password! Please try again!'
                else:
                    print 'user has not been activated'
                    return HttpResponse('You Must activate first.')



    elif request.method=="GET":
        form = LoginForm()
        response_data['form'] = form
    return render(request, 'login.html', response_data)



def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
           return session.user
    else:
        return None

def post_view(request):
    user=check_validation(request)
    if user:
        if request.method=="GET":
            form = PostForm()
            return render(request, 'posts.html', {'form': form})
        elif request.method=="POST":
            form=PostForm(request.POST,request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')

                post = PostModel(user=user, image=image, caption=caption)
                post.save()
                path=str(BASE_DIR +'/'+ post.image.url)
                client=ImgurClient("7c523b250772ade","5307069c8ab8398c385cfbeacd51857ed22")
                post.image_url = client.upload_from_path(path, anon=True)['link']
                post.save()

        else:
            return redirect('/login/')
    return redirect('/feed/')

def feed_view(request):
      user = check_validation(request)
      if user:
        posts = PostModel.objects.all().order_by('-created_on')
        for post in posts:
            existing_like=LikeModel.objects.filter(post_id=post.id,user=user).first()
            if existing_like:
                post.has_liked=True
        return render(request, 'feeds.html', {'posts' : posts})
      else:
        return redirect('/login/')


def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id

            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()

            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()

            return redirect('/feed/')

    else:
        return redirect('/login/')


def comment_view(request):
  user = check_validation(request)
  if user and request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
      post_id = form.cleaned_data.get('post').id
      comment_text = form.cleaned_data.get('comment_text')
      comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
      comment.save()
      return redirect('/feed/')
    else:
      return redirect('/feed/')
  else:
    return redirect('/login')


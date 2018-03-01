# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse
from django.core.mail import send_mail
from forms import SignUpForm
from forms import LoginForm
from forms import PostForm
from forms import LikeForm,CommentForm,OtpForm,ProfilePicForm
from models import UserModel
from models import PostModel
from models import LikeModel,CommentModel,ProfilePicModel
from models import SessionToken
from imgurpython import ImgurClient
from django.http import HttpResponse
from Instagram.settings import BASE_DIR
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from twilio.rest import Client
import pyotp
from django.db.models import Q
import os

from django.core import serializers
TWILIO_ACCOUNT_SID = 'AC10f5e164b1e86db138c25be3019ee199'
TWILIO_AUTH_TOKEN = '61816dc5a5701775b63caf590adb8756'
num=7607904382
my_twilio="+1"+str(num)
totp = pyotp.TOTP('JBSWY3DPEHPK3PXP')
pin=totp.now()

#NEXMO_API_KEY='5c5e821f'
#NEXMO_API_SECRET='03fbb5b222ab1913'

from django.contrib.auth.models import User
from friendship.models import Friend, Follow

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
                      'https://instaapplication.herokuapp.com/email_activate/?user_email=' + email
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
            username=form.cleaned_data['username']
            number=form.cleaned_data['number']
            user_number="+91"+str(number)
            # saving data to DB
            finduser = UserModel.objects.filter(username=username).first()
            finduser.number=number
            finduser.save()

            #totp = pyotp.TOTP('JBSWY3DPEHPK3PXP')
            #pin=totp.now()
            #global pin
            #client = nexmo.Client(key=NEXMO_API_KEY, secret=NEXMO_API_SECRET)
            #client.send_message({
             #   'from': 'Instagram',
              #  'to': user_number,
             #   'text':"Instagram Verification Code:"+pin+". Only valid for 30 seconds.",
            #})
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            client.messages.create(to=user_number, from_=my_twilio,body="Instagram Verification Code:"+pin+". Only valid for 30 seconds.")

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
            return HttpResponseRedirect('/login/')
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
        profilepic = ProfilePicModel.objects.filter(user=user).first()
        firstpost = PostModel.objects.filter(user=user).first()
        for post in posts:
            existing_like=LikeModel.objects.filter(post_id=post.id,user=user).first()
            if existing_like:
                post.has_liked=True
        if profilepic:
            profilepic.has_picture=True
        if firstpost:
            firstpost.has_post=True
        return render(request, 'feeds.html', {'posts' : posts,'user':user,'profilepic':profilepic,'firstpost':firstpost})
      else:
        return redirect('/login/')


def profile_view(request):
    user = check_validation(request)
    if user:
        posts = PostModel.objects.filter(user=user).all().order_by('-created_on')
        profilepic=ProfilePicModel.objects.filter(user=user).first()
        if profilepic:
            profilepic.has_picture=True
        return render(request, 'profile.html', {'posts': posts,'user':user,'profilepic':profilepic})
    else:
        return redirect('/login/')
@csrf_exempt
def profile_by_search(request):
    user=check_validation(request)
    if user:
        username=request.POST.get('username')
        print username
        searcheduser=UserModel.objects.filter(username=username).first()
        posts = PostModel.objects.filter(user=searcheduser).all().order_by('-created_on')
        profilepic = ProfilePicModel.objects.filter(user=searcheduser).first()
        if profilepic:
            print username+str(searcheduser)
            profilepic.has_picture = True
        return render(request, 'profile.html', {'posts': posts, 'user': searcheduser, 'profilepic': profilepic})
    else:
        return redirect('/login/')

def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        #form = LikeForm(request.POST)
        #if form.is_valid():
            #post_id = form.cleaned_data.get('post').id
        post_id=request.POST['postId']
        existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()

        if not existing_like:
            LikeModel.objects.create(post_id=post_id, user=user)
            data={
                "flag":True
            }
        else:
            existing_like.delete()
            data = {
                "flag": False
            }

        return JsonResponse(data)


    else:
        return redirect('/login/')


def comment_view(request):
  user = check_validation(request)
  if user and request.method == 'POST':
    #form = CommentForm(request.POST)
    #if form.is_valid():
    post_id = request.POST['cmntPostId']
    comment_text = request.POST['commentText']
    comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
    comment.save()
    created_comment={
        "text":comment_text,
    }
    return JsonResponse(created_comment)
  else:
    return redirect('/login')


def profile_pic(request):
    user=check_validation(request)
    if user:
        if request.method == "GET":
            form = ProfilePicForm()
            return render(request, 'profilepic.html', {'form': form})
        elif request.method == "POST":
            post = ProfilePicModel.objects.filter(user=user).first()
            #if already a profile pic is existing
            if post:
                post = ProfilePicModel.objects.filter(user=user).first()
                post.delete()
                print "profile Pic deleted"
                form = ProfilePicForm(request.POST, request.FILES)
                if form.is_valid():
                    image = form.cleaned_data.get('image')
                    post = ProfilePicModel(user=user, image=image)
                    post.save()
                    path = str(BASE_DIR + '/' + post.image.url)
                    client = ImgurClient("7c523b250772ade", "5307069c8ab8398c385cfbeacd51857ed22")
                    post.image_url = client.upload_from_path(path, anon=True)['link']
                    post.save()
            #if only default pic is there
            else:
                form = ProfilePicForm(request.POST, request.FILES)
                if form.is_valid():
                    image = form.cleaned_data.get('image')
                    post = ProfilePicModel(user=user, image=image)
                    post.save()
                    path = str(BASE_DIR + '/' + post.image.url)
                    client = ImgurClient("7c523b250772ade", "5307069c8ab8398c385cfbeacd51857ed22")
                    post.image_url = client.upload_from_path(path, anon=True)['link']
                    post.save()
        return redirect('/user_profile/')

    else:
        return redirect('/login/')




def remove_profile_pic(request):
    user=check_validation(request)
    if user:

            post=ProfilePicModel.objects.filter(user=user).first()
            post.delete()
            print "profile Pic deleted"
            return redirect('/user_profile/')

    else:
        return redirect('/login/')


def search_user(request):
    user=check_validation(request)
    if user:
        if request.method=='POST':
            username=request.POST['userName']
            print username
            match=UserModel.objects.filter(Q(name__icontains=username)| Q(username__icontains=username))
            data = serializers.serialize("json", match)
            print data
            if match:
                return JsonResponse({
                    'searchresult':data
                })
            else:
                return JsonResponse({'message':'User Not Found'})
        else:
            return HttpResponseRedirect('/feed/')
    else:
        return HttpResponseRedirect('/login/')



def logout(request):
    user = check_validation(request)
    if user:
        token = SessionToken.objects.filter(user=user)
        token.delete()
        return redirect('/login/')
    else:
        return redirect('/login/')



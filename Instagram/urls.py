"""Instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin



from InstagramApp.views import signup_view
from InstagramApp.views import login_view
from InstagramApp.views import feed_view
from InstagramApp.views import post_view
from InstagramApp.views import like_view,comment_view,email_activate,otp_send,otp_receive


urlpatterns = [
    url(r'^$', signup_view),
    url(r'^admin/',admin.site.urls),
    url(r'^login/', login_view),
    url(r'^feed/', feed_view),
    url(r'^post/', post_view),
    url(r'^like/', like_view),
    url(r'^comment/', comment_view),
    url(r'^email_activate/', email_activate),
    url(r'^otp_verification/',otp_send),
    url(r'^otp_receive/',otp_receive)

]
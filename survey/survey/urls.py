"""survey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from Join.views import join,join_member,login,login_check,logout
from poll.views import (poll_page,question_entry_page,question_entry,
    poll_page_admin,question_update_page,question_delete,
    poll_submit)
from main_page.views import (main_page,review_page_User,
    review_page_User_Detail,review_page_Admin,review_page_Admin_Detail,
    review_update)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^join/$', join),
    url(r'^join_member/$',join_member),
    url(r'^login/$',login),
    url(r'^login_check/$',login_check),
    url(r'^logout/$',logout),
    # Join APP

    url(r'^poll_page/$',poll_page), # For User

    url(r'^poll_entry_page/$',question_entry_page), # For Administor
    url(r'^poll_entry/$',question_entry),
    url(r'^poll_page_admin/$',poll_page_admin), 
    url(r'^poll_update/$',question_update_page),
    url(r'^poll_delete/$',question_delete),
    url(r'^poll_submit/$',poll_submit),
    # Poll APP

    url(r'^',main_page),
    url(r'^review/',review_page_User),
    url(r'^review/(?P<No>\d+)/',review_page_User_Detail),
    url(r'^review_admin/',review_page_Admin),
    url(r'^review_admin/(?P<No>\d+)/',review_page_Admin_Detail),
    url(r'^review_update/(?P<No>\d+)/',review_update)
    # Main_Page APP

]

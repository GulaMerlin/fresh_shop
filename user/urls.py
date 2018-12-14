from django.conf.urls import url

from user import views

urlpatterns = [
    # url(r'^index/$', views.index),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),

    # 用户中心
    url(r'^user_center_info/$', views.user_center_info, name='user_center_info'),
    url(r'^user_center_site/$', views.user_center_site, name='user_center_site'),
    url(r'^user_center_order/$', views.user_center_order, name='user_center_order'),

]
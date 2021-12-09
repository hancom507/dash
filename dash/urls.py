# 소스 수정시 서버 재실행

from django.urls import path
from django.contrib import admin

from . import views

app_namp = 'dash'
# path() 첫번째 인자는 url에 있는 값, 두번째 인자는
urlpatterns = [
    path('', views.index),
    path('test/', views.test),
    path('login.html', views.demo_plot_view),
    path('map.html', views.map),
    path('manager.html', admin.site.urls),
    path('report.html', views.report),
    path('dash.html', views.index),
]
# 소스 수정시 서버 재실행

from django.urls import path
from django.contrib import admin
from .views import index_views, map_views, report_views, dg_index_views

from . import views

app_name = 'dash'
# path() 첫번째 인자는 url에 있는 값, 두번째 인자는
urlpatterns = [
    path('', index_views.index),
    path('', dg_index_views.index),
    path('dash.html', dg_index_views.index),
    path('dash.html', index_views.index),
    #path('test/', views.test),
    #path('login.html', views.demo_plot_view),
    path('manager.html', admin.site.urls),
    # view.py
    path('map.html',map_views.map, name='map'),
    path('report.html', report_views.report),
]
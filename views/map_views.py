# 이 파일 수정시 서버를 재 시동해야함
from django.shortcuts import render, redirect
# from django.http import HttpResponse
from plotly.offline import plot
import plotly.graph_objects as go
from folium import plugins, Marker, Icon, DivIcon
import folium
import pandas as pd
from datetime import datetime, timedelta
import time

def map(request):
    df = pd.read_csv('./data/DevList.csv')
    df_data = pd.read_csv('./data/floatPopPerDay.csv')
    lat = df['위도'].mean()   #위도의 평균값을 구하기 위해 mean() 사용
    long = df['경도'].mean()  #처음 위치 잡기위해 평균값 사용
    m = folium.Map([lat, long], zoom_start=17, width='100%', height='100%')
    tooltip = "클릭해주세요"
    zoneName = df['존 이름'].drop_duplicates()
    color = ['red', 'orange','darkblue','green','blue','gray','purple']
    t = dict(zip(zoneName, color)) # 존 이름과 컬러색 묶음
    radius = 50
    radiusa = [150,130,110,90,70,50,30] #원크기 지정
    for i in df.itertuples():
        folium.Marker(location=[i[11], i[12]],
                      icon=Icon(color=t[i[10]]),
                      popup=f'<pre>존 이름 : {i[10]} </pre>',
                      tooltip=tooltip).add_to(m)
        '''
        folium.CircleMarker(location=[i[11], i[12]],
                      radius=radius).add_to(m)
                      '''
    # 존별 중간위치에 circle함수 적용 / data크기 순에 따라 원의 크기 결정
    for i in df_data.itertuples():
        df_zonelat = df[df['존 이름'] == i[2]]['위도'].mean() #존 이름별 위도 평균
        df_zonelong = df[df['존 이름'] == i[2]]['경도'].mean() #존 이름별 경도 평균
        folium.Circle(location=[df_zonelat,df_zonelong],
                      radius=radiusa[i[0]],
                      tooltip=i[2], #동그라미에 마우스 가져다대면 존 이름 팝업 뜸
                      color='rgb(0,0,0,0)',
                      fill_color=t[i[2]]).add_to(m)
        folium.Marker(location=[df_zonelat,df_zonelong],
                      icon=folium.DivIcon(
                          icon_size=(250, 36),
                          icon_anchor=(-2, -1),
                          html = f"""<div><h3 style="color:{t[i[2]]};"><b style="text-align:center;">{i[2]}</b></h3></div>""") #map위에 존별 이름 표시
                      ).add_to(m)

    #popup = folium.Popup(test, max_width=2650)
    #folium.RegularPolygonMarker(location=[51.5, -0.25], popup=popup).add_to(m)
    maps = m._repr_html_()

    # return redirect('https://www.google.com')
    return render(request, "dash/map.html",context={'map':maps})

'''
class FoliumView(TemplateView):
    template_name = "folium_app/map.html"

    def get_context_data(self, **kwargs):
        figure = folium.Figure()
        m = folium.Map(
            location=[45.372, -121.6972],
            zoom_start=12,
            tiles='Stamen Terrain'
        )
        m.add_to(figure)

        folium.Marker(
            location=[45.3288, -121.6625],
            popup='Mt. Hood Meadows',
            icon=folium.Icon(icon='cloud')
        ).add_to(m)

        folium.Marker(
            location=[45.3311, -121.7113],
            popup='Timberline Lodge',
            icon=folium.Icon(color='green')
        ).add_to(m)

        folium.Marker(
            location=[45.3300, -121.6823],
            popup='Some Other Location',
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
        figure.render()
        return {"map": figure}
'''

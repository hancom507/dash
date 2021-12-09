# 이 파일 수정시 서버를 재 시동해야함
from django.shortcuts import render, redirect
from django.http import HttpResponse
from plotly.offline import plot
import plotly.graph_objects as go
from folium import plugins, Marker, Icon
import folium
import pandas as pd
import datetime
#import dash_html_components as html

# Create your views here.
# render()는 첫번째 인자로 request, 두번째 인자로 템플릿, 세번째 인자로 context(dic타입)으로 전달
# key는 템플릿에서 사용될 템플릿변수명이 되고, value는 전달하는 내용이 된다.

def report(request):
    return render(request, 'dash/report.html')

def test(request):
    return render(request,'dash/test.html')

def index(request):
    df = pd.read_csv('./data/zoneVisitor.csv')
    figHour = go.Figure()
    df['TIME'] = pd.to_datetime(df['TIME'], errors='coerce')
    hour = df.query("TIME >= '2021-08-05 00:00' and TIME <= '2021-08-05 23:59'")
    figHour.add_trace(
        go.Bar(
            x=hour['TIME'].dt.hour,
            y=hour['시외버스터미널']
        )
    )
    plot_hour = plot(figHour, output_type='div')

    df = pd.read_csv('./data/zoneVisitorDay.csv')
    df['TIME'] = pd.to_datetime(df['TIME'], errors='coerce')
    figWeek = go.Figure()
    week = df.query("'2021-08-22' <= TIME <= '2021-08-29'")
    figWeek.add_trace(
        go.Bar(
            x=week['TIME'].dt.day,
            y=week['시외버스터미널']
        )
    )
    plot_week = plot(figWeek, output_type='div')

    df = pd.read_csv('./data/zoneVisitorDay.csv')
    df['TIME'] = pd.to_datetime(df['TIME'], errors='coerce')
    figMonth = go.Figure()
    month = df.query("'2021-09-01' <= TIME < '2021-10-01'")
    figMonth.add_trace(
        go.Bar(
            x=month['TIME'].dt.day,
            y=month['시외버스터미널']
        )
    )
    plot_month = plot(figMonth, output_type='div')


    return render(request, "dash/index.html", context={'plot_hour': plot_hour,
                                                       'plot_week': plot_week,
                                                       'plot_month': plot_month
                                                       }
                  )



def login(request):
    #return HttpResponse("login")
    return render(request, "dash/login.html")

def map(request):
    df = pd.read_csv('./data/DevList.csv')
    lat = df['위도'].mean()   #위도의 평균값을 구하기 위해 mean() 사용
    long = df['경도'].mean()  #처음 위치 잡기위해 평균값 사용
    m = folium.Map([lat, long], zoom_start=16, width='100%', height='100%')
    tooltip = "클릭해주세요"
    zoneName = df['존 이름'].drop_duplicates()
    color = ['red', 'orange','darkblue','green','blue','gray','purple']
    t = dict(zip(zoneName, color))
    radius = 50
    for i in df.itertuples():
        folium.Marker(location=[i[11], i[12]],
                      icon=Icon(color=t[i[10]]),
                      popup=f'<pre>존 이름 : {i[10]} </pre>',
                      tooltip=tooltip).add_to(m)
        folium.Circle(location=[i[11], i[12]],
                      radius=radius).add_to(m)

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




def demo_plot_view(request):
    """
    View demonstrating how to display a graph object
    on a web page with Plotly.
    """

    # Generating some data for plots.
    x = [i for i in range(-10, 11)]
    y1 = [3 * i for i in x]
    y2 = [i ** 2 for i in x]
    y3 = [10 * abs(i) for i in x]

    # List of graph objects for figure.
    # Each object will contain on series of data.
    graphs = []

    # Adding linear plot of y1 vs. x.
    graphs.append(
        go.Scatter(x=x, y=y1, mode='lines', name='Line y1')
    )

    # Adding scatter plot of y2 vs. x.
    # Size of markers defined by y2 value.
    graphs.append(
        go.Scatter(x=x, y=y2, mode='markers', opacity=0.8,
                   marker_size=y2, name='Scatter y2')
    )

    # Adding bar plot of y3 vs x.
    graphs.append(
        go.Bar(x=x, y=y3, name='Bar y3')
    )

    # Setting layout of the figure.
    layout = {
        'title': 'Title of the figure',
        'xaxis_title': 'X',
        'yaxis_title': 'Y',
        'height': 420,
        'width': 560,
    }

    # Getting HTML needed to render the plot.
    plot_div = plot({'data': graphs, 'layout': layout},
                    output_type='div')

    return render(request, 'dash/login.html',
                  context={'plot_div': plot_div})



'''
df = pd.read_csv('../data/DevList.csv')
lat = df['위도'].mean()
long = df['경도'].mean()
m = folium.Map([lat,long],zoom_start=16)
tooltip="클릭해주세요"
for i in df.itertuples():
    #print(i[11])
    #Marker(location=[i['xcoordinate'][1],i['ycoordinate'][1]]).add_to(m)
    folium.Marker(location = [i[11],i[12]], popup=f'<pre>존 이름 : {i[10]} </pre>', tooltip = tooltip).add_to(m)


m.save("test.html")
'''

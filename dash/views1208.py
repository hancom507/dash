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
    """
    #전일 방문객
    df = pd.read_csv('./data/floatPopPerDay.csv')
    data = df['data'].sum()
    fig1 = go.Figure()
    fig1.add_trace(
        go.Indicator(
            mode="number",
            value=data,
            title={'text':"전일 방문객", 'font':{'size':20}},
            number={'suffix':'명', 'font':{'size':20}, 'valueformat':',d'},
        )
    )
    fig1.update_layout(height=100)
    plot_div1 = plot(fig1, output_type='div')

    #지난달 총 방문객
    df = pd.read_csv('./data/countMonth.csv')
    data = df['data'][0]
    fig2 = go.Figure()
    fig2.add_trace(
        go.Indicator(
            mode="number",
            value=data,
            title={'text': "지난달 총 방문객", 'font': {'size': 20}},
            number={'suffix': '명', 'font': {'size': 20}, 'valueformat': ',d'},
        )
    )
    fig2.update_layout(height=100)
    plot_div2 = plot(fig2, output_type='div')

    #체류 시간
    df = pd.read_csv('./data/residenceTime.csv')
    data = df['data'].mean()//60
    fig3 = go.Figure()
    fig3.add_trace(
        go.Indicator(
            mode="number",
            value=data,
            title={'text': "<b>체류 시간</b>", 'font': {'size': 20}},
            number={'prefix':'<b>', 'suffix': '분</b>', 'font': {'size': 20,'family':"Arial"}, 'valueformat': 'd'},
        )
    )
    fig3.update_layout(height=100)
    plot_div3 = plot(fig3, output_type='div')

    #어제 재방문객
    df = pd.read_csv('./data/revisitPerDay.csv')
    data = df['data'].sum()
    fig4 = go.Figure()
    fig4.add_trace(
        go.Indicator(
            mode="number",
            value=data,
            title={'text': "어제 재방문객", 'font': {'size': 20}},
            number={'suffix': '명', 'font': {'size': 20}, 'valueformat': ',d'},
        )
    )
    fig4.update_layout(height=100)
    plot_div4 = plot(fig4, output_type='div')


    return render(request, "dash/index.html", context={'plot_div1': plot_div1,
                                                       'plot_div2': plot_div2,
                                                       'plot_div3': plot_div3,
                                                       'plot_div4': plot_div4
                                                       }
                  )
    """
    df = pd.read_csv('./data/zoneVisitor.csv')
    fig = go.Figure()
    df['TIME'] = pd.to_datetime(df['TIME'], errors='coerce')
    k = df.query("TIME >= '2021-08-05 00:00' and TIME <= '2021-08-05 23:59'")
    trace1 = go.Bar(
        x=k['TIME'].dt.hour,
        y=k['시외버스터미널']
    )
    data = [trace1]
    layout = go.Layout(title="일별 데이타")
    fig = go.Figure(data,layout)
    plot_div = plot(fig, output_type='div')
    return render(request, "dash/index.html", context={'plot_div': plot_div})
    """
    fig.add_trace(
        go.Bar(
            x=k['TIME'].dt.hour,
            y=k['시외버스터미널'] 
        )
    )
    plot_div = plot(fig, output_type='div')
    return render(request, "dash/index.html", context={'plot_div':plot_div})
    """


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

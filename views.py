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
# import dash_html_components as html

# Create your views here.
# render()는 첫번째 인자로 request, 두번째 인자로 템플릿, 세번째 인자로 context(dic타입)으로 전달
# key는 템플릿에서 사용될 템플릿변수명이 되고, value는 전달하는 내용이 된다.




def test(request):
    #regionValue = request.POST.getlist('region[]')  # report.html에서 'name =region[]' 인 값 들고옴
    if request.method == 'POST':
        return render(request, 'reprot.html', {'POST': 'POST 방식입니다.'})
    elif request.method == 'GET':
        return render(request, 'reprot.html', {'GET': 'GET 방식입니다.'})
    else:
        return render(request, 'reprot.html', {'test':'regionValue'})


def login(request):
    #return HttpResponse("login")
    return render(request, "dash/login.html")


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

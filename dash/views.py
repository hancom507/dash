# 이 파일 수정시 서버를 재 시동해야함
from django.shortcuts import render, redirect
# from django.http import HttpResponse
from plotly.offline import plot
import plotly.graph_objects as go
from folium import plugins, Marker, Icon
import folium
import pandas as pd
from datetime import datetime, timedelta
# import dash_html_components as html

# Create your views here.
# render()는 첫번째 인자로 request, 두번째 인자로 템플릿, 세번째 인자로 context(dic타입)으로 전달
# key는 템플릿에서 사용될 템플릿변수명이 되고, value는 전달하는 내용이 된다.


def report(request):
    df = pd.read_csv('./data/zoneVisitor.csv')
    fighour = go.Figure()
    df['TIME'] = pd.to_datetime(df['TIME'], errors='coerce')
    hour = df.query("TIME >= '2021-08-05 00:00' and TIME <= '2021-08-05 23:59'")
    fighour.add_trace(
        go.Bar(
            x=hour['TIME'].dt.hour,
            y=hour['시외버스터미널']
        )
    )
    plot_hour = plot(fighour, output_type='div')

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

    return render(request, 'dash/report.html', context={'plot_hour': plot_hour,
                                                       'plot_week': plot_week,
                                                       'plot_month': plot_month
                                                       }
                  )


def test(request):
    return render(request,'dash/test.html')

def index(request):
    # 전일 방문객
    #df = pd.read_csv('./data/floatPopPerDay.csv')
    df = pd.read_csv('./data/zoneVisitorDay.csv')
    #df.drop(['TIME'], axis=1, inplace=True)  # 시간값은 계산 못하기에 제거
    #del df['TIME']
    data = df.iloc[-1][:-1].sum()
    deltas = df.iloc[-2][:-1].sum()
    fig1 = go.Figure()
    fig1.add_trace(
        go.Indicator(
            mode="number+delta",
            value=data,
            title={'text': "전일 방문객", 'font': {'size': 20}},
            number={'suffix': '명', 'font': {'size': 20}, 'valueformat':',.0f'},
            delta=dict(reference=deltas, increasing=dict(color='blue'))
        )
    )
    fig1.update_layout( width=150, height=100, margin=dict(l=0, r=0, b=0, t=0))
    plot_div1 = plot(fig1, output_type='div')

    # 지난달 총 방문객
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
    fig2.update_layout(width=150, height=100)
    plot_div2 = plot(fig2, output_type='div')

    # 체류 시간
    df = pd.read_csv('./data/residenceTime.csv')
    data = df['data'].mean() // 60
    fig3 = go.Figure()
    fig3.add_trace(
        go.Indicator(
            mode="number",
            value=data,
            title={'text': "<b>체류 시간</b>", 'font': {'size': 20}},
            number={'prefix': '<b>', 'suffix': '분</b>', 'font': {'size': 20, 'family': "Arial"}, 'valueformat': 'd'},
        )
    )
    fig3.update_layout(width=150, height=100)
    plot_div3 = plot(fig3, output_type='div')

    # 어제 재방문객
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
    fig4.update_layout(width=150, height=100)
    plot_div4 = plot(fig4, output_type='div')


    #지역별 일일방문객
    df = pd.read_csv('./data/zoneVisitorDay.csv')
    zoneDay = go.Figure()
    y = df.columns[1:-1]
    x = df.iloc[-1][1:-1]
    colors = ['blue','lightslategray','green','red','teal','lime','purple' ]
    #colors[4] = 'crimson'
    zoneDay.add_trace(
        go.Bar(
            y=y,
            x=x,
            text = y,
            orientation = 'h',
            marker_color = colors
        )
    )
    zoneDay.update_layout(width=540, height=540,xaxis=dict(autorange=True),yaxis=dict(visible=False),
                          margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='LightSteelBlue')
    plot_zoneDay = plot(zoneDay, output_type='div')

    # 지난요일별 방문객
    df_lastw = pd.read_csv('./data/zoneVisitorDay.csv')
    del df_lastw['Unnamed: 0']
    # 기간 검색을 위해 시간값을 변환
    df_lastw['TIME'] = pd.to_datetime(df_lastw['TIME'], format='%Y-%m-%d')
    # today= datetime.today()
    today = datetime.today() - timedelta(67)   #임시로 특정 날짜 지정함
    #지난주 일요일 값을 구함
    startDate = today - timedelta(today.weekday()) - timedelta(8)
    df_lastw = df_lastw[(df_lastw['TIME'] >= startDate) & (df_lastw['TIME'] < startDate + timedelta(7))]
    y = df_lastw.sum(axis=1)
    x = ['월요일','화요일','수요일','목요일','금요일','토요일','일요일']
    fig_w = go.Figure()
    fig_w.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='markers + lines'))
    fig_w.update_layout(width=540, height=500, margin=dict(l=0,r=0,t=0,b=0) )
    plot_fig_w = plot(fig_w, output_type='div')

    # 실시간 방문객
    df_visitor = pd.read_csv('./data/zoneVisitor.csv')
    df_visitor['TIME'] = pd.to_datetime(df_visitor['TIME'], format='%Y-%m-%d %H:%M')
    df_visitor=df_visitor.iloc[-1]
    fig_pie = go.Figure()
    fig_pie.add_trace(
        go.Pie( labels = df_visitor.index[1:-1],
                values= df_visitor,
                textinfo='percent',
                insidetextorientation='tangential',
                hole=0.2)
    )
    fig_pie.update_layout( width=540, height=500, annotations=[dict(text='부안', font_size=20, showarrow=False)],
                           margin=dict(l=0,r=0,t=0,b=0))
    plot_fig_pie = plot(fig_pie, output_type='div')

    # 지난주 재방문객
    df_lastWeek = pd.read_csv('./data/zoneVisitorWeek.csv')
    fig_lastWeek = go.Figure()
    x = df_lastWeek.columns[1:-1]
    y = df_lastWeek.iloc[-1][1:-1]
    colors = ['blue', 'lightslategray', 'green', 'red', 'teal', 'lime', 'purple']
    # colors[4] = 'crimson'
    fig_lastWeek.add_trace(
        go.Bar(
            y=y,
            x=x,
            text=y,
            #orientation='h',
            marker_color=colors
        )
    )
    fig_lastWeek.update_layout(width=540, height=700, xaxis=dict(autorange=True), yaxis=dict(visible=True),
                               margin=dict(l=0,r=0,t=0,b=0))
    plot_lastWeek = plot(fig_lastWeek, output_type='div')

    return render(request, "dash/index.html", context={'plot_div1': plot_div1,
                                                       'plot_div2': plot_div2,
                                                       'plot_div3': plot_div3,
                                                       'plot_div4': plot_div4,
                                                       'plot_div5': plot_zoneDay,
                                                       'plot_div6': plot_fig_w,
                                                       'plot_div7': plot_fig_pie,
                                                       'plot_div8': plot_lastWeek
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

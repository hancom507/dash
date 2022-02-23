# 이 파일 수정시 서버를 재 시동해야함
from django.shortcuts import render, redirect
# from django.http import HttpResponse
from plotly.offline import plot
import plotly.graph_objects as go
from folium import plugins, Marker, Icon, DivIcon
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

    #날짜별, 지역별 방문 그래프
    startDate = request.POST.get('startDate') # 시작 날짜
    endDate = request.POST.get('endDate') # 끝나는 날짜
    regionValue = request.POST.getlist('region[]')  # report.html에서 'name =region[]' 인 값 들고옴
    regionValue.append('TIME') # regionValue리스트에 'TIME' 요소추가
    df = pd.read_csv('./data/zoneVisitorDay.csv')
    df['TIME'] = pd.to_datetime(df['TIME'], errors='coerce')
    figWeek = go.Figure()
    #week = df.query("'2021-08-22' <= TIME <= '2021-08-29'")
    a='2021-08-22'
    week = df.query("@a <= TIME <= '2021-08-29'") # 변수명으로 되는데 왜 post로 받아온 변수명으로는 안되는지 모르겠다.
    region = week[regionValue] # 선택한 지역들과 'TIME' 컬럼으로 데이터 프레임 생성
    x = region.columns[0:-1] # TIME 컬럼 빼고 지역들만 선택
    trace = []
    n = 0
    for i in region['TIME']: # 선택한 시간 만큼 그래프를 보여줌
        trace.append(go.Bar(
            x=x,
            y=week.iloc[n][1:-2],
            name=str(i),
        ))
        n = n + 1

    data = trace
    layout = go.Layout()
    figWeek = go.Figure(data, layout)


    '''
    figWeek.add_trace(
        go.Bar(
            x=week['TIME'].dt.day,
            y=week[regionValue[0]]
        )
    )
 '''
    figWeek.update_layout(
                          height=540,
                          xaxis=dict(autorange=True,zeroline=False),#그래프의 그리드와 영점선 삭제
                          yaxis=dict(visible=False),
                          margin=dict(l=0,r=0,t=0,b=0),
                          paper_bgcolor="#001B50",
                          plot_bgcolor="rgba(0,0,0,0)",#그래프 배경 투명색
                          autosize=True,
                          font=dict(color="#ffffff") #그래프 폰트 색상 변경
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

    rgv = print('e',startDate,endDate) # report.html 에서 값 잘 불어오는지 확인 cmd창에서 확인 할 수 있음

    return render(request, 'dash/report.html', context={'plot_hour': plot_hour,
                                                       'plot_week': plot_week,
                                                       'plot_month': plot_month,
                                                       'rgv': rgv,
                                                       }
                  )



def test(request):
    #regionValue = request.POST.getlist('region[]')  # report.html에서 'name =region[]' 인 값 들고옴
    if request.method == 'POST':
        return render(request, 'reprot.html', {'POST': 'POST 방식입니다.'})
    elif request.method == 'GET':
        return render(request, 'reprot.html', {'GET': 'GET 방식입니다.'})
    else:
        return render(request, 'reprot.html', {'test':'regionValue'})

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
            title={'text': "전일 방문객", 'font': {'size': 15, 'color':'#C5C5C5'}},
            number={'suffix': '명', 'font': {'size': 20, 'color':'#ffffff'}, 'valueformat':',.0f'},
            delta=dict(reference=deltas, increasing=dict(color='blue'))
        )
    )
    fig1.update_layout( width=290, #데이터를 가운데로 맞추기 위해 넓이를 늘림
                        height=100,
                        margin=dict(l=0, r=0, b=0, t=0),
                        paper_bgcolor = "rgba(0,0,0,0)") #텍스트상자배경색
    plot_div1 = plot(fig1, output_type='div')

    # 지난달 총 방문객
    df = pd.read_csv('./data/countMonth.csv')
    data = df['data'][0]
    fig2 = go.Figure()
    fig2.add_trace(
        go.Indicator(
            mode="number",
            value=data,
            title={'text': "지난달 총 방문객", 'font': {'size': 15, 'color':'#C5C5C5'}},
            number={'suffix': '명', 'font': {'size': 20, 'color':'#FFFFFF'}, 'valueformat': ',d'},
        )
    )
    fig2.update_layout(width=290,
                       height=100,
                       paper_bgcolor = "rgba(0,0,0,0)")
    plot_div2 = plot(fig2, output_type='div')

    # 체류 시간
    df = pd.read_csv('./data/residenceTime.csv')
    data = df['data'].mean() // 60
    fig3 = go.Figure()
    fig3.add_trace(
        go.Indicator(
            mode="number",
            value=data,
            title={'text': "<b>체류 시간</b>", 'font': {'size': 15, 'color':'#C5C5C5'}},
            number={'prefix': '<b>', 'suffix': '분</b>', 'font': {'size': 20, 'family': "Arial", 'color':'#FFFFFF'}, 'valueformat': 'd'},
        )
    )
    fig3.update_layout(width=290,
                       height=100,
                       paper_bgcolor = "rgba(0,0,0,0)")
    plot_div3 = plot(fig3, output_type='div')

    # 어제 재방문객
    df = pd.read_csv('./data/revisitPerDay.csv')
    data = df['data'].sum()
    fig4 = go.Figure()
    fig4.add_trace(
        go.Indicator(
            mode="number",
            value=data,
            title={'text': "어제 재방문객", 'font': {'size': 15, 'color':'#C5C5C5'}},
            number={'suffix': '명', 'font': {'size': 20, 'color':'#FFFFFF'}, 'valueformat': ',d'},
        )
    )
    fig4.update_layout(width=290,
                       height=100,
                       paper_bgcolor = "rgba(0,0,0,0)")
    plot_div4 = plot(fig4, output_type='div')


    #지역별 일일방문객
    df = pd.read_csv('./data/zoneVisitorDay.csv')
    zoneDay = go.Figure()
    y = df.columns[1:-1]
    x = df.iloc[-1][1:-1]
    colors = ['#9515FF','#8EE600','lightgray','#0486DE','#FB195A','#FA9F1A' ] #바 색상변경
    #colors[4] = 'crimson'
    zoneDay.add_trace(
        go.Bar(
            y=y,
            x=x,
            text = y,
            orientation = 'h',
            marker_color = colors,
        )
    )
    zoneDay.update_layout(width=540,
                          height=540,
                          xaxis=dict(autorange=True,zeroline=False),#그래프의 그리드와 영점선 삭제
                          yaxis=dict(visible=False),
                          margin=dict(l=0,r=0,t=0,b=0),
                          paper_bgcolor="#001B50",
                          plot_bgcolor="rgba(0,0,0,0)",#그래프 배경 투명색
                          autosize=True,
                          font=dict(color="#ffffff") #그래프 폰트 색상 변경
                          )
    plot_zoneDay = plot(zoneDay, output_type='div')

    # 지난요일별 방문객
    df_lastw = pd.read_csv('./data/zoneVisitorDay.csv')
    del df_lastw['Unnamed: 0']
    '''
    # 기간 검색을 위해 시간값을 변환
    df_lastw['TIME'] = pd.to_datetime(df_lastw['TIME'], format='%Y-%m-%d')
    
    # today= datetime.today()
    today = datetime.today() - timedelta(67)   #임시로 특정 날짜 지정함
    
    #지난주 일요일 값을 구함
    startDate = today - timedelta(today.weekday()) - timedelta(8)
    df_lastw = df_lastw[(df_lastw['TIME'] >= startDate) & (df_lastw['TIME'] < startDate + timedelta(7))]
    '''
    #오늘 요일구하기(0-월 6-일)
    weektoday = datetime.today().weekday()

    #y = df_lastw.sum(axis=1)
    y=[]
    #마지막행이 오늘 날짜라고 생각
    for i in range(-8-weektoday,-weektoday): # 지난주 요일별로 부안 전체 방문자수 더해서 'y'리스트에 넣기
        y.append(sum(df_lastw.iloc[i][1:7]))

    x = ['월요일','화요일','수요일','목요일','금요일','토요일','일요일']

    fig_w = go.Figure()
    fig_w.add_trace(
        go.Scatter(
            x=x,
            y=y,
            line= dict(color='#FA9F1A'),
            mode='markers + lines'))

    fig_w.update_layout(width=500,
                        height=600,
                        margin=dict(l=0,r=0,t=20,b=0),
                        xaxis=dict(showgrid=False),
                        paper_bgcolor="#001B50",
                        plot_bgcolor="rgba(0,0,0,0)",
                        autosize=True,
                        font=dict(color="#ffffff")
                        )
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
                hole=0.4)
    )
    fig_pie.update_layout( width=500, # 원형그래프가 상자 안에 들어 올 수 있게 크기 조정
                           height=500,
                           annotations=[dict(text='부안', font_size=20, showarrow=False)],
                           margin=dict(l=0,r=0,t=0,b=0),
                           paper_bgcolor="#001B50",
                           plot_bgcolor="rgba(0,0,0,0)",
                           autosize=True,
                           font=dict(color="#ffffff")
                           )
    plot_fig_pie = plot(fig_pie, output_type='div')

    # 지난주 재방문객
    df_lastWeek = pd.read_csv('./data/zoneVisitorWeek.csv')
    fig_lastWeek = go.Figure()
    x = df_lastWeek.columns[1:-1]
    y = df_lastWeek.iloc[-1][1:-1]
    colors = ['#9515FF','#8EE600','lightgray','#0486DE','#FB195A','#FA9F1A']
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
    fig_lastWeek.update_layout(width=500,
                               height=600,
                               xaxis=dict(autorange=True),
                               yaxis=dict(visible=True),
                               margin=dict(l=0,r=0,t=20,b=0),
                               paper_bgcolor="#001B50",
                               plot_bgcolor="rgba(0,0,0,0)",
                               autosize=True,
                               font=dict(color="#ffffff")
                               )
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

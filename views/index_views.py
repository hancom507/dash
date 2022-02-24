from django.shortcuts import render, redirect
# from django.http import HttpResponse
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import time


def index(request):
    # 전일 방문객
    # df = pd.read_csv('./data/floatPopPerDay.csv')
    df = pd.read_csv('./data/zoneVisitorDay.csv')
    # df.drop(['TIME'], axis=1, inplace=True)  # 시간값은 계산 못하기에 제거
    # del df['TIME']
    data = df.iloc[-1][:-1].sum()
    deltas = df.iloc[-2][:-1].sum()
    fig1 = go.Figure()
    fig1.add_trace(
        go.Indicator(
            mode="number+delta",
            value=data,
            title={'text': "전일 방문객", 'font': {'size': 15, 'color': '#C5C5C5'}},
            number={'suffix': '명', 'font': {'size': 20, 'color': '#ffffff'}, 'valueformat': ',.0f'},
            delta=dict(reference=deltas, increasing=dict(color='blue'))
        )
    )
    fig1.update_layout(width=290,  # 데이터를 가운데로 맞추기 위해 넓이를 늘림
                       height=100,
                       margin=dict(l=0, r=0, b=0, t=0),
                       paper_bgcolor="rgba(0,0,0,0)")  # 텍스트상자배경색
    plot_div1 = plot(fig1, output_type='div')

    # 지난달 총 방문객
    df = pd.read_csv('./data/countMonth.csv')
    data = df['data'][0]
    fig2 = go.Figure()
    fig2.add_trace(
        go.Indicator(
            mode="number",
            value=data,
            title={'text': "지난달 총 방문객", 'font': {'size': 15, 'color': '#C5C5C5'}},
            number={'suffix': '명', 'font': {'size': 20, 'color': '#FFFFFF'}, 'valueformat': ',d'},
        )
    )
    fig2.update_layout(width=290,
                       height=100,
                       paper_bgcolor="rgba(0,0,0,0)")
    plot_div2 = plot(fig2, output_type='div')

    # 체류 시간
    df = pd.read_csv('./data/residenceTime.csv')
    data = df['data'].mean() // 60
    fig3 = go.Figure()
    fig3.add_trace(
        go.Indicator(
            mode="number",
            value=data,
            title={'text': "<b>체류 시간</b>", 'font': {'size': 15, 'color': '#C5C5C5'}},
            number={'prefix': '<b>', 'suffix': '분</b>', 'font': {'size': 20, 'family': "Arial", 'color': '#FFFFFF'},
                    'valueformat': 'd'},
        )
    )
    fig3.update_layout(width=290,
                       height=100,
                       paper_bgcolor="rgba(0,0,0,0)")
    plot_div3 = plot(fig3, output_type='div')

    # 어제 재방문객
    df = pd.read_csv('./data/revisitPerDay.csv')
    data = df['data'].sum()
    fig4 = go.Figure()
    fig4.add_trace(
        go.Indicator(
            mode="number",
            value=data,
            title={'text': "어제 재방문객", 'font': {'size': 15, 'color': '#C5C5C5'}},
            number={'suffix': '명', 'font': {'size': 20, 'color': '#FFFFFF'}, 'valueformat': ',d'},
        )
    )
    fig4.update_layout(width=290,
                       height=100,
                       paper_bgcolor="rgba(0,0,0,0)")
    plot_div4 = plot(fig4, output_type='div')

    # 지역별 일일방문객
    df = pd.read_csv('./data/zoneVisitorDay.csv')
    zoneDay = go.Figure()
    y = df.columns[1:-1]
    x = df.iloc[-1][1:-1]
    colors = ['#9515FF', '#8EE600', 'lightgray', '#0486DE', '#FB195A', '#FA9F1A']  # 바 색상변경
    # colors[4] = 'crimson'
    zoneDay.add_trace(
        go.Bar(
            y=y,
            x=x,
            text=y,
            orientation='h',
            marker_color=colors,
        )
    )
    zoneDay.update_layout(width=540,
                          height=540,
                          xaxis=dict(autorange=True, zeroline=False),  # 그래프의 그리드와 영점선 삭제
                          yaxis=dict(visible=False),
                          margin=dict(l=0, r=0, t=0, b=0),
                          paper_bgcolor="#001B50",
                          plot_bgcolor="rgba(0,0,0,0)",  # 그래프 배경 투명색
                          autosize=True,
                          font=dict(color="#ffffff")  # 그래프 폰트 색상 변경
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
    # 오늘 요일구하기(0-월 6-일)
    weektoday = datetime.today().weekday()

    # y = df_lastw.sum(axis=1)
    y = []
    # 마지막행이 오늘 날짜라고 생각
    for i in range(-8 - weektoday, -weektoday):  # 지난주 요일별로 부안 전체 방문자수 더해서 'y'리스트에 넣기
        y.append(sum(df_lastw.iloc[i][1:7]))

    x = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

    fig_w = go.Figure()
    fig_w.add_trace(
        go.Scatter(
            x=x,
            y=y,
            line=dict(color='#FA9F1A'),
            mode='markers + lines'))

    fig_w.update_layout(width=500,
                        height=600,
                        margin=dict(l=0, r=0, t=20, b=0),
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
    df_visitor = df_visitor.iloc[-1]
    fig_pie = go.Figure()
    fig_pie.add_trace(
        go.Pie(labels=df_visitor.index[1:-1],
               values=df_visitor,
               textinfo='percent',
               insidetextorientation='tangential',
               hole=0.4)
    )
    fig_pie.update_layout(width=500,  # 원형그래프가 상자 안에 들어 올 수 있게 크기 조정
                          height=500,
                          annotations=[dict(text='부안', font_size=20, showarrow=False)],
                          margin=dict(l=0, r=0, t=0, b=0),
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
    colors = ['#9515FF', '#8EE600', 'lightgray', '#0486DE', '#FB195A', '#FA9F1A']
    # colors[4] = 'crimson'
    fig_lastWeek.add_trace(
        go.Bar(
            y=y,
            x=x,
            text=y,
            # orientation='h',
            marker_color=colors
        )
    )
    fig_lastWeek.update_layout(width=500,
                               height=600,
                               xaxis=dict(autorange=True),
                               yaxis=dict(visible=True),
                               margin=dict(l=0, r=0, t=20, b=0),
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

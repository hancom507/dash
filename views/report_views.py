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

def report(request):
    startDate = request.POST.get('startDate')  # 시작 날짜
    endDate = request.POST.get('endDate')  # 끝나는 날짜
    regionValue = request.POST.getlist('region[]')  # report.html에서 'name =region[]' 인 값 들고옴
    chk_data = request.POST.get('chk_data')  # 데이터 선택 값
    now = datetime.now()  # 현재시간 불러오기

    #실시간 방문객
    if chk_data == '실시간방문객':
        df = pd.read_csv('./data/zoneVisitor.csv')
        fighour = go.Figure()
        df['TIME'] = pd.to_datetime(df['TIME'], errors='coerce')
        hour = df.query("TIME >= '2021-08-5 00:00' and TIME <= '2021-08-5 23:59'")
        region = hour[regionValue]  # 선택한 지역들과 'TIME' 컬럼으로 데이터 프레임 생성
        x = region.columns
        fighour.add_trace(
            go.Bar(
                x=x, # 지역이름
                y=region[regionValue].sum(axis=0), # 한 시간 이동한 인구수
            )
        )
        fighour.update_layout(
            height=540,
            xaxis=dict(autorange=True, zeroline=False),  # 그래프의 그리드와 영점선 삭제
            yaxis=dict(visible=True),
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="#001B50",
            plot_bgcolor="rgba(0,0,0,0)",  # 그래프 배경 투명색
            autosize=True,
            font=dict(color="#ffffff")  # 그래프 폰트 색상 변경
        )
        plot_chart = plot(fighour, output_type='div')

    #날짜별, 지역별 방문 그래프
    elif chk_data == '지역별방문객':
        regionValue.append('TIME') # regionValue리스트에 'TIME' 요소추가
        df = pd.read_csv('./data/zoneVisitorDay.csv')
        df['TIME'] = pd.to_datetime(df['TIME'], errors='coerce')
        figWeek = go.Figure()
        if startDate == None: #날짜 공백시
            week = df.query("'2021-08-22' <= TIME <= '2021-08-25'")  # 임시로 날짜기간 정해서 데이터 프레임 생성
        else:
            week = df.query("@startDate <= TIME <= @endDate") # 기간선택한 날짜로만 데이터 프레임 생성
        region = week[regionValue] # 선택한 지역들과 'TIME' 컬럼으로 데이터 프레임 생성
        x = region.columns[0:-1] # TIME 컬럼 빼고 지역들만 선택
        trace = []
        n = 0
        for i in region['TIME']: # 선택한 시간 만큼 그래프를 보여줌
            trace.append(go.Bar(
                x=x,
                y=week.iloc[n][1:-2],
                name=str(i)[0:10],
                text=str(i)[8:10],
            ))
            n = n + 1

        data = trace
        layout = go.Layout()
        figWeek = go.Figure(data, layout)
        figWeek.update_layout(
                              height=540,
                              xaxis=dict(autorange=True,zeroline=False),#그래프의 그리드와 영점선 삭제
                              yaxis=dict(visible=True),
                              margin=dict(l=0,r=0,t=0,b=0),
                              paper_bgcolor="#001B50",
                              plot_bgcolor="rgba(0,0,0,0)",#그래프 배경 투명색
                              autosize=True,
                              font=dict(color="#ffffff") #그래프 폰트 색상 변경
        )

        plot_chart = plot(figWeek, output_type='div')


    # 전체 방문객
    elif chk_data == '전체방문객':
        df = pd.read_csv('./data/zoneVisitorDay.csv')
        df['TIME'] = pd.to_datetime(df['TIME'], errors='coerce')
        figMonth = go.Figure()
        month = df.query("@startDate <= TIME <= @endDate")
        figMonth.add_trace(
            go.Bar(
                x=month['TIME'].dt.day,
                y=month[regionValue].sum(axis=1),
                text=month['TIME'].dt.day,
            )
        )
        figMonth.update_layout(
            height=540,
            xaxis=dict(autorange=True, zeroline=False),  # 그래프의 그리드와 영점선 삭제
            yaxis=dict(visible=True),
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="#001B50",
            plot_bgcolor="rgba(0,0,0,0)",  # 그래프 배경 투명색
            autosize=True,
            font=dict(color="#ffffff")  # 그래프 폰트 색상 변경
        )
        plot_chart = plot(figMonth, output_type='div')

    elif chk_data == '환경센서데이터':
        plot_chart = ''

    else:
        plot_chart = ''


    rgv = print(now) # report.html 에서 값 잘 불어오는지 확인 cmd창에서 확인 할 수 있음

    return render(request, 'dash/report.html', context={'plot_chart': plot_chart,
                                                       'rgv': rgv,
                                                       }
                  )


import requests
import pandas as pd

#devLoc = "http://restapi.toysmythiot.com:8080/v1/DaeguDalseong/DeviceInfo"
devOnOff = "http://restapi.toysmythiot.com:8080/v1/BuanSmartTown/DeviceStatus"
floatPopPerHour = "http://restapi.toysmythiot.com:8080/v1/BuanSmartTown/DeviceCountHourly"
floatPopPerDay = "http://restapi.toysmythiot.com:8080/v1/BuanSmartTown/DeviceCountDay"
revisitPerDay = "http://restapi.toysmythiot.com:8080/v1/BuanSmartTown/DeviceCountRevisit"
senseDataPerHour = "http://restapi.toysmythiot.com:8080/v1/BuanSmartTown/SensorDataHourly"
residenceTime = "http://restapi.toysmythiot.com:8080/v1/BuanSmartTown/DeviceResidenceTime"
#pdf 문서에서 복사해서 하면 안됨.
countMonth = "http://restapi.toysmythiot.com/v1/BuanSmartTown/DeviceCountMonthly"

def creatData():
    response = requests.get(devOnOff)
    data = response.json()
    df = pd.DataFrame(data)
    df.to_csv("../data/devOnOff.csv", encoding='utf-8-sig')

    response = requests.get(floatPopPerHour)
    data = response.json()
    df = pd.DataFrame(data)
    df.to_csv("../data/floatPopPerHour.csv", encoding='utf-8-sig')

    response = requests.get(floatPopPerDay)
    data = response.json()
    df = pd.DataFrame(data)
    #df.to_csv("../data/floatPopPerDay.csv", encoding='euc-kr',mode='a')
    df.to_csv("../data/floatPopPerDay.csv", encoding='utf-8-sig')

    response = requests.get(revisitPerDay)
    data = response.json()
    df = pd.DataFrame(data)
    df.to_csv("../data/revisitPerDay.csv", encoding='utf-8-sig')

    response = requests.get(senseDataPerHour)
    data = response.json()
    df = pd.DataFrame(data)
    df.to_csv("../data/senseDataPerHour.csv", encoding='utf-8-sig',index = False)

    response = requests.get(residenceTime)
    data = response.json()
    df = pd.DataFrame(data)
    df.to_csv("../data/residenceTime.csv", encoding='utf-8-sig')

    response = requests.get(countMonth)
    data = response.json()
    df = pd.DataFrame(data)
    df.to_csv("../data/countMonth.csv", encoding='utf-8-sig')


if __name__ == "__main__":
    creatData()
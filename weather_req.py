import requests
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import datetime
from datetime import timedelta
import settings
import json
import threading
from dic import dict
settings.init()


appid = '8448f8c04f64c01bd0ad50c135bd90ba'


class SimplePopup(Popup):
    def __init__(self, **kwargs):
        super(SimplePopup, self).__init__(**kwargs)
        self.size_hint =(None, None)
        self.size = (400, 300)


def error_popup(error):
    pops = SimplePopup()
    pops.title = 'Error'
    set_text_input=Label (text = error)
    pops.add_widget(set_text_input)
    pops.open()

def get_wind_direction(deg):
    l_rus = ['С ', 'СВ', ' В', 'ЮВ', 'Ю ', 'ЮЗ', ' З', 'СЗ']
    l_eng = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    for i in range(0, 8):
        step = 45.
        min = i*step - 45/2.
        max = i*step + 45/2.
        if i == 0 and deg > 360-45/2.:
            deg = deg - 360
        if deg >= min and deg <= max:
            if settings.language == 'English':
                l = l_eng
            elif settings.language == 'Russian':
                l = l_rus
            else:
                l = l_eng
            res = l[i]
            break
    return res

def lang_select():
    if settings.language == 'English':
        return 'en'
    elif settings.language == 'Russian':
        return 'ru'

# Проверка наличия в базе информации о нужном населенном пункте
def get_city_id(s_city_name):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                     params={'q': s_city_name, 'type': 'like', 'units': 'metric', 'lang': lang_select(), 'APPID': appid}, verify=False, timeout=5)
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        print("city:", cities)
        city_id = data['list'][0]['id']
        print('city_id=', city_id)
    except Exception as e:
        error_popup('Wrong City')
        return '0000'
    assert isinstance(city_id, int)
    return city_id

global request

request = {'weather': 0, 'forecast': 0}

# Запрос текущей погоды
def request_current_weather(city_id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'id': city_id, 'units': 'metric', 'lang': lang_select(), 'APPID': appid},verify=False, timeout=5)
        data = res.json()
        #return json.dumps(data)
        request['weather'] = json.dumps(data)
        print('выполнение везер')
    except Exception as e:
        print("Exception (weather):", e)
        error_popup('No Internet')
        #return '0000'
        request['weather'] = '0000'


# Прогноз
def request_forecast(city_id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': lang_select(), 'APPID': appid}, verify=False, timeout=5)
        data = res.json()
        #return json.dumps(data)
        request['forecast'] = json.dumps(data)
        print ('выполнение форкаст')
    except Exception as e:
        print("Exception (forecast):", e)
        error_popup('No Internet')
        #return '0000'
        request['forecast'] = '0000'


def parcing_current_weather(data):

    data = json.loads(data)
    wind = '{0:2.0f}'.format(data['wind']['speed'])
    temp = data['main']['temp']
    conditions = data['weather'][0]['description']
    parcing(conditions, temp, wind)
    real_feel_temp = int(temp)+settings.factor
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    sunset = data['sys']['sunset']
    sunrise = data['sys']['sunrise']
    if data['wind']['speed']>1:
        wind_direction = get_wind_direction(data['wind']['deg'])
    else:
        wind_direction = 'None'
    current_weather = {'condition': conditions, 'temp': str(temp) +'\nReal Feel ' + str(real_feel_temp),
                       'wind': str(wind) + dict['wind_speed'][settings.ind] + str(wind_direction), 'pressure': pressure, 'humidity': humidity,
                       'sunset': sunset, 'sunrise': sunrise}
    return current_weather

def parcing_forecast(data, n, time):
    data = json.loads(data)
    forecast = 'None'
    n = int(n)
    now = datetime.datetime.now()
    for m in data['list']:
        if (m['dt_txt'])[11:16] == time and (m['dt_txt'])[8:10] == (now+timedelta(n)).strftime("%d"):
            temp = '{0:+3.0f}'.format(m['main']['temp'])
            wind = '{0:2.0f}'.format(m['wind']['speed'])
            if  m['wind']['speed']>1:
                wind_direction = get_wind_direction(m['wind']['deg'])
            else:
                wind_direction = 'None'
            conditions = m['weather'][0]['description']
            parcing (conditions, temp, wind)
            real_feel_temp = int(temp) + settings.factor
            forecast = {'condition': conditions, 'temp': str(temp) +'\nReal Feel ' + str(real_feel_temp),
                       'wind': str(wind) + " м/с " + str(wind_direction)}
    return forecast

def parcing (conditions, temp, wind):
    if -100 <= int(temp) < 10:
        settings.temp_pict = 2
    if 10 <= int(temp) < 20:
        settings.temp_pict = 1
    if 20 <= int(temp) < 45:
        settings.temp_pict = 0

    if 0 <= int(wind) < 3:
        settings.factor = settings.factor - 0
        settings.wind_pict = 0
    if 3 <= int(wind) < 6:
        settings.factor = settings.factor - 2
        settings.wind_pict = 1
    if 6 <= int(wind) < 9:
        settings.factor = settings.factor - 3
        settings.wind_pict = 2
    if 9 <= int(wind):
        settings.factor = settings.factor - 5
        settings.wind_pict = 4


    if conditions == 'ясно' or conditions == 'облачно с прояснениями' or conditions == 'clear sky':
        settings.condition = 0
    if conditions == 'пасмурно' or conditions == 'переменная облачность' or conditions == 'облачно' or conditions == 'небольшая облачность'\
            or conditions == 'туман' or conditions == 'плотный туман' or conditions == 'few clouds' or conditions == 'broken clouds'\
            or conditions == 'scattered clouds' or conditions == 'overcast clouds':
        settings.condition = 1
        settings.factor = settings.factor - 1
    if conditions == 'дождь' or conditions == 'легкий дождь' or conditions == 'light rain' or conditions == 'rain':
        settings.condition = 2
        settings.factor = settings.factor - 2
    if conditions == 'небольшой дождь' or conditions == 'небольшой проливной дождь' or conditions == 'heavy rain':
        settings.condition = 3
        settings.factor = settings.factor - 2
    if conditions == 'снег' or conditions == 'snow':
        settings.condition = 5
        settings.factor = settings.factor - 2






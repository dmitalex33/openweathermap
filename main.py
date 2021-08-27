from weather_req import request_forecast, request_current_weather, get_city_id,parcing_current_weather, parcing_forecast
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import SlideTransition
import settings
from kivy.lang import Builder
import gesture_box as gesture
import datetime
import time
from datetime import timedelta
import threading
from weather_req import request
from kivy.clock import Clock
from dic import dict



#settings.init()

import graphics

class Runner(gesture.GestureBox):
    pass

class SimplePopup(Popup):
    def __init__(self, **kwargs):
        super(SimplePopup, self).__init__(**kwargs)
        self.size_hint =(None, None)
        self.size = (400, 100)

class MyLayout(Screen):
   # renew_time = StringProperty('')
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)

    def thread_renew(self):
        weather_thread = threading.Thread(target=request_current_weather, args=(settings.city_id,))
        forecast_thread = threading.Thread(target=request_forecast, args=(settings.city_id,))
        weather_thread.start()
        forecast_thread.start()
        weather_thread.join()
        forecast_thread.join()
        #print('wait 3 sek')
        #time.sleep(3)

    def set_loading (self):
        #self.loading = Image(source='./widget/loading.gif', width=50)
        self.loading = Label(text = 'Loading...')
        self.add_widget(self.loading)

        print('sign setup')
        time.sleep(3)

    def remove_loading (self):
        self.loading.text = ''

    def press_renew(self):
        #self.set_loading()
        MyLayout.thread_renew(self)
        #Clock.unschedule(self.set_loading)
        #self.remove_loading()
        weather = request['weather']
        forecast = request['forecast']
        if weather == '0000' or forecast == '0000':
            pass
        else:
            conf_write('weather', weather)
            conf_write('forecast', forecast)
            now = datetime.datetime.now()
            time = now.strftime("%d.%m.%y %A %T")
            conf_write('renew_time', time)
            show_all()


    def icon (self):
        pass
        return str(settings.factor)

    def rain (self):
        return str(settings.rain)

class Forecast(Screen):

    def __init__(self, **kwargs):
        super(Forecast, self).__init__(**kwargs)



class SettingsScreen(Screen):
    settings.s_city_name
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)


    def change_city(self,new_city):
        resp = get_city_id(new_city)
        if resp == '0000':
            pass
        else:
            settings.s_city_name = new_city
            conf_write('city', new_city)
            settings.city_id = resp
            conf_write('city_id', str(resp))
            app = App.get_running_app()
            main = app.root.ids.main.ids
            zero = app.root.ids.zero.ids
            first = app.root.ids.first.ids
            second = app.root.ids.second.ids
            third = app.root.ids.third.ids
            main.l_city.text = new_city
            zero.l_city.text = new_city
            first.l_city.text = new_city
            second.l_city.text = new_city
            third.l_city.text = new_city
            MyLayout.press_renew(self)


class CustomDropDown(DropDown):

    def change_lang(self, lang):
        app = App.get_running_app()
        app.root.ids.settingsscreen.ids.lang.text = '{}'.format(lang)
        language = str(lang)
        print("lang =", lang)
        conf_write('language', language)



def conf_write(index, data):
    with open("config.txt", "r") as file:
        lines = file.readlines()
        index = lines.index("["+index+"]\n") + 1
        lines[index] = data + '\n'
    with open("config.txt", "w") as file:
        file.writelines(lines)

def conf_read(index):
    with open("config.txt", "r") as file:
        lines = file.readlines()
        index = lines.index("["+index+"]\n") + 1
        data = lines[index]
        return data

class ScreenManager(ScreenManager):
    pass

def show_all():
    settings.factor = 0
    settings.condition = settings.wind_pict = settings.temp_pict = None
    app = App.get_running_app()
    data = conf_read('weather')
    parcing = parcing_current_weather(data)
    app.root.ids.main.ids.weather.text = parcing['condition']
    app.root.ids.main.ids.temp.text = parcing['temp']
    app.root.ids.main.ids.wind.text = parcing['wind']
    app.root.ids.main.ids.rain_img.source = graphics.rain_pict()
    app.root.ids.main.ids.temp_img.source = graphics.temp_pict()
    app.root.ids.main.ids.wind_img.source = graphics.wind_pict()
    app.root.ids.main.ids.pressure.text = str(parcing['pressure']*0.75)
    app.root.ids.main.ids.humidity.text = str(parcing['humidity'])
    app.root.ids.main.ids.sunset.text = time.ctime(parcing['sunset'])[11:16]
    app.root.ids.main.ids.sunrise.text = time.ctime(parcing['sunrise'])[11:16]
    data = conf_read('forecast')
    app.root.ids.main.ids.update_time.text = renew_time_format()
    zero =app.root.ids.zero.ids
    first = app.root.ids.first.ids
    second = app.root.ids.second.ids
    third =app.root.ids.third.ids
    days = [zero, first, second, third]
    times = ['09:00', '18:00']
    now = datetime.datetime.now()
    app.root.ids.settingsscreen.ids.lang.text = settings.language

    for day in days:
        settings.factor = 0
        settings.condition = settings.wind_pict = settings.temp_pict = None
        parcing = parcing_forecast(data, days.index(day), '09:00')
        #print (parcing)
        day.rain_img.source = graphics.rain_pict()
        day.temp_img.source = graphics.temp_pict()
        day.wind_img.source = graphics.wind_pict()
        day.day.text = (now + timedelta(days.index(day))).strftime("%d.%m %A")
        if parcing == None or parcing == 'None':
            continue
        day.weather.text = parcing['condition']
        day.temp.text = parcing['temp']
        day.wind.text = parcing['wind']

    for day in days:
        settings.factor = 0
        settings.condition = settings.wind_pict = settings.temp_pict = None
        parcing = parcing_forecast(data, days.index(day), '15:00')
        #print (parcing)
        day.rain_img_d.source = graphics.rain_pict()
        day.temp_img_d.source = graphics.temp_pict()
        day.wind_img_d.source = graphics.wind_pict()
        day.day.text = (now + timedelta(days.index(day))).strftime("%d.%m %A")
        if parcing == None or parcing == 'None':
            continue
        day.weather_d.text = parcing['condition']
        day.temp_d.text = parcing['temp']
        day.wind_d.text = parcing['wind']


    for day in days:
        settings.factor = 0
        settings.condition = settings.wind_pict = settings.temp_pict = None
        parcing = parcing_forecast(data, days.index(day), '18:00')
        day.rain_img_e.source = graphics.rain_pict()
        day.temp_img_e.source = graphics.temp_pict()
        day.wind_img_e.source = graphics.wind_pict()
        if parcing == None or parcing == 'None':
            continue
        day.weather_e.text = parcing['condition']
        day.temp_e.text = parcing['temp']
        day.wind_e.text = parcing['wind']

def check_weather ():
    now = datetime.datetime.now()
    update_time = conf_read('renew_time')
    if update_time[:2] == now.strftime("%d"):
        return
    else:
        MyLayout.press_renew(MyLayout)

def renew_time_format():
    renew_time = conf_read('renew_time')
    now = time.time()
    #time.mktime(
    updated = time.mktime(time.strptime(renew_time[:-1], '%d.%m.%y %A %X'))
    difference = (now-updated)/3600

    if difference <= 0.05:
        return dict['just'][settings.ind]
    elif difference <= 2:
        return dict['less than an hour'][settings.ind]
    elif difference <= 2:
        return ''+ dict['hours ago'][settings.ind]
    elif difference <= 3:
        return '3'+ dict['hours ago'][settings.ind]
    elif difference <= 4:
        return '4'+ dict['hours ago'][settings.ind]
    elif difference <= 6:
        return '6'+ dict['hours ago'][settings.ind]
    elif difference <= 10:
        return '10'+ dict['hours ago'][settings.ind]
    elif difference <= 24:
        return dict['yesterday'][settings.ind]
    else:
        return dict['long ago'][settings.ind]


buildKV = Builder.load_file("BikeWeather.kv")

class BikeWeatherApp(App):
    def build(self):
        Clock.schedule_interval(lambda dt: self.update_time(), 3600)
        return Runner() #buildKV
    def on_start(self, **kwargs):
        show_all()
        check_weather()

    def update_time(self):
        app = App.get_running_app()
        app.root.ids.main.ids.update_time.text = renew_time_format()
        #app.root.ids.main.ids.update_time.text += '1'






if __name__ == '__main__':
    BikeWeatherApp().run()







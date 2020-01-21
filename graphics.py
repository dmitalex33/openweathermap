import settings
import datetime

def rain_pict():
    x = settings.condition
    if x == 0:
        pict = "./widget/images/sunny.png"  #
    elif x == 1:
        pict = "./widget/images/cloud.png"  #
    elif x == 2:
        pict = "./widget/images/rain.png"  #
    elif x == 3:
        pict = "./widget/images/havyrain.png"  #
    elif x == 4:
        pict = "./widget/images/storm.png"  #
    elif x == 5:
        pict = "./widget/images/snow.png"  #
    else:
        pict = "./widget/images/none.png"
    return pict

def temp_pict():
    x = settings.temp_pict
    if x == 0:
        pict = "./widget/images/hot.png"  #
    elif x == 1:
        pict = "./widget/images/medium.png"  #
    elif x == 2:
        pict = "./widget/images/cold.png"  #
    else:
        pict = "./widget/images/none.png"
    return pict

def wind_pict():
    x = settings.wind_pict
    if x == 1:
        pict = "./widget/images/wind1.png"  #
    elif x == 2:
        pict = "./widget/images/wind2.png"  #
    elif x == 3:
        pict = "./widget/images/wind3.png"  #
    elif x == 4:
        pict = "./widget/images/wind.png"  #
    else:
        pict = "./widget/images/none.png"
    return pict

sett = "./widget/images/settings.png"
sett_ = "./widget/images/settings_.png"
summer = "./summer.png"
morning = "./widget/timeofday/morning.png"
day = "./widget/timeofday/day.png"
evening = "./widget/timeofday/evening.png"
night = "./widget/timeofday/night.png"

def screen_img():
    now = datetime.datetime.now()
    if 11<now.hour<= 18:
        screen_image = "./widget/screen/day_screen.png"
    elif 6 <now.hour<= 11:
        screen_image = "./widget/screen/morning_screen.png"
    elif 18 <now.hour<= 22:
        screen_image = "./widget/screen/evening_screen.png"
    else:
        screen_image = "./widget/screen/night_screen.png"
    return screen_image

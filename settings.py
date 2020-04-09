#from main import conf_read


def init():
    global factor
    factor = 0

    global condition
    condition = None

    global temp_pict
    temp_pict = None

    global wind_pict
    wind_pict = None

    global s_city_name

    #s_city_name = conf_read('city')

    with open("config.txt", "r") as file:
        lines = file.readlines()
        index = lines.index("[city]\n") + 1
        s_city_name = lines[index]

    global city_id
    #city_id = conf_read(city_id)[:6]

    with open("config.txt", "r") as file:
        lines = file.readlines()
        index = lines.index("[city_id]\n") + 1
        city_id = lines[index][:6]

    global renew_time

    with open("config.txt", "r") as file:
        lines = file.readlines()
        index = lines.index("[renew_time]\n") + 1
        renew_time = lines[index]

    global language

    with open("config.txt", "r") as file:
        lines = file.readlines()
        index = lines.index("[language]\n") + 1
        language = lines[index][:-1]

    global ind

    if language == 'Russian':
        ind = 1
    elif language == 'English':
        ind = 0
    else:
        ind = 0
import json
import requests

from datetime import datetime, timedelta, date


class WeatherForecast:
    def __init__(self, path_to_file):
        self.file = path_to_file
        self.data = self.load_data_from_file()
        self.locations = self.data.keys()
        self.dates = set(date for location in self.data.values() for date in location)
        self.index = 0

    def load_data_from_file(self):
        with open(self.file) as file:
            return json.loads(file.read())

    def save_data_to_file(self):
        with open(self.file, mode="w") as file:
            file.write(json.dumps(self.data))

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.dates):
            raise StopIteration
        day = list(self.dates)[self.index]
        self.index += 1
        return day

    def __getitem__(self, item):
        city, date = item
        print(city)
        print(date)
        selected_city = self.data.get(city)
        if selected_city:
            for city_date, info in selected_city.items():
                if city_date == date:
                    return info
        return None

    def __setitem__(self, key, value):
        city, day = key
        city_data = self.data.get("city")
        if city_data:
            self.data[city][day] = value
        else:
            self.data[city] = {}
            self.data[city][day] = value

    def items(self):
        for city in self.data:
            for day, result in self.data[city].items():
                yield (day, result)

    def change_city_to_latitude_and_longitude(self, address):
        city_URL = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1"
        r = requests.get(url=city_URL)
        if r.status_code == 200:
            city_data = r.json()
            if len(city_data) != 0:
                print(f"Request passed, status code is {r.status_code} data is being downloaded from API :)")
                latitude = city_data[0]['lat']
                longitude = city_data[0]['lon']
                return latitude, longitude
            else:
                print("Probably there is no city like that")

        else:
            print(
                f"Unfortunately there is no city like provided or downloading failed :( status code is {r.status_code}")

    def data_validation(self, user_date):
        if user_date == '':
            present_day = datetime.today()
            tomorrow = present_day + timedelta(1)
            tomorrow = tomorrow.strftime('%Y-%m-%d')
            user_date = tomorrow
            return user_date
        else:
            try:
                date.fromisoformat(user_date)
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")
            return user_date

    def request_from_weather_api(self, latitude, longitude, user_date):
        weather_URL = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=rain&daily=rain_sum" \
                      f"&timezone=Europe%2FLondon&start_date={user_date}&end_date={user_date}"

        r_2 = requests.get(url=weather_URL)
        weather_data = r_2.json()
        if r_2.status_code == 200:

            print(f"Request passed, status code is {r_2.status_code} data is being downloaded from API :)")
        else:
            print(
                f"Unfortunately there is no city like provided or downloading failed :( status code is {r_2.status_code}")
        rain_sum = (weather_data['daily']['rain_sum'][0])
        if rain_sum > 0.0:
            rain = "It's a rainy day"
            return rain
        elif rain_sum == 0.0:
            rain = "It's not a rainy day"
            return rain
        else:
            print("Unknown")

    def get_data_from_file(self, data, address, user_date):
        if address in data.items():
            for key, value in data[address].items():
                if key == user_date:
                    return value
        else:
            return None

    def upload_new_city_to_data(self, city, day, result):
        self.data[city] = {day: result}




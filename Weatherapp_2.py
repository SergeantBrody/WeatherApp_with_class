from weather_forecast import WeatherForecast

print("Welcome to the app which will let you check if certain day is rainy day or not")

weather_forecasting = WeatherForecast(path_to_file="weather_data.json")


address = input("Provide the city in order to check the weather: ")
user_date = input("Provide the date in order to check the weather: ")
city_in_file = weather_forecasting.get_data_from_file(weather_forecasting.data, address, user_date)
if city_in_file:
    print(city_in_file)
    print("Downloaded data from file")
else:
    latitude, longitude = weather_forecasting.change_city_to_latitude_and_longitude(address)
    valid_date = weather_forecasting.data_validation(user_date)
    if_rain = weather_forecasting.request_from_weather_api(latitude, longitude, valid_date)
    print(if_rain)
    print("Above data has been downloaded from API ")
    weather_forecasting.upload_new_city_to_data(city=address, day=valid_date, result=if_rain)
    weather_forecasting.save_data_to_file()


print(weather_forecasting.data)
print(weather_forecasting[("Bydgoszcz", "2024-04-04")])  # get_item
weather_forecasting[("Krakow", "2024-04-06")] = "It's not a rainy day"  # set_item
weather_forecasting.save_data_to_file()
generator = weather_forecasting.items()
print(generator.__next__())
print(generator.__next__())
print(generator.__next__())
print(generator.__next__())
for date in weather_forecasting:
    print(date)


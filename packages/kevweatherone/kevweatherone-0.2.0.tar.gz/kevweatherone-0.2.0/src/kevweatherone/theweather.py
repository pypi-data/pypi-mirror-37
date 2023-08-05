from weather import Weather, Unit


def get_weather_by_location(location):
    weather = Weather(unit=Unit.FAHRENHEIT)
    location = weather.lookup_by_location(location)
    condition = location.condition
    # print(condition.text)
    return condition.text





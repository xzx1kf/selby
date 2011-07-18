class Horse(object):
    """A horse"""

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    name = property(get_name, set_name)

    def get_weight(self):
        return self.__weight

    def set_weight(self, weight):
        self.__weight = weight

    weight = property(get_weight, set_weight)

    def get_last_ran(self):
        return self.__last_ran

    def set_last_ran(self, days):
        self.__last_ran = days

    last_ran = property(get_last_ran, set_last_ran)

    def get_forecast_odds(self):
        return self.__fodds

    def set_forecast_odds(self, odds):
        self.__fodds = odds

    forecast_odds = property(get_forecast_odds, set_forecast_odds)

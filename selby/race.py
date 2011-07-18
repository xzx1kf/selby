class Race(object):
    """A race"""

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    name = property(get_name, set_name)

    def get_time(self):
        return self.__time

    def set_time(self, time):
        self.__time = time

    time = property(get_time, set_time)

    def get_distance(self):
        return self.__distance

    def set_distance(self, distance):
        self.__distance = distance

    distance = property(get_distance, set_distance)

    def get_runners(self):
        return self.__runners

    def set_runners(self, runners):
        self.__runners = runners

    runners = property(get_runners, set_runners)
    
    def get_horses(self):
        return self.__horses

    def set_horses(self, horses):
        self.__horses = horses

    horses = property(get_horses, set_horses)


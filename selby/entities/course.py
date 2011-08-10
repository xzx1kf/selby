class Course(object):
    """A course"""

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    name = property(get_name, set_name)
   
    def get_going(self):
        return self.__going

    def set_going(self, going):
        self.__going = going

    going = property(get_going, set_going)

    def get_races(self):
        return self.__races

    def set_races(self, races):
        self.__races = races

    races = property(get_races, set_races)


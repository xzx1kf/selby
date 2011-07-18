from BeautifulSoup import BeautifulSoup
from selby.horse import Horse
from selby.race import Race
from selby.course import Course
import htmllib
import urllib2
import pickle


class RacingPostParser(object):

    def read_file(self, filename):
        """Reads a file as a data source."""
        f = open(filename)
        data = f.read()
        f.close()

        return data

    def read_url(self, url):
        response = urllib2.urlopen(url)
        html = response.read()
        response.close()

        return html

    def parse_todays_races(self, html):
        """Parse todays races."""
        soup = self.strip_races_from(html)

        rpcp = RacingPostCourseParser()
        courses = rpcp.parse_courses(soup)

        return courses
    
    def strip_races_from(self, html):
        """Strips the race information from todays card."""
        soup = BeautifulSoup(html)
        html = soup.find('div', {'id' : 'races_result'})
        return html

    def strip_races_from_course(self, course_soup):
        soup = course_soup.find('table', {'class' : 'cardsGrid'})

        rprp = RacingPostRaceParser()
        races = []

        for i in range(len(soup('tr'))):
            race_soup = soup('tr')[i]

            race = rprp.parse_race(race_soup)
            races.append(race)

            #print race.title

            # CHECK THAT THE DISTANCE IS OK 
            distance_is_within_limits = self.is_distance_within_limits(race.distance)
            #print "Distance within limits? " + str(distance_is_within_limits)

            # CHECK THAT THE RACE IS A HANDICAP AND A FLAT RACE
            is_a_flat_race = self.is_a_flat_race(race.title)
            #print "Is a flat race? " + str(is_a_flat_race)

            # CHECK THAT THE NUMBER OF RUNNERS IS BETWEEN 11 AND 16
            is_number_of_runners_within_limits = self.is_number_of_runners_within_limits(race.runners)
            #print "Is the number of runners between 11 and 16? " + str(is_number_of_runners_within_limits)

            if distance_is_within_limits and is_a_flat_race and is_number_of_runners_within_limits:
                # CHECK THAT THE BETTING FORECAST FOR EACH OF THE HORSES IN THE RACE
                for horse in race.horses:
                    pass
                    #print "[" + horse.weight + "] " + horse.name + " {" + str(horse.last_ran) + "} BF: " + horse.forecast_odds

        return races

    def unescape(self, string):
        """Remove the special character from html."""
        p = htmllib.HTMLParser(None)
        p.save_bgn()
        p.feed(string)
        return str(p.save_end())

    def is_distance_within_limits(self, distance):
        """Checks that the distance is under 1m2f."""
        if distance[0] == 0:
            return True
        elif distance[0] < 2:
            if distance[1] < 2:
                return True
            else:
                return False
        else:
            return False

    def is_a_flat_race(self, race_title):
        if "Hurdle" in race_title or "Chase" in race_title or "Handicap" not in race_title:
            return False
        else:
            return True
            
    def is_number_of_runners_within_limits(self, number_of_runners):
        """The number of runners must be between 11 and 16(inclusive)."""
        if number_of_runners >= 11 and number_of_runners <= 16:
            return True
        else:
            return False


    def check_betting_forecast(self, soup):
        url = soup('a')[0]['href']
        html = self.read_url(url)
        #html = self.read_file('../static/race_card.html')

        card_soup = BeautifulSoup(html)

        # Check that its not in the top 5 weights
        horses = self.check_weight(card_soup)

        card_soup = card_soup.find('div', {'class' : 'info'})
        
        qualifying_horses = []
        
        # Check the first
        odds = (card_soup.contents[2].contents[0]).strip(', ')
        horse = card_soup.contents[2].contents[1].contents[0]
        horse = horse.lstrip().rstrip().upper()
        horse = horse.replace('&ACUTE;', '')
        #print horse + ' - check'

        if horse in horses.keys():
            if self.check_odds(odds):
                details = odds, horse, horses[horse][1]
                qualifying_horses.append(details)

        try:
            # Check the rest
            for x in range(3, len(card_soup.contents)-1, 2):
                odds = (card_soup.contents[x]).strip(', ')
                horse = card_soup.contents[x+1].contents[0]
                horse = horse.lstrip().rstrip().upper()
                horse = horse.replace('&ACUTE;', '')
                #print horse + ' - check'

                if horse in horses.keys():
                    # Check the odds are in range. 
                    if self.check_odds(odds):
                        details = odds, horse, horses[horse][1]
                        qualifying_horses.append(details)
        except:
            # Check the first
            print '########## EXCEPTION ###########'
            odds = (card_soup.contents[4].contents[0]).strip(', ')
            horse = card_soup.contents[4].contents[1].contents[0]
            horse = horse.lstrip().rstrip().upper()
            horse = horse.replace('&ACUTE;', '')
            #print horse + ' - check'

            if horse in horses.keys():
                if self.check_odds(odds):
                    details = odds, horse, horses[horse][1]
                    qualifying_horses.append(details)

        return qualifying_horses

    def check_odds(self, odds):
        """docstring for check_odds"""
        i = odds.find('/')
        x = float(odds[:i])
        y = float(odds[i+1:])
        z = x/y

        if z >= 4 and z <= 7.5:
            return True

        return False

    def check_weight(self, soup):
        """docstring for check_weight"""

        card_item = soup('div', {'class' : 'cardItem'})

        horses = {}

        for i in range(len(card_item)):
            card_soup = card_item[i]

            weight_position = card_soup.find('td', {'class' : 't'})
            horse = card_soup.find('td', {'class' : 'h'})
            days = card_soup.find('div', {'class' : 'horseShortInfo'})

            weight_position = weight_position.contents[1].contents[0]
            horse = horse.contents[1].contents[1].contents[0].contents[0]
            horse = horse.replace('&acute;', '')
            days = (days.contents[len(days.contents)-1]).strip()
            days = days.split(' ')
            days = days[0]

            if int(weight_position) > 5:
                if int(days) > 7:
                    horses[horse] = weight_position, days

            #print weight_position + ' ' + horse + ' : ' + days

        return horses


class RacingPostCourseParser(object):
    """Parses the course information."""

    def parse_courses(self, course_soup):

        courses = []

        for i in range(len(course_soup('div', {'class' : 'crBlock'}))):
            course_item = course_soup('div', {'class' : 'crBlock'})[i]

            course = Course()

            course.name = self.parse_name(course_item)
            course.going = self.parse_going(course_item)
            course.races = self.parse_races(course_item)

            if len(course.races) > 0:
                courses.append(course)

        return courses

    def parse_name(self, course_soup):
        name = course_soup('td', {'class' : 'meeting'})
        soup = BeautifulSoup(str(name))
        return str(soup.find('a').contents[0])

    def parse_going(self, race_soup):
        going = str(race_soup.contents[5].contents[2])
        i = going.find('(')
        return going[2:i-1]

    def parse_races(self, course_soup):
        soup = course_soup.find('table', {'class' : 'cardsGrid'})
        
        rprp = RacingPostRaceParser()
        races = []

        for i in range(len(soup('tr'))):
            race_soup = soup('tr')[i]

            try:
                race = rprp.parse_race(race_soup)
                races.append(race)
            except:
                pass
        
        return races 


class RacingPostRaceParser(object):
    """Parses the race information."""

    def parse_race(self, race_soup):
        race = Race()

        race.title = self.parse_title(race_soup) 
        race.time = self.parse_time(race_soup)
        race.distance = self.parse_distance(race.title)
        race.url = self.parse_race_url(race_soup)
        race.card_soup = self.read_url(race.url)

        rphp = RacingPostHorseParser()
        race.horses = rphp.parse_horses(race.card_soup)

        race.runners = int(len(race.horses))

        return race

    def parse_title(self, race_soup):
        return str(race_soup.contents[3].contents[1].contents[0])

    def parse_time(self, race_soup):
        return race_soup.contents[1].contents[1].contents[0]

    def parse_race_url(self, race_soup):
        return race_soup('a')[0]['href']

    def parse_distance(self, title):
        i = title.rfind(' ')
        distance = title[i:]

        mIndex = distance.find('m')
        fIndex = distance.find('f')
        yIndex = distance.find('y')

        miles = 0
        furlongs = 0
        yards = 0

        if mIndex is not -1:
            miles = distance[mIndex-1:mIndex]

        if fIndex is not -1:
            furlongs = distance[fIndex-1:fIndex]

        if yIndex is not -1:
            if fIndex is -1:
                yards = distance[mIndex+1:yIndex]
            else:
                yards = distance[fIndex+1:yIndex]

        return int(miles), int(furlongs), int(yards)

    def read_url(self, url):
        response = urllib2.urlopen(url)
        html = response.read()
        response.close()
        return html


class RacingPostHorseParser(object):
    """Parses the horse information given the race card soup."""

    def parse_horses(self, race_card_soup):
        """docstring for parse_horses"""

        horses_list = self.parse_betting_forecast(race_card_soup)

        race_card_soup = BeautifulSoup(race_card_soup)
        card_item = race_card_soup('div', {'class': 'cardItem'})

        horses = []

        for i in range(len(card_item)):
            horse = Horse()
            card_item_soup = card_item[i]

            horse.weight = self.parse_weight(card_item_soup)
            horse.name = self.parse_name(card_item_soup)
            horse.last_ran = self.parse_days_since_last_run(card_item_soup)

            try:
                horse.forecast_odds = horses_list[horse.name]
            except:
                horse.forecast_odds = "NONE"
                pass

            horses.append(horse)

        return horses

    def parse_name(self, card_item_soup):
        name = card_item_soup.find('td', {'class' : 'h'})
        name = name.contents[1].contents[1].contents[0].contents[0]
        name = name.replace('&acute;', '')
        return name

    def parse_weight(self, card_item_soup):
        weight = card_item_soup.find('td', {'class' : 't'})
        weight = weight.contents[1].contents[0]
        return weight

    def parse_days_since_last_run(self, card_item_soup):
        days = card_item_soup.find('div', {'class' : 'horseShortInfo'})
        days = (days.contents[len(days.contents)-1]).strip()
        days = days.split(' ')
        days = days[0]
        try:
            return int(days)
        except: 
            return 0

    def parse_betting_forecast(self, race_card_soup):
        race_card_soup = BeautifulSoup(race_card_soup)
        forecast = race_card_soup.find('div', {'class' : 'info'})

        horses = {}

        odds = (forecast.contents[2].contents[0]).strip(', ')
        horse = forecast.contents[2].contents[1].contents[0]
        horse = horse.lstrip().rstrip().upper()
        horse = horse.replace('&ACUTE;', '')

        horses[str(horse)] = odds

        for x in range(3, len(forecast.contents)-1, 2):
            odds = (forecast.contents[x]).strip(', ')
            horse = forecast.contents[x+1].contents[0]
            horse = horse.lstrip().rstrip().upper()
            horse = horse.replace('&ACUTE;', '')

            horses[str(horse)] = odds

        return horses

        



if __name__ == '__main__':
    rpp = RacingPostParser()
    #data = rpp.read_file('../static/cards.html')
    #data = rpp.read_url('http://www.racingpost.com/horses2/cards/home.sd')
    #courses = rpp.parse_todays_races(data)

    #f = open("temp.obj", 'w')
    #pickle.dump(courses, f)
    #f.close()

    f = open("temp.obj", 'r')
    courses = pickle.load(f)
    f.close()

    for course in courses:
        if len(course.races) > 0:
            print course.name + " - Going: " + course.going

        for race in course.races:
            if rpp.is_distance_within_limits(race.distance):
                if rpp.is_a_flat_race(race.title):
                    if rpp.is_number_of_runners_within_limits(race.runners):
                        print "\t" + race.time + " : " + race.title
                        for horse in race.horses:
                            print "\t\t" + horse.weight + " : " + horse.name
                        print "\n"

        print "\n\r"



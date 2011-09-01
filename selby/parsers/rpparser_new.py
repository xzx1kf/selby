from BeautifulSoup import BeautifulSoup
from selby.entities.horse import Horse
from selby.entities.race import Race
from selby.entities.course import Course
import urllib2

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
        soup = self.parse_course_and_race_information(html)

        rpcp = RacingPostCourseParser()
        courses = rpcp.parse_courses(soup)

        return courses
    
    def parse_course_and_race_information(self, html):
        """Strips the course and race information from todays card."""
        soup = BeautifulSoup(html)
        html = soup.find('div', {'id' : 'races_list'})
        return html 


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
        
        """
        if race.title.find("FR") >= 0:
            print "raising exception"
            raise None

        print race.title
        """

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
        url = "http://www.racingpost.com" + url
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
        card_item = race_card_soup('tr', {'class': 'cr'})

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
                horse.forecast_odds = "50/2"
                pass

            horses.append(horse)

        return horses

    def parse_name(self, card_item_soup):
        name = card_item_soup('td')[2].contents[1].contents[0].contents[0]
        name = name.replace('&acute;', '')
        return name

    def parse_weight(self, card_item_soup):
        weight = card_item_soup.find('td', {'class' : 't'})
	weight = weight.contents[1].contents[0]
        return weight

    def parse_days_since_last_run(self, card_item_soup):
        days = card_item_soup.find('div', {'class' : 'horseShortInfo'})
	days = days.contents[-2].contents[0]
        try:
            return int(days)
        except: 
            return 0

    def parse_betting_forecast(self, race_card_soup):
		race_card_soup = BeautifulSoup(race_card_soup)
		forecast = race_card_soup.find('div', {'class' : 'info'})

		horses = {}

		odds = (forecast.contents[1].contents[1].contents[0]).strip()
		horse = forecast('a')[0].contents[0]
		horse = horse.lstrip().rstrip().upper()
		horse = horse.replace('&ACUTE;', '')

		horses[str(horse)] = odds

		number_of_horses = len(forecast('a'))

		for x in range(3, number_of_horses * 2, 2):
			horse = forecast.contents[1].contents[x].contents[0]
			odds = (forecast.contents[1].contents[x-1]).strip(', ')
			horse = horse.lstrip().rstrip().upper()
			horse = horse.replace('&ACUTE;', '')

			horses[str(horse)] = odds

		return horses

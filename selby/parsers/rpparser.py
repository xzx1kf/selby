from BeautifulSoup import BeautifulSoup
import htmllib
import urllib2


class RacingPostParser(object):

    def read_file(self, filename):
        """Reads a file as a data source."""
        f = open(filename)
        data = f.read()
        f.close()

        return data

    def parse_todays_races(self, html):
        """Parse todays races."""
        soup = self.strip_races_from(html)
        soup = self.strip_course_from(soup)
    
    def strip_races_from(self, html):
        """Strips the race information from todays card."""
        soup = BeautifulSoup(html)
        html = soup.find('div', {'id' : 'races_result'})
        return html

    def strip_course_from(self, soup):

        for i in range(len(soup('div', {'class' : 'crBlock'}))):
            html = soup('div', {'class' : 'crBlock'})[i]
        
            # Get race name.
            title = html('td', {'class' : 'meeting'})
            self.strip_course_name_from(title)

            # Get the going information.
            self.strip_going_from(html.contents[5])

            # Get the race information at this course.
            self.strip_races_from_course(html)

            print "\n\r==================================================\n\r"

    def strip_course_name_from(self, soup):
        soup = BeautifulSoup(str(soup))
        print 'Course:\t' + str(soup.find('a').contents[0])
        
    def strip_going_from(self, soup):
        going = str(soup.contents[2])
        x = going.find('(')
        going = going[2:x-1]
        print 'Going:\t' + going + '\n\r'

    def strip_races_from_course(self, course_soup):
        soup = course_soup.find('table', {'class' : 'cardsGrid'})

        count = 0
        
        for i in range(len(soup('tr'))):
            race_soup = soup('tr')[i]

            # Time
            time = race_soup.contents[1].contents[1].contents[0]

            # Title
            title = self.unescape(str(race_soup
                                        .contents[3]
                                        .contents[1]
                                        .contents[0]))

            # Check that the distance is less than 1m2f
            distance = self.check_distance(title)


            # Filter out races that have "hurdle" or "chase" or
            # aren't a handicap.
            if "Hurdle" in title or "Chase" in title or "Handicap" not in title:
                pass
            elif distance:
                # Check the number of runners is 11-16 inclusive.
                runners = self.check_number_of_runners(race_soup)

                qualifying_horses = self.check_betting_forecast(race_soup)

                if runners >= 11 and runners <= 16:
                    print str(i+1) + ' ' + str(time) + ' ' + title + ' : ' + str(runners)

                    for details in qualifying_horses:
                        print '\t\t' + details[0] + ' - ' + details[1] + ' - ' + details[2]

                    count += 1

        if count == 0:
            print "No races qualify at this course today."


    def unescape(self, string):
        """Remove the special character from html."""
        p = htmllib.HTMLParser(None)
        p.save_bgn()
        p.feed(string)
        return str(p.save_end())

    def check_distance(self, string):
        """Checks that the distance is under 1m2f."""
        # Strip the distance from the title
        index = string.rfind(' ')
        distance = string[index:]

        m = distance.find('m')
        f = distance.find('f')

        miles = 0
        furl = 0

        if m is not -1:
            miles = distance[m-1:m]

        if f is not -1:
            furl = distance[f-1:f]

        if int(miles) >= 1:
            if int(furl) >= 2:
                return False
            elif int(miles) <= 1:
                return True
        else:
            return True

    def check_number_of_runners(self, soup):
        """Retrieve the number of runners from a race card."""
        url = soup('a')[0]['href']
        html = self.read_url(url)
        #html = self.read_file('../static/race_card.html')

        card_soup = BeautifulSoup(html)
        card_soup = card_soup.find('p', {'class' : 'raceInfo'})
        card_soup = card_soup.find('span', {'class' : 'nowrap'}).contents[0]
        index = card_soup.rfind(' ')
        runners = card_soup[index:]
        return int(runners)

    def read_url(self, url):
        response = urllib2.urlopen(url)
        html = response.read()
        response.close()

        return html

    def check_betting_forecast(self, soup):
        url = soup('a')[0]['href']
        html = self.read_url(url)
        #html = self.read_file('../static/race_card.html')

        card_soup = BeautifulSoup(html)

        # Check that its not in the top 5 weights
        horses = self.check_weight(card_soup)

        card_soup = card_soup.find('div', {'class' : 'info'})

        print card_soup.contents
        exit(0)
        
        qualifying_horses = []
        
        # Check the first
        odds = (card_soup.contents[2].contents[0]).strip(', ')
        horse = card_soup.contents[2].contents[1].contents[0]
        horse = horse.lstrip().rstrip().upper()
        horse = horse.replace('&ACUTE;', '')
        print horse + ' - check'

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
                print horse + ' - check'

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
            print horse + ' - check'

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

            if int(weight_position) > 5:
                horses[horse] = weight_position, days

            print weight_position + ' ' + horse + ' : ' + days

        return horses


if __name__ == '__main__':
    rpp = RacingPostParser()
    #data = rpp.read_file('../static/cards.html')
    data = rpp.read_url('http://www.racingpost.com/horses2/cards/home.sd')
    rpp.parse_todays_races(data)

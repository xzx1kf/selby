from selby.parsers import rpparser_new
import cPickle

def write():
	rpp = rpparser_new.RacingPostParser()
	data = rpp.read_url('http://www.racingpost.com/horses2/cards/home.sd')
	courses = rpp.parse_todays_races(data)

	f = open("temp.obj", 'w')
	cPickle.dump(courses, f)
	f.close()
	
def read():
	f = open("temp.obj", 'r')
	courses = cPickle.load(f)
	f.close()

	print "Number of courses today ---> " + str(len(courses))
	print "\n"

	for course in courses:
		if check_going(course.going) == False:
			continue
		if len(course.races) > 0:
			print course.name + " - Going: " + course.going

		for race in course.races:
			if layem(race) == False:
				continue
			else:
				print "\t" + race.time + " " + race.title + " : [" + str(race.runners) + "]"
				for horse in race.horses:
					if check_weight_and_odds(horse):
						print "\t\t" + horse.weight + "\t: " + horse.name + " ["+ str(horse.last_ran) + "] - " + horse.forecast_odds
				print "\n"
			print "\n"

def layem(race):
	if check_race_type(race.title) == False:
		return False
	if check_distance(race.distance) == False:
		return False
	if check_runners(race.runners) == False:
		return False

def check_going(going):
	if going.find("GOOD") <> -1 or going.find("STANDARD") <> -1:
		return True

	return False
	
def check_race_type(title):
	if "Hurdle" in title or "Chase" in title or "Handicap" not in title:
		return False
	else:
		return True
		
def check_distance(distance):
	miles, furlongs, yards = distance
	
	if miles > 1:
		return false
	elif miles == 1 and furlongs > 2:
		return False
	else:
		return True
		
def check_runners(runners):
	if runners >= 11 and runners <= 16:
		return True
	else:
		return False
		
def check_weight_and_odds(horse):
	if int(horse.weight) <= 5:
		return False
	else:
		if check_forecast_odds(horse.forecast_odds):
			return True
		else:
			return False
			
def check_forecast_odds(odds):
	i = odds.find('/')
	
	try:
		x = float(odds[:i])
		y = float(odds[i+1:])
		z = x/y

		if z >= 4 and z <= 7.5:
			return True
	except:
		return False
		
	return False

	
if __name__ == '__main__':
	#write()
	read()
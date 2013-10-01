import webapp2
from webapp2_extras import json
from google.appengine.ext import ndb
import logging

class Location(ndb.Model):
    loc = ndb.GeoPtProperty()
    geohash = ndb.StringProperty()
    name = ndb.StringProperty()
    address = ndb.StringProperty(repeated=True)
    notes = ndb.TextProperty()

    L1_hashsize = 0.05

    @classmethod
    def make_geohash_L1(cls, lon, lat):
	# round to nearest 0.05
	x = round(float(lat)*20, 0)/20
	y = round(float(lon)*20, 0)/20
	if x == -0.0:
	    x = 0.0
	if y == -0.0:
	    y = 0.0
	return str(x) + ":" + str(y)

    @classmethod
    def query_bbox(cls, north, east, south, west):
	# Let's not generate massive queries
	if west > east + 1 or north > south + 1:
	    return []

	squares = []
	x = west
	# generate the list of geohashes we need to find
	while x >= east:
	    y = north
	    while y >= south:
		squares.append(cls.make_geohash_L1(x, y))
		y -= cls.L1_hashsize
	    x -= cls.L1_hashsize
	result = []
	if len(squares) > 0:
	    for loc in cls.query(Location.geohash.IN(squares)):
		# The geohash might return results just outside the search area
		if loc.loc.lon <= west and loc.loc.lon >= east \
		    and loc.loc.lat <= north and loc.loc.lat >= south:
		    result.append(loc)
	return result

class LocationAPI(webapp2.RequestHandler):

    def post(self, arg):
	loc = Location()
	loc.loc = ndb.GeoPt(float(self.request.get('latitude')), float(self.request.get('longitude')))
	loc.geohash = Location.make_geohash_L1(loc.loc.lat, loc.loc.lon)
	loc.name = self.request.get('name')
	loc.address = [self.request.get('address1'),
		       self.request.get('address2'),
		       self.request.get('address3'),
		       self.request.get('address4'),
		       self.request.get('address5')]
	loc.notes = self.request.get('notes')
	loc.put()

    def get(self,id):
	if id == '':
	    # search requires parameters
	    west = float(self.request.get('west'))
	    east = float(self.request.get('east'))
	    north = float(self.request.get('north'))
	    south = float(self.request.get('south'))

	# TODO: queries for large areas
	    data = []
	    for loc in Location.query_bbox(north, east, south, west):
		data.append({"lon": loc.loc.lon,
			     "lat": loc.loc.lat,
			     "name": loc.name,
			     "address": loc.address,
			     "notes": loc.notes})

	else:
	    # client requested a specific location
	    key = ndb.Key(urlsafe=id)
	    loc = key.get()
	    data = {"id": id,
		    "lon": loc.loc.lon,
		    "lat": loc.loc.lat,
		    "name": loc.name,
		    "address": loc.address,
		    "notes": loc.notes}
	self.response.headers['Content-Type'] = 'application/json'
	self.response.write(json.encode(data))

api = webapp2.WSGIApplication([
	 ('/api/v1.0/locations/(.*)', LocationAPI)
	], debug=True)

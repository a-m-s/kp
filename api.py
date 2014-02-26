import webapp2
from webapp2_extras import json
from google.appengine.ext import ndb
import logging
import math

class Location(ndb.Model):
    loc = ndb.GeoPtProperty()
    geohash = ndb.StringProperty()
    name = ndb.StringProperty()
    address = ndb.StringProperty()
    notes = ndb.TextProperty()

    L1_hashsize = 0.05

    @classmethod
    def make_geohash_L1(cls, lat, lon):
	# round down to multiple of 0.05
	lat = math.floor(float(lat)*20)/20
	lon = math.floor(float(lon)*20)/20
	if lat == -0.0:
	    lat = 0.0
	if lon == -0.0:
	    lon = 0.0
	return str(lat) + ":" + str(lon)

    @classmethod
    def query_bbox(cls, north, east, south, west):
	# Let's not generate massive queries
	if east > west + 1 or north > south + 1:
	    return []

	squares = []
	x = west
	# generate the list of geohashes we need to find
	while x <= east:
	    y = south
	    while y <= north:
		squares.append(cls.make_geohash_L1(y, x))
		y += cls.L1_hashsize
	    x += cls.L1_hashsize
	result = []
	if len(squares) > 0:
	    logging.info("squares:" + str(squares))
	    for loc in cls.query(Location.geohash.IN(squares)):
		logging.info("loc:" + str(loc))
		logging.info("{0} {1} {2} {3}".format(east,west,north,south))
		# The geohash might return results just outside the search area
		if loc.loc.lon <= east and loc.loc.lon >= west \
		    and loc.loc.lat <= north and loc.loc.lat >= south:
		    result.append(loc)
	logging.info("result: " + str(result))
	return result

class LocationAPI(webapp2.RequestHandler):

    def post(self, arg):
	loc = Location()
	loc.loc = ndb.GeoPt(float(self.request.get('latitude')), float(self.request.get('longitude')))
	loc.geohash = Location.make_geohash_L1(loc.loc.lat, loc.loc.lon)
	loc.name = self.request.get('name')
	loc.address = self.request.get('address')
	loc.notes = self.request.get('notes')
	loc.put()

    def get(self,id):
	if id == '':
	    # search requires parameters
	    west, south, east, north = [float(x) for x in self.request.get('bbox').split(',')]

	    # TODO: queries for large areas
	    data = []
	    for loc in Location.query_bbox(north, east, south, west):
		data.append({"type": "Feature",
			     "geometry": {
			       "type": "Point",
			       "coordinates": [loc.loc.lon, loc.loc.lat]
			     },
			     "properties": {
			       "name": loc.name,
			       "address": loc.address,
			       "notes": loc.notes
			     }
			    })

	else:
	    # client requested a specific location
	    key = ndb.Key(urlsafe=id)
	    loc = key.get()
	    data = [{"type": "Feature",
		     "id": id,
		     "geometry": {
		       "coordinates": [loc.loc.lon, loc.loc.lat]
		     },
		     "properties": {
		       "name": loc.name,
		       "address": loc.address,
		       "notes": loc.notes
		     }
		    }]

	data = {"type": "FeatureCollection",
		"features": data}

	self.response.headers['Content-Type'] = 'application/json'
	jsondata = json.encode(data)
	logging.info("geojson: " + jsondata)
	self.response.write(jsondata)

api = webapp2.WSGIApplication([
	 ('/api/v1.0/locations/(.*)', LocationAPI)
	], debug=True)

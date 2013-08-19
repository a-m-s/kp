import webapp2
from webapp2_extras import json
from google.appengine.ext import ndb

class Location(ndb.Model):
    loc = ndb.GeoPtProperty()
    name = ndb.StringProperty()
    address = ndb.StringProperty(repeated=True)
    notes = ndb.TextProperty()

class LocationAPI(webapp2.RequestHandler):

    def post(self, arg):
	loc = Location()
	loc.loc = ndb.GeoPt(float(self.request.get('latitude')), float(self.request.get('longitude')))
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
	    self.response.write("not implemented")
	else:
	    # client requested a specific location
	    key = ndb.Key(urlsafe=id)
	    loc = key.get()
	    data = {"id": id,
		    "long": loc.loc.lon,
		    "lat": loc.loc.lat,
		    "name": loc.name,
		    "address": loc.address,
		    "notes": loc.notes}
	    self.response.headers['Content-Type'] = 'application/json'
	    self.response.write(json.encode(data))

api = webapp2.WSGIApplication([
	 ('/api/v1.0/locations/(.*)', LocationAPI)
	], debug=True)

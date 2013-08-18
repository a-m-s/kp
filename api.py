import webapp2
from google.appengine.ext import ndb

class Location(ndb.Model):
    loc = ndb.GeoPtProperty()
    name = ndb.StringProperty()
    address = ndb.StringProperty(repeated=True)
    notes = ndb.TextProperty()

class locationAPI(webapp2.RequestHandler):

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

api = webapp2.WSGIApplication([
         ('/api/v1.0/location/(.*)', locationAPI)
        ], debug=True)

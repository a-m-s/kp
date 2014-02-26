#!/bin/sh

curl -X POST -F name="Hengrove Play Park" -F latitude=51.41542 -F longitude=-2.58461 -F address="Hengrove Play Park
Hengrove2
Bristol
BS????" -F notes="hmmmm" http://localhost:8080/api/v1.0/locations/

#!/bin/sh

curl -X POST -F name="Hengrove Play Park" -F latitude=51.41542 -F longitude=-2.58461 -F address1="Hengrove Play Park" -F address2="Hengrove" -F address3="" -F address4="Bristol" -F address5="BS????" -F notes="hmmmm" http://localhost:8080/api/v1.0/locations/

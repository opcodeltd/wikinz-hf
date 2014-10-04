
## Test servers

[Nigel](http://wikinz-hf.dev.home.mcnie.name)

## SODA documentation

[Finding an endpoint](http://dev.socrata.com/docs/endpoints.html)

[JSON conventions that are notable in SODA](http://dev.socrata.com/docs/formats/json.html)

## Sample data services

https://data.cityofnewyork.us/api/views/h9gi-nx95/rows.json?accessType=DOWNLOAD

https://data.cityofchicago.org/resource/alternative-fuel-locations.json


## Findings

Socrata's SODA server doesn't really exist as a usable open source implementation.

SDMX is horrible.  Not human-readable and hard to consume without an XML parser and a lot of code.

SODA data is not typed in any way that's usefully exposed to a user.  You're supposed to guess, and that sucks.  Applications built on the SODA "API" are very brittle.  There doesn't seem to be any versioning, either.

There's an extension header (?) called "XSODA2" that supposedly returns type definitions for the document, but this seems to be undocumented and possibly deprecated.



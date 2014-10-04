
## Our data

Our data has five states.  Data progresses through these states in order.

**Raw** data is the files or URLs received from a contributor.  They are in any format and are not normalised, relational or even necessarily correct.

**Corrected** data is a file or URL which has been cleaned up in some way.  This step is optional and varies depending on the data.  For example, it might mean inflation adjustments, or standardising on units.

**Queryable** data is stored in a database that belongs to us.  It can be queried by us or by other people using a stable API we provide.

**Chartable** data is stored by us in a different database. It consists of simple series extracted from the data that can be used to render a graph or a map.

**Chart** data is the visual representation of the series data, published on the Wiki New Zealand site.


<!-- START HERE -->

Raw:
Raw data sources:  Lots of different sources. CSV, SDMX, whatever.

-> PROCESS:  Chew them up, spit them out as JSON of data series and whatever metadata is available.

Series:
Consume JSON. Render it as a grid with spreadsheet-like controls.  Select series graphically, perhaps create derivative data.  Some are easy (structured data that Team David has already fixed), some are horrible and require a lot of careful selection.  Output is one or more series from a data source.  These can be queried via an API.

[not yet] Composer:  Can transform series or combine them.

Chart Designer:
Select one or more series via the API.  Select a graph type.  Label graph, axes, etc. Get as much as possible of this automatically from metadata.  Output is a graph definition.

Chart Renderer:
Turns a graph definition into an actual chart.  Vega, D3, whatever.

Site (Team Christian):  Put a user interface around the graphs.

<!-- STOP HERE -->



## What other people use

* [Socrata / SODA](http://socrata.com)

* [CKAN](http://ckan.org)

### Socrata

Socrata's SODA server doesn't really exist as a usable open source implementation.

SDMX is horrible.  Not human-readable and hard to consume without an XML parser and a lot of code.

SODA data is not typed in any way that's usefully exposed to a user.  You're supposed to guess, and that sucks.  Applications built on the SODA "API" are very brittle.  There doesn't seem to be any versioning, either.

There's an extension header (?) called "XSODA2" that supposedly returns type definitions for the document, but this seems to be undocumented and possibly deprecated.

Socrata isn't all that.

#### Documentation

* [Finding an endpoint](http://dev.socrata.com/docs/endpoints.html)

* [JSON conventions that are notable in SODA](http://dev.socrata.com/docs/formats/json.html)

#### Sample data services

* [https://data.cityofnewyork.us/api/views/h9gi-nx95/rows.json?accessType=DOWNLOAD](https://data.cityofnewyork.us/api/views/h9gi-nx95/rows.json?accessType=DOWNLOAD)

* [https://data.cityofchicago.org/resource/alternative-fuel-locations.json](https://data.cityofchicago.org/resource/alternative-fuel-locations.json)

### CKAN

CKAN is better.  CKAN is basically a data store for arbitrary tables in Postgres.  Data can be strongly typed provided it's entered via the API, and data can be retrieved via that same API.  This would satisfy our QUERYABLE component for free, but we would still need to write an import system and CHARTABLE.

CKAN's built-in graphing is Recline.js, itself a wrapper on d3.js.  It's not very useful.

#### Documentation

## Test servers

* [Nigel](http://wikinz-hf.dev.home.mcnie.name)

## Charts

* [Vega](https://github.com/trifacta/vega/wiki/Tutorial)


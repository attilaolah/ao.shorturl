ao.shorturl - a reusable short URL library
==========================================

`ao.shorturl` is a library for integrating short URLs to a web application.
Its front-end configuration is not specific to any web application framework,
instead it uses various back-ends for different frameworks.

For example, `ao.shorturl.appengine` implements a Datastore backand for Google
/ Typhoon App Engine. If installed as a Django application, `ao.shorturl` also
provides a template tag for easily displaying short urls for any object that
supports short URLs.

TODO
====

* Write some documentation (high prio)
* Get it 100% unit-tested (high prio)
* Add backends for Django Models and SQLAlchemy/Elixir (low prio)

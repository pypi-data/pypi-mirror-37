=============================
django-pj-feedreader
=============================

.. image:: https://badge.fury.io/py/django-pj-feedreader.png
    :target: https://badge.fury.io/py/django-pj-feedreader

.. image:: https://travis-ci.org/jokimies/django-pj-feedreader.png?branch=master
    :target: https://travis-ci.org/jokimies/django-pj-feedreader

.. image:: https://codecov.io/github/jokimies/django-pj-feedreader/coverage.svg?branch=master
    :target: https://codecov.io/github/jokimies/django-pj-feedreader?branch=master


Django/AngularJS RSS feed reader

Quick install
-------------

Install with pip::

  pip install django-pj-feedreader

Add to 'pjfedreader' to INSTALLED_APPS

Migrate::

  python manage.py migrate

Each feeds need to belong to a caterogy. At the moment way to create
categories is via admin interface. Thus, create the ones needed.

Add JS & CSS files to project

JS::

   <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.3.3/angular.min.js"></script>
   <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.3.3/angular-animate.min.js"></script>
   <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.3.3/angular-cookies.min.js"></script>
   <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.3.3/angular-resource.min.js"></script>
   <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.3.3/angular-route.min.js"></script>
   <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.3.3/angular-sanitize.min.js"></script>
   <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.3.3/angular-touch.min.js"></script>
   <script src="https://cdnjs.cloudflare.com/ajax/libs/ng-dialog/0.5.5/js/ngDialog.min.js"></script>

CSS::

  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" integrity="sha512-dTfge/zgoMYpP7QbHy4gWMEGsbsdZeCXz7irItjcC3sPUFtf0kuFbDz/ixG7ArTxmDjLXDmezHubeNikyKGVyQ==" crossorigin="anonymous">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css"/>
  <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/ng-dialog/0.5.5/css/ngDialog.min.css"/>
  <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/ng-dialog/0.5.5/css/ngDialog-theme-default.min.css"/>
  <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-material-design/0.4.1/css/material.min.css"/>


Features
--------

* TODO

Cookiecutter Tools Used in Making This Package
----------------------------------------------

*  cookiecutter
*  cookiecutter-djangopackage




v0.1.1 (2015-12-05)
-------------------

Fix
~~~

- *requirements*: Specific about Django version. [Petri Jokimies]







- Replace Google API. Fixes #2. [Petri Jokimies]

Documentation
~~~~~~~~~~~~~

- Generated new HISTORY. [Petri Jokimies]

v0.1.0 (2015-11-22)
-------------------

New features
~~~~~~~~~~~~

- Eslint taken into use. [Petri Jokimies]

- *ui*: Added refresh icon to feed panels. [Petri Jokimies]




- *ui*: Feeds can be deleted. [Petri Jokimies]

- *feed*: Add submit function, use new sercives. [Petri Jokimies]




- *layout*: Show three feeds per column. [Petri Jokimies]




- *feed*: Store new feed to server. [Petri Jokimies]

- *feed*: 'Add new feed' dialog added. [Petri Jokimies]






- *ui*: First version to show existing feeds. [Petri Jokimies]




- *admin*: Register to admin interface. [Petri Jokimies]

- *feed*: Feed list & creation via API with tests. [Petri Jokimies]

Fix
~~~

- Don't load needed 3rd party js & css. [Petri Jokimies]




- *ui*: Panel size set, trash can added to panel title. [Petri Jokimies]




- *models*: Initial migrations. [Petri Jokimies]

Refactor
~~~~~~~~

- *feed*: Feed service is handling http failures. [Petri Jokimies]




- *category*: Category service is handling http failures. [Petri
  Jokimies]




- Angular code restructure. [Petri Jokimies]




- *models*: Rename Feed.feed_url to Feed.url. [Petri Jokimies]

- *models*: Update date_checked & date_updated automatically. [Petri
  Jokimies]

- *category*: Removed own category creation functions. [Petri Jokimies]

Documentation
~~~~~~~~~~~~~

- README update. [Petri Jokimies]

Other
~~~~~

- Some css for 'Add' button  and feed panels. [Petri Jokimies]

- Don't use btn-primary. [Petri Jokimies]






- *new feed*: Don't allow invalid form to be submitted. [Petri Jokimies]

- *category*: Test for creating category. [Petri Jokimies]




- *category*: API read test for Category API. [Petri Jokimies]

- First feed model test. [Petri Jokimies]

- Removed Quicstart for now. [Petri Jokimies]

- Initial commit. [Petri Jokimies]



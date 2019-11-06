[![Build Status](https://travis-ci.org/aptivate/django-sortable-listview.svg?branch=master)](https://travis-ci.org/aptivate/django-sortable-listview) [![Coverage Status](https://coveralls.io/repos/aptivate/django-sortable-listview/badge.svg?branch=master)](https://coveralls.io/r/aptivate/django-sortable-listview?branch=master)

django-sortable-listview
========================
An extension of django's ListView that provides sorting.

Features:
- Works with django's built in pagination.
- Contains templates & css for pagination and sort buttons (or just use the context_data and build your own).
- Adds an arrow to show the sort direction on the active sort.
- Knows what the next sort is (i.e. if you're already sorted by title in one direction, clicking on the title button/link again will sort it in the other direction).
- Lets you specify default sort for your list (defaults to -id) and for each of the sortable fields.
- Modifies the queryset, so your database does your sorting.
- Maintains additional query strings (configurable)

Requirements
============

These are the supported versions. Older versions may also work.

    * Python (2.7, 3.5, 3.6, 3.7)
    * Django (1.11, 2.1, 2.2)


Install
=======
Using pip::

    pip install django-sortable-listview

If you want to use the provided templates and CSS add ``'sortable_listview'`` to your INSTALLED_APPS in your django settings.

To see how to include the css and templates in your application, look at the example project. The css is just standard bootstrap.


Example Project
===============
![Screenshot of example project](/example_project/screenshot.png)

To run the example project. First make sure django and django-sortable-listview are on your python path. For example, from inside a virtualenv::

    pip install django
    pip install django-sortable-listview

Then from your cloned folder::

    cd example_project
    python manage.py migrate
    python manage.py runserver

You should be able to see the example project at localhost:8000. A database is provided with some sample content. The username and password is admin/admin

Development and Tests
=====================

For your development setup::

    pip install -r requirements-dev.txt

To run the tests::

    tox

You may not want to run the whole tox suite when you are doing development.
In this case, uncomment the extra lines in requirements-dev.txt, but please
don't commit these changes. (Suggestions welcome on a better way to manage this)

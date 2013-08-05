django-sortable-listview
========================
An extension of django's ListView that provides sorting

Install
=======
Add to your python path.

If you want to use the provided temaplates and CSS add ``'sortable_listview'`` to your INSTALLED_APPS in your django settings.

To see how to include the css and templates in your application, look at the example project. The css is just standard bootstrap.


Example Project
===============
![Screenshot of example project](/example_project/screenshot.png)

To run the example project. First make sure django and django-sortable-listview are on your python path. For example, from inside a virtualenv:

    pip install django
    pip install git+git://github.com/aptivate/django-sortable-listview

Then from your cloned folder:

    cd example_project
    python manage.py runserver

You should be able to see the example project at localhost:8000. A database is provided with some sample content. The username and password is admin/admin

Development and Tests
=====================

To run the tests:

    python setup.py test

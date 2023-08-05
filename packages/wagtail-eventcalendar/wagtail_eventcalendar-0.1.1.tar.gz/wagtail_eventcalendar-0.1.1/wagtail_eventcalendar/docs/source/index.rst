Welcome to Wagtail Event Calendar's documentation!
======================================================

This is a very basic calendar app that integrates with Wagtail. It allows a person to create events that will be shown on the website via fullcalendar and also generates an ical file.

This app is simple, and not feature rich. It does the basics and thats it. I will probably add more features and options to it as time permits, but only if requests are made.

It is also not production ready as there are **no tests currently written** for it. I did put this up on a site and they have been using it extensively and haven't had any reported issues. That said, *apps without tests should always be treated sceptically.*

I hope to write tests in a month or so when I get a bit of free time. I also hope to add a bunch of features in the near future. See: :ref:`roadmap-label`

Please report any errors you encounter. I will try resolve them quickly and then add tests for them as things come up so it doesn't reoccur. Please visit `wagtail_eventcalendar git <https://gitlab.com/dfmeyer/wagtail_eventcalendar>`_ to make pull requests or log issues etc. Documentation is at readthedocs.io: `wagtail_eventcalendar documentation <https://wagtail-eventcalendar.readthedocs.io/en/latest/>`_

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting-started
   syncing
   customising
   internationalisation
   api
   roadmap
   changelog


Thanks
====================

This app wouldn't be possible without the following great projects and people:

   #. `Wagtail CMS <https://wagtail.io/>`_
   #. `Django Web Framework   <https://www.djangoproject.com/>`_
   #. `iCalendar <http://github.com/collective/icalendar>`_
   #. `FullCalendar JS <https://fullcalendar.io/>`_
   #. `Wagtailgmaps <https://github.com/springload/wagtailgmaps>`_
   #. `Bootstrap <http://getbootstrap.com/>`_
   #. `Django Social Share <https://github.com/fcurella/django-social-share>`_
   #. `Font Awesome <https://fontawesome.com/>`_


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

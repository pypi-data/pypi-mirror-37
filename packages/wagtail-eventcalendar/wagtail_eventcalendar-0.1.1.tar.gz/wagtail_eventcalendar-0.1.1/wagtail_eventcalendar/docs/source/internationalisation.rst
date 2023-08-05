**************************
Internationalisation
**************************

Languages
=============

Currently only these languages are fully supported:

    #. English (Daniel F. Meyer)
    #. Afrikaans (Daniel F. Meyer)


It would be super awesome if you translate it to your locale language and make a pull request so that everybody can enjoy your translations. You'll also get credit on this page.

Admin and General Website
------------------------------

To translate the app is super easy thanks to gettext and Django's builtin stuff. This will translate the user interface and admin interface.

.. code-block:: shell

    $ cd wagtail_podcast
    $ django-admin makemessages -l <your_locale>


Open the ``wagtail_eventcalendar/locale/<your_locale>LC_MESSAGES/django.po`` file in your favourite text editor. Provide your translations and then run ``django-admin compilemessages``. The translations should now automatically activate on server restart.

The language will default to what is set in ``settings.py`` ;however, if a specific Wagtail user changes it then it will be what they set as their language or what langauge you serve the page in to the client. See the Django and Wagtail internationalisation documentation on this.

Calendar
---------------------------

The calendar is also rather easy to translate. in the ``templates\wagtail_eventcalendar\event_calendar.html`` and ``templates\wagtail_eventcalendar\event_calendar_category.html`` templates just look at the commented but about translating where it says 'Upcoming'.

To translate the other aspects of the calendar see: `locale <https://fullcalendar.io/docs/locale>`_. Make sure to load this javascript file after you load ``fullcalendar.min.js``. Also remember to change the locale setting.

Caveats
=================

#. I have not internationalised the urls yet; however,its on my list. Just not high on my list of changes.
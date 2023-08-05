Introduction
===========================================

This is a very basic calendar app that integrates with Wagtail. It allows a person to create events that will be shown on the website via FullCalendar and also generates an ical file.

This app is simple, and not feature rich. It does the basics and thats it. I will probably add more features and options to it as time permits, but only if requests are made.

It is also not production ready as there are **no tests currently written** for it. I did put this up on a site and they have been using it extensively and haven't had any reported issues. That said, *apps without tests should always be treated sceptically.*

I hope to write tests in a month or so when I get a bit of free time. I also hope to add a bunch of features in the near future.

Please report any errors you encounter. I will try resolve them quickly and then add tests for them as things come up so it doesn't reoccur. Please visit `wagtail_eventcalendar git <https://gitlab.com/dfmeyer/wagtail_eventcalendar>`_ to make pull requests or log issues etc. Documentation is at readthedocs.io: `wagtail_eventcalendar documentation <https://wagtail-eventcalendar.readthedocs.io/en/latest/>`_

Installation
===================

To install run ``pip install wagtail_eventcalendar``

It should automatically install the dependencies; however, if it doesn't then you will need to install them manually with: ``pip install mutagen wagtailgmaps icalendar pytz django-social-share``

Remember to add ``wagtail_eventcalendar`` (along with the others mentioned) to your installed apps in settings.py i.e.

    .. code-block:: Python

        INSTALLED_APPS = [
            ...
            'wagtail_eventcalendar',
            'wagtail.contrib.modeladmin',
            'wagtailgmaps',
            'django_social_share',
            'wagtail.contrib.routable_page',
        ]

Requirements:

    .. code-block:: Python

        python3
        icalendar
        wagtail
        django
        django-social-share
        pytz
        wagtailgmaps

You will need to follow the wagtailgmaps installation instructions to get things to work: https://github.com/springload/wagtailgmaps/

I'm not quite sure how far back this app works; however, it should work going back quite far. It's currently tested on Python3 with Wagtail >2 and Django >2 on openSUSE. It should work on all platforms and shouldn't break anytime soon. Let me know if you have a combo that doesn't work and I'll see what I can do to support it.

Caveats
============

#.  I haven't implemented nested categories yet. I will eventually, but not just yet.

#. It only exports to ical for now. I will hopefully add support for caldav and gcal as well at some point.

#. Recurring events are currently not supported. This is really high on my list, but I haven't figured out a really great way to do it whilst keeping everything simple and manageable.
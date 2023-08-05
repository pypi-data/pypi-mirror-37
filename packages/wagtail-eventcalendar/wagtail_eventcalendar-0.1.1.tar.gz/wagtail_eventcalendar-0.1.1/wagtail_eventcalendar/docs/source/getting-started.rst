***************************
Getting Started
***************************

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

*Please see the* :ref:`caveats-label` *below*

Usage
===================================

To use the app just add a Calendar Root Page to your page hierarchy and fill in the details as necessary.

To create a new calendar entry just click the tab on the left handside labelled calendar and add Calendar Events there. You can also add, delete and manage your categories in the panel.

To sync with your devices see: :ref:`Syncing <syncing-label>`

To get an ical file for either a calendar, a calendar filtered by category or even just a specific event, append ``/ical/`` to the url.


Customising
==========================

Honestly I give a really basic thing. No menus, no title bar, just some bootstrap cards, and a side bar, all of which is responsive. I highly recommend you edit the templates. I do plan on creating template tags at a later stage that should make customising much easier in the future. This is a rough, ugly framework just to get you on your feet. Go nuts! I recommend cheaking out the beautiful themes (based on Bootstrap) made by `Creative Tim <https://www.creative-tim.com/>`_

For more about customising see: :ref:`customising-label`

.. _caveats-label:

Caveats
============

#.  I haven't implemented nested categories yet. I will eventually, but not just yet.

#. It only exports to ical for now. I will hopefully add support for caldav and gcal as well at some point.

#. Recurring events are currently not supported. This is really high on my list, but I haven't figured out a really great way to do it whilst keeping everything simple and manageable.




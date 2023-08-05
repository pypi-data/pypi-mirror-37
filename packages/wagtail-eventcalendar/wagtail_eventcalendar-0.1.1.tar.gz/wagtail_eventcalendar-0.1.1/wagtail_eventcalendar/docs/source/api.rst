********************************
API Documentation
********************************

FullCalendar API
======================

To get events we return JSON. The api is super simple, but perfectly functional.

To get the events you need three components in your GET request namely ``start``, ``end`` and ``timezone`` so a URL would look something like this ``https://example.com/calendar/events?start=<start date and time>&end=<end date and time>&timezone='<timezone>'``

This API is made for simple GET requests only and is based on what FullCalendar uses.


Models
===========================

.. automodule:: wagtail_eventcalendar.models
    :members:
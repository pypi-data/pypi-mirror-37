.. _syncing-label:

Syncing
===================

There isn't any real syncing implemented. If you can subscribe to an internet icalendar then you can sync. This is well supported on iOS and OSX, as well as pretty much everything in the Linux world. You will need an app on Android. Outlook has an extension available too.

You cannot add events to the calendar from a device. Only receive. Most of the time when a user clicks the <calendar add> button then it will give them the ical file. How each client handles that is up to the client. Most will just add the calendar entry to the device (all devices I know of including Android and Microsoft out of the box) but will not support syncing with them.

If you have very many clients accessing the calendar for syncing purposes it can have performance rammifications. This is because ical files are always dynamically generated on each and every request to them. You may be able to use Varnish to cache them for a few minutes at a time thus bringing requests actually hitting the servers down to a very negligible amount.

There is at present no :ref:`gcal and caldav syncing support <roadmap-label>`. If I do ever introduce it, it will be one way only i.e. devices cannot add to a calendar, only the admin interface can. Two way syncing is out of the scope of this project.

All calendars are at present public. I have not implemented any kind of permissions to them.
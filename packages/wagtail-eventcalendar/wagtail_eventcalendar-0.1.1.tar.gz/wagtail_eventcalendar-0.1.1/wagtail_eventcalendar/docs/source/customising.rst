.. _customising-label:

===================
Customising
===================

Edit the template files. I do plan on doing template tags in the :ref:`future <roadmap-label>` for a better experience but this is just how it is for now.

All that you absolutely need is to load the ``wagtail_eventcalendar/css/fullcalendar.min.css`` at the top of the page. You will need to load ``wagtail_eventcalendar/js/jquery.min.js`` and ``wagtail_eventcalendar/js/moment.min.js`` before ``wagtail_podcast/js/fullcalendar.min.js`` static files in the ``wagtail_eventcalendar/event_calendar.html`` and ``wagtail_eventcalendar/event_calendar_category.html`` templates.

To actually render the calendar add the following:

.. code-block:: html

    <div id='calendar'></div>
    <script type="text/javascript">
        $(document).ready(function () {
            $('#calendar').fullCalendar({
                header: {center: 'month,agendaWeek,upcoming'},
                timeFormat: 'H(:mm)',
                nowIndicator: true,
                timezone: 'Africa/Johannesburg', //Change as necessary
                eventColor: "#f8f9fa", //Change as necessary
                eventTextColor: "#9c27b0", //Change as necessary
                businessHours: [{
                    dow: [1, 2, 3, 4, 5],
                    start: '08:00',
                    end: '13:00'
                }, //change as necessary
                    {
                        dow: [7],
                        start: '10:00',
                        end: '11:00'
                    }
                ],
                views: {
                    upcoming: {
                        type: 'list',
                        duration: {months: 2},
                        buttonText: 'Upcoming', //translate as necessary
                        validRange: function (nowDate) {
                            return {
                                start: nowDate,
                                end: nowDate.clone().add(1, 'months')
                            };
                        }
                    }
                },
                // put your options and callbacks here
                events: '{{ page.get_url }}events/'
            })
        });
    </script>

There is plenty of customisation available of both how the calendar looks and functions, see: `FullCalendar JS docs <https://fullcalendar.io/docs>`_ . In the above snippet of code you'll see that i added come comment that give you a decent starting point.
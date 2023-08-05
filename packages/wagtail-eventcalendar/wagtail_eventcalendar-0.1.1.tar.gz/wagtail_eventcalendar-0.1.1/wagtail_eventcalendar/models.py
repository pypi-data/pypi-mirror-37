from django.db import models
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.core.models import Page
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from .managers import CategoryManager
from modelcluster.fields import ParentalKey
from wagtailgmaps.edit_handlers import MapFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
import json
from django.shortcuts import render
from django.utils import timezone
from wagtail.search import index
from icalendar import Calendar, Event, vText
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
import pytz
import django.http
from typing import Union


# Create your models here.

class EventCalendar(RoutablePageMixin, Page):
    """
    Base calendar class which actually displays the calendar.
    """

    description = RichTextField(blank=True, help_text=_('Description of the calendar'), verbose_name=_('Description'))
    """ Short description of the calendar."""

    default_image = models.ForeignKey('wagtailimages.Image',
                                      null=True,
                                      blank=True,
                                      on_delete=models.SET_NULL,
                                      related_name='+',
                                      verbose_name=_('Default Image'),
                                      help_text=_('Default image to be used for calendar entries')
                                      )
    """ Default image to be used for calendar entries """

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        ImageChooserPanel('default_image'),
    ]

    subpage_types = ['wagtail_eventcalendar.EventCalPage']

    search_fields = Page.search_fields + [
        index.SearchField('description')
    ]

    class Meta:
        verbose_name = _("Calendar Root Page")

    @route(r"^events/$")
    def getEvents(self, request: django.http.HttpRequest) -> django.http.HttpResponse:
        """
        Route that returns the events. Is accessed by fullcalender as the api to call

        :param request: Django request
        :return: JSON of the events ard their details
        """

        def filterForPeriod(request: django.http.HttpRequest) -> models.QuerySet:
            """
            Filter for the specific time frame being queried by FullCalendar

            :param request: Django request
            :return: Queryset of EventCalPage objects
            """

            # TODO make sure start and end points work properly
            events = EventCalPage.objects.filter(start_dt__range=[request.GET['start'], request.GET['end']]).live()
            return events

        if request.is_ajax():
            result = [
                {
                    'title': event.title,
                    'start': event.start_dt.astimezone(pytz.timezone(request.GET['timezone'])).isoformat(),
                    'end': event.end_dt.astimezone(pytz.timezone(request.GET['timezone'])).isoformat(),
                    'url': event.url
                } for event in filterForPeriod(request)
            ]
            json_output = json.dumps(result)
            return HttpResponse(json_output)
        else:
            return super(EventCalendar, self).serve(request)

    @route(r"^category/(?P<category>[\w\-]+)/$")
    def viewByCategory(self, request: django.http.HttpRequest, **kwargs) -> django.http.HttpResponse:
        """
        View calendar by a specific category

        :param request: Django request
        :param kwargs: Django request kwargs
        :return: HttpResponse that shows a calendar filtered by a category
        """

        return render(request, "wagtail_eventcalendar/event_calendar_category.html",
                      {'self': self, 'page': self, 'category': kwargs['category']})

    @route(r"^category/(?P<category>[\w\-]+)/events/$")
    def getEventsByCategory(self, request: django.http.HttpRequest, **kwargs: dict) -> django.http.HttpResponse:
        """
        Gets the events for a specific category for a specific timeframe. Is accessed by fullcalender.js

        :param request: Django request
        :param kwargs: Django request kwargs
        :return: HttpResponse
        """

        categ = kwargs['category']

        def filterForPeriod(request: django.http.HttpRequest, categ: str) -> django.http.HttpResponse:
            """
            Filters for a period taking into account the specific category

            :param request:
            :param categ:
            :return:
            """
            # TODO make sure start and end points work properly
            events = EventCalPage.objects.filter(start_dt__range=[request.GET['start'], request.GET['end']]).live()
            events = events.filter(categories__name__iexact=categ)

            return events

        if request.is_ajax():
            result = [
                {
                    'title': event.title,
                    'start': event.start_dt.astimezone(pytz.timezone(request.GET['timezone'])).isoformat(),
                    'end': event.end_dt.astimezone(pytz.timezone(request.GET['timezone'])).isoformat(),
                    'url': event.url
                } for event in filterForPeriod(request, categ)
            ]
            json_output = json.dumps(result)
            return HttpResponse(json_output)
        else:
            return render(request, "wagtail_eventcalendar/event_calendar_category.html",
                          {'self': self, 'page': self, 'category': kwargs['category']})

    @route(r'^ical/$')
    def icalView(self, request: django.http.HttpRequest, *args, **kwargs: dict) -> django.http.HttpResponse:
        """
        Route that produces the ical files requested by clients.

        :param request: Django request
        :param args: Django request args
        :param kwargs: Django request kwargs
        :return: HttpResponse containing an ical file
        """

        cal = Calendar()
        cal.add('prodid', '-//Calendar Event event//mxm.dk//')
        cal.add('version', '2.0')
        for entry in EventCalPage.objects.live():
            event = Event()
            event.add('summary', entry.title)
            event.add('dtstart', entry.start_dt)
            event.add('dtend', entry.end_dt)
            event.add('dtstamp', timezone.now())
            event.add('uid', str(entry.pk))
            event['location'] = vText(entry.location)
            cal.add_component(event)
        return HttpResponse(cal.to_ical(), content_type="text/calendar")

    @route(r"^category/(?P<category>[\w\-]+)/ical/$")
    def icalViewCategory(self, request: django.http.HttpRequest, *args, **kwargs: dict) -> django.http.HttpResponse:
        """
        Route that produces the ical files requested by clients, but filtered for a specific category

        :param request: Django HttpRequest
        :param args: Django request args
        :param kwargs: Django request kwargs
        :return: HttpResponse containing an ical file
        """
        cal = Calendar()
        cal.add('prodid', '-//Calendar Event event//mxm.dk//')
        cal.add('version', '2.0')
        print(kwargs['category'])
        for entry in EventCalPage.objects.filter(categories__name__iexact=kwargs['category']).live():
            event = Event()
            event.add('summary', entry.title)
            event.add('dtstart', entry.start_dt)
            event.add('dtend', entry.end_dt)
            event.add('dtstamp', timezone.now())
            event.add('uid', str(entry.pk))
            event['location'] = vText(entry.location)
            cal.add_component(event)
        return HttpResponse(cal.to_ical(), content_type="text/calendar")

    @property
    def get_categories(self) -> models.QuerySet:
        """
        Gets the calendar categories that currently exist

        :return: Returns a Queryset of Category objects
        """
        return Category.objects.all()

    @property
    def get_url(self) -> str:
        """
        Gets the url of the calendar page

        :return: Url of the calendar page
        """
        return self.url


class EventCalPage(RoutablePageMixin, Page):
    """
    Calendar entry/ an even base model.
    """

    categories = models.ManyToManyField('wagtail_eventcalendar.Category', through='wagtail_eventcalendar.CategoryEventPage', blank=True,
                                        help_text=_('Categories this event belongs to'), verbose_name=_('Categories'))
    """Optional category that a specific calendar entry may belong to"""

    description = RichTextField(blank=True, help_text=_('Description of event'), verbose_name=_('Description'))
    """Required. Description of the event/calendar entry"""

    image = models.ForeignKey('wagtailimages.Image',
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              related_name='+',
                              verbose_name=_('Image'),
                              )
    """Optional image to associate with a calendar entry. Only really useful for the website"""

    start_dt = models.DateTimeField(help_text=_('Starting time of event'),
                                    verbose_name=_('Start of Event'))
    """Required. Start datetime of the event/calender entry"""

    end_dt = models.DateTimeField(help_text=_('End time of event. Does not need to be same day.'),
                                  verbose_name=_('End of Event'))
    """Required. End datetime of the event/calender entry. Must be after start_dt else it raises a Validation Error"""

    location = models.CharField(max_length=255, blank=True, help_text=_('Location of event'),
                                verbose_name=_('Location'))
    """Optional location information"""

    problem_status = models.BooleanField(default=False, help_text=_('Whether there is a problem with the event'),
                                         verbose_name=_('Problem Status'))
    """Optional true/false indicating whether there is an issue with an event. It is important to both the ical files and the website"""

    problem_text = models.TextField(blank=True, null=True, help_text=_('Text that describes the problem. Keep brief.'),
                                    verbose_name=_('Problem Description'))
    """Optional text that describes what is wrong. Used in conjunction with problem_status. Requires problem_status = true to work at all."""

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        ImageChooserPanel('image'),
        FieldPanel('start_dt'),
        FieldPanel('end_dt'),
        MapFieldPanel('location'),
        MultiFieldPanel([
            InlinePanel("event_categories", label=_("Categories"))
        ])
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('problem_status'),
        FieldPanel('problem_text')
    ]

    parent_page_types = ["wagtail_eventcalendar.EventCalendar"]

    search_fields = Page.search_fields + [
        index.SearchField('description'),
        index.RelatedFields('categories', [
            index.SearchField('name'),
            index.SearchField('description'),
        ])
    ]

    class Meta:
        verbose_name = _("Calendar Event")

    def clean(self):
        """
        Checks that the end date and time occurs after the start date and date
        """

        if self.start_dt > self.end_dt:
            raise ValidationError(_('Start date and time must be before end date and time'))

    def save(self, *args, **kwargs):
        """
        Overloads the save method of the Page model. It applies the default image to a calendar entry/event if it doesn't already have one.
        """
        if not self.image:
            self.image = EventCalendar.objects.live()[0].default_image

        super(EventCalPage, self).save()

    @property
    def get_categories(self) -> models.QuerySet:
        """
        Gets all the event categories.

        :return: Queryset containing the Categories objects
        """
        return Category.objects.all()

    @property
    def get_status_text(self) -> Union[str, bool]:
        """
        Shows the status text of a calender entry/event

        :return: Str if the event is finished, or begun but not yet completed else false.
        """
        if self.end_dt < timezone.now():
            return _("Event Finished")
        elif self.problem_status:
            return self.problem_text
        elif self.start_dt < timezone.now() < self.end_dt:
            return _("Event has begun")  # TODO  better time format @ {self.start_dt.isoformat()}
        else:
            return False

    @route(r'^ical/$')
    def icalView(self, request: django.http.HttpRequest, *args, **kwargs: dict) -> django.http.HttpResponse:
        """
        Route that returns an ical file for a specific event.

        :param request: Django HttpRequest
        :param args: Normal request args
        :param kwargs: Normal request kwargs
        :return: ical file as part of HttpResponse with only the details of a specific event
        """
        cal = Calendar()
        cal.add('prodid', '-//Calendar Event event//mxm.dk//')
        cal.add('version', '2.0')
        event = Event()
        event.add('summary', self.title)
        event.add('dtstart', self.start_dt)
        event.add('dtend', self.end_dt)
        event.add('dtstamp', timezone.now())
        event.add('uid', str(self.pk))
        event['location'] = vText(self.location)
        cal.add_component(event)
        return HttpResponse(cal.to_ical(), content_type="text/calendar")


class Category(models.Model):
    """
    Category to which an event belongs
    """

    name = models.CharField(max_length=80, unique=True, verbose_name=_('Category name'))
    """Required. Name of the category"""

    slug = models.SlugField(unique=True, max_length=80)
    """Required. Not used. Planned for later. Make it the same as the name for now."""

    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name="children",
        verbose_name=_('Parent category'),
        on_delete=models.SET_NULL
    )
    """Optional. Not used currently. Planned for later as part of nested categories."""

    description = models.CharField(max_length=500, blank=True, verbose_name=_('Description'))
    """Optional description of a specific category."""

    objects = CategoryManager()

    def __str__(self):
        return self.name

    def clean(self):
        """
        Ensures that there are no circular references when it comes to nested categories.
        """
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError(_('Parent category cannot be self.'))
            if parent.parent and parent.parent == self:
                raise ValidationError(_('Cannot have circular Parents.'))

    def save(self, *args, **kwargs):
        """
        Overrides Page model save method. Handles the slug
        """
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = _("Event Category")
        verbose_name_plural = _("Event Categories")


class CategoryEventPage(models.Model):
    """Internally used model. Ignore."""

    category = models.ForeignKey(Category, related_name="+", verbose_name=_('Category'), on_delete=models.CASCADE)
    page = ParentalKey('EventCalPage', related_name='event_categories')
    panels = [
        FieldPanel('category')
    ]

    def __str__(self):
        return str(self.category)

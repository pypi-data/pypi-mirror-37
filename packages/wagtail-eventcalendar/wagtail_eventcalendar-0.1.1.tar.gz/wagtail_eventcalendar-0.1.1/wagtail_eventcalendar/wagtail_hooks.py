from django.utils.translation import ugettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from .models import EventCalPage, Category


class EventCalPageModelAdmin(ModelAdmin):
    """
    ModelAdmin required for pulling the calender functionality out of the pages hierarchy for easier accessibility.
    """
    model = EventCalPage
    menu_label = _('Calendar Events')
    menu_icon = 'date'
    list_display = ('title', 'start_dt', 'description', 'categories')
    list_filter = ('start_dt', 'categories')
    search_fields = ('title', 'description', 'start_dt', 'categories')


class EventCalPageCategoryAdmin(ModelAdmin):
    """
    Model Admin required for making the calendar categories available in the special calendar tab
    """
    model = Category
    menu_label = _('Categories')
    menu_icon = 'group'
    list_display = ('name',)
    search_fields = ('name',)


class EventCalendarModelAdminGroup(ModelAdminGroup):
    """
    ModelAdminGroup that allows one to add Events/Calendar Entries via a tab on the sidebar rather than digging through the page hierarchy.
    """
    menu_label = _('Calendar')
    menu_icon = 'date'
    menu_order = 300
    items = (EventCalPageModelAdmin, EventCalPageCategoryAdmin)


modeladmin_register(EventCalendarModelAdminGroup)

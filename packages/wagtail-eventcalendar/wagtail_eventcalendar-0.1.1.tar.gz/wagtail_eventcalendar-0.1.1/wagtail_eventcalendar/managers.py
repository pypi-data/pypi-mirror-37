from django.db import models


class CategoryManager(models.Manager):

    def with_uses(self, announcements):
        entries = announcements.get_entries()
        return self.filter(announcements__in=entries).distinct()

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

class Service(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
        ordering = ['name']

    def __str__(self):
        return self.name


class PublicSubscriptionManager(models.Manager):
    def get_queryset(self):
        qs = super(PublicSubscriptionManager, self).get_queryset()
        return qs.filter(is_public=True)


class Subscription(models.Model):
    url = models.URLField()
    title = models.CharField('title', max_length=255)
    description = models.TextField('description', blank=True)
    is_public = models.BooleanField('public', default=True)
    date_created = models.DateTimeField('date created')
    date_updated = models.DateTimeField('date updated')
    owner = models.ForeignKey(User, verbose_name='owner',
        related_name='bookmarks', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Service, blank=True)

    objects = models.Manager()
    public = PublicSubscriptionManager()

    class Meta:
        verbose_name = 'bookmark'
        verbose_name_plural = 'bookmarks'
        ordering = ['-date_created']

    def __str__(self):
        return '%s (%s)' % (self.title, self.url)

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = now()
        self.date_updated = now()
        super(Subscription, self).save(*args, **kwargs)
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    # override a Manager’s base QuerySet by overriding the Manager.get_queryset() method. get_queryset() should return a QuerySet with the properties you require
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    #A slug is a short label for something, containing only letters, numbers, underscores or hyphens. They’re generally used in URLs.
    #unique_for_date:Set this to the name of a DateField or DateTimeField to require that this field be unique for the value of the date field.
    # For example, if you have a field title that has unique_for_date="pub_date", then Django wouldn’t allow the entry of two records with the same title and pub_date
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    #auto_now fields are updated to the current timestamp every time an object is saved and are therefore perfect for tracking when an object was last modified,
    # while an auto_now_add field is saved as the current timestamp when a row is first added to the database and is therefore perfect for tracking when it was created.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager() # The default manager.
    #custom manager
    published = PublishedManager() # The Dahl-specific manager.

    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    #this method should appear to return a string that can be used to refer to the object over HTTP
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.strftime('%m'),
                                                 self.publish.strftime('%d'),
                                                 self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)

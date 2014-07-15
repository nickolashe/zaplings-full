from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your models here.
class Idea(models.Model):
    creator = models.ForeignKey(User)
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title

class FeaturedIdea(models.Model):
    idea = models.ForeignKey(Idea)

    def __unicode__(self):
        return self.idea.title

class Love(models.Model):
    tagname = models.CharField(max_length=200)

    def __unicode__(self):
        return self.tagname

class Offer(models.Model):
    tagname = models.CharField(max_length=200)

    def __unicode__(self):
        return self.tagname

class Need(models.Model):
    tagname = models.CharField(max_length=200)

    def __unicode__(self):
        return self.tagname

class UserLove(models.Model):
    user = models.ForeignKey(User)
    love = models.ForeignKey(Love)

class UserNeed(models.Model):
    user = models.ForeignKey(User)
    need = models.ForeignKey(Need)

class UserOffer(models.Model):
    user = models.ForeignKey(User)
    offer = models.ForeignKey(Offer)

class NewUserEmail(models.Model):
    email = models.EmailField(max_length=60, unique=True)

      #def was_published_recently(self):
    #    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

#class User(models.Model):
#    email = models.EmailField(max_length=60)
#    password = models.CharField(max_length=255)
#    loggedin = models.BooleanField(default=False)
#
#    def __unicode__(self):
#        return self.email
#
#    def is_logged_in(self):
#        return self.loggedin

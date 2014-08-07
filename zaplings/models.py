from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your models here.
class Idea(models.Model):
    creator = models.ForeignKey(User)
    title = models.CharField(max_length=40)
    tagline = models.CharField(max_length=40)
    description = models.CharField(max_length=100)

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

    def __unicode__(self):
        return ' '.join([self.user.username, "loves", self.love.tagname])

class UserNeed(models.Model):
    user = models.ForeignKey(User)
    need = models.ForeignKey(Need)

    def __unicode__(self):
        return ' '.join([self.user.username, "needs", self.need.tagname])

class UserOffer(models.Model):
    user = models.ForeignKey(User)
    offer = models.ForeignKey(Offer)

    def __unicode__(self):
        return ' '.join([self.user.username, "offers", self.offer.tagname])

class NewUserEmail(models.Model):
    email = models.EmailField(max_length=60, unique=True)

    def __unicode__(self):
        return self.email

class LoveText(models.Model):
    user = models.ForeignKey(User, unique=True)
    text = models.CharField(max_length=1000)

class OfferText(models.Model):
    user = models.ForeignKey(User, unique=True)
    text = models.CharField(max_length=1000)

class NeedText(models.Model):
    user = models.ForeignKey(User, unique=True)
    text = models.CharField(max_length=1000)

class Where(models.Model):
    user = models.ForeignKey(User, unique=True)
    radius = models.IntegerField(blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    place = models.CharField(max_length=100, blank=True)
    hangout = models.BooleanField()

    def __unicode__(self):
        return ' '.join([self.user.username + "'s",
                         "where preferences"])

class When(models.Model):
    user = models.ForeignKey(User, unique=True)
    weekdays = models.BooleanField()
    weekends = models.BooleanField()
    mornings = models.BooleanField()
    afternoons = models.BooleanField()
    evenings = models.BooleanField()
    nights = models.BooleanField()
    utc_offset = models.IntegerField()

    def __unicode__(self):
        return ' '.join([self.user.username + "'s",
                         "when preferences"])

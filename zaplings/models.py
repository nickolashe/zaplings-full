from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class IdeaType(models.Model):
    ideatype = models.CharField(max_length=50)

    def __unicode__(self):
        return self.ideatype


class Idea(models.Model):
    creator = models.ForeignKey(User)
    ideatype = models.ForeignKey(IdeaType)
    title = models.CharField(max_length=40)
    tagline = models.CharField(max_length=40)
    description = models.CharField(max_length=100)
    notes = models.CharField(max_length=10000)
    ispublic = models.BooleanField() # something for "if user has public ideas" 
    isfunding = models.BooleanField()
    haspage = models.BooleanField()
    
    def __unicode__(self):
        return self.title


class FeaturedIdea(models.Model):
    idea = models.ForeignKey(Idea)

    def __unicode__(self):
        return self.idea.title


class IdeaTeam(models.Model):
    member = models.ForeignKey(User)
    idea = models.ForeignKey(Idea)
    isadmin = models.BooleanField()

    def __unicode__(self):
        return "%s is member of idea %s" % \
                (member.username, idea.title)


class Love(models.Model):
    tagname = models.CharField(max_length=200)
    issuggested = models.BooleanField()

    def __unicode__(self):
        return self.tagname


class Offer(models.Model):
    tagname = models.CharField(max_length=200)
    issuggested = models.BooleanField()

    def __unicode__(self):
        return self.tagname


class Need(models.Model):
    tagname = models.CharField(max_length=200)
    issuggested = models.BooleanField()

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

    def __unicode__(self):
        return ' '.join(["Love text for", self.user.username])


class OfferText(models.Model):
    user = models.ForeignKey(User, unique=True)
    text = models.CharField(max_length=1000)

    def __unicode__(self):
        return ' '.join(["Offer text for", self.user.username])


class NeedText(models.Model):
    user = models.ForeignKey(User, unique=True)
    text = models.CharField(max_length=1000)

    def __unicode__(self):
        return ' '.join(["Need text for", self.user.username])


class UserRsvp(models.Model):
    """
    Keep timestamps of rsvp's
    """
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return "%s rsvp'd at %s" % (self.user.username, self.date)



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


class FeedBack(models.Model):
    user = models.ForeignKey(User)
    feedback_type = models.CharField(max_length=30)    
    feedback_subject = models.CharField(max_length=200,   blank=True)    
    feedback_response = models.CharField(max_length=2000, blank=True)    

    def __unicode__(self):
        subject = self.feedback_subject
        return "feedback from [%s] on %s (%s)" % \
                    (self.user.username,
                     subject if subject else 'No subject provided',
                     self.feedback_type)


class Referrer(models.Model):
    referrer = models.ForeignKey(User, related_name="user_referrer")
    # email address of referred user    
    referree = models.ForeignKey(User, related_name="user_referree", unique=True) 

    def __unicode__(self):
        return "%s referred %s" % (self.referrer.username, self.referree.username)

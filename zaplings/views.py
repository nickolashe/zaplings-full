from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from zaplings.models import FeaturedIdea, Love, Offer, Need, UserLove, UserOffer, UserNeed, LoveText, OfferText, NeedText, NewUserEmail, Where, When, FeedBack, Referrer
from django.template import RequestContext, loader
from django.views import generic
from django.db import IntegrityError

from nltk.stem.snowball import SnowballStemmer

import logging
import time

logging.basicConfig(level=logging.INFO, filename="logs/views.log")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class IndexView(generic.ListView):
    #model = FeaturedIdea
    template_name = 'zaplings/index.html'
    context_object_name = 'featured_ideas'

    def get_queryset(self):
        """Return the all features ideas."""
        return FeaturedIdea.objects.all()

class LovesView(generic.ListView):
    template_name = 'zaplings/loves.html'
    context_object_name = 'suggested_loves'

    def get_queryset(self):
        """Return top suggested loves."""
        # pre-sort loves based on frequency of selection
        loves_freq = [ [ userlove.love.id 
                        for userlove in UserLove.objects.filter(love_id=id) ]
                      for id in [ love.id 
                                  for love in Love.objects.all() ]]
        # display first n tags
        top_loves = sorted(loves_freq, key=len, reverse=True)[:12]
        suggested_loves = Love.objects.filter(id__in=[loveid[0] 
                                              for loveid in top_loves])
        #return Love.objects.all()
        logger.info("top loves: %s", [(Love.objects.get(pk=ids[0]), len(ids)) \
                                      for ids in top_loves] )
        return suggested_loves
    
class OffersView(generic.ListView):
    template_name = 'zaplings/offers.html'
    context_object_name = 'suggested_offers'

    def get_queryset(self):
        """Return the top suggested offers."""
        # pre-sort offers based on frequency of selection
        offers_freq = [ [ useroffer.offer.id 
                        for useroffer in UserOffer.objects.filter(offer_id=id) ]
                      for id in [ offer.id 
                                  for offer in Offer.objects.all() ]]
        # display first n tags
        top_offers = sorted(offers_freq, key=len, reverse=True)[:12]
        suggested_offers = Offer.objects.filter(id__in=[offerid[0] 
                                              for offerid in top_offers])
        #return Offer.objects.all()
        logger.info("top offers: %s", [(Offer.objects.get(pk=ids[0]), len(ids)) \
                                      for ids in top_offers] )
        return suggested_offers
    
class NeedsView(generic.ListView):
    template_name = 'zaplings/needs.html'
    context_object_name = 'suggested_needs'

    def get_queryset(self):
        """Return top suggested needs."""
        needs_freq = [ [ userneed.need.id 
                        for userneed in UserNeed.objects.filter(need_id=id) ]
                      for id in [ need.id 
                                  for need in Need.objects.all() ]]
        # display first n tags
        top_needs = sorted(needs_freq, key=len, reverse=True)[:12]
        suggested_needs = Need.objects.filter(id__in=[needid[0] 
                                              for needid in top_needs])
        #return Need.objects.all()
        logger.info("top needs: %s", [ (Need.objects.get(pk=ids[0]), len(ids)) \
                                        for ids in top_needs] )
        return suggested_needs

class RsvpView(generic.ListView):
    model = User    
    template_name = 'zaplings/creatorsnight.html'

class WhereView(generic.ListView):
    model = User    
    template_name = 'zaplings/where.html'

class WhenView(generic.ListView):
    model = User    
    template_name = 'zaplings/when.html'

class SignupView(generic.ListView):
    model = User
    template_name = 'zaplings/signup.html'

class MyIdeasView(generic.ListView):
    model = User
    template_name = 'zaplings/myideas.html'

class NewIdeaView(generic.ListView):
    model = User
    template_name = 'zaplings/newidea.html'

class ThankYouView(generic.ListView):
    model = User
    template_name = 'zaplings/thankyou.html'

class ProfileView(generic.ListView):
    context_object_name = 'user_tags'    
    template_name = 'zaplings/profile.html'
    queryset = Love.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user_tags = generate_user_tags(pk)
        context.update(user_tags)
        # And so on for more models
        return context

class AboutView(generic.ListView):
    model = User
    template_name = 'zaplings/10-reasons.html'
    
class HowItWorksView(generic.ListView):
    model = User
    template_name = 'zaplings/howitworks.html'
    
class GetInvolvedView(generic.ListView):
    model = User
    template_name = 'zaplings/getinvolved.html'
    
class FaqView(generic.ListView):
    model = User
    template_name = 'zaplings/faq.html'

class ErrorView(generic.ListView):
    model = User
    template_name = 'zaplings/error.html'

class IdeaFeedView(generic.ListView):
    model = User    
    template_name = 'zaplings/idea-feed.html'

class DiscussView(generic.ListView):
    model = User    
    template_name = 'zaplings/discuss.html'

class EditProfileView(generic.ListView):
    model = User
    template_name = 'zaplings/editprofile.html'
    
class ViewIdeaPageView(generic.ListView):
    model = User
    template_name = 'zaplings/view-idea-page.html'

class EditIdeaPageView(generic.ListView):
    model = User
    template_name = 'zaplings/edit-idea-page.html'

class ShareView(generic.ListView):
    model = User
    template_name = 'zaplings/share.html'
 
class ProfileTextView(generic.ListView):
    model = Love
    template_name = 'zaplings/profile-text.html'

class ViewProfileView(generic.ListView):
    model = User
    template_name = 'zaplings/profile-view.html'

# form handler views
def referrer(request, referrer):
    logger.info("referrer is [%s]", referrer)
    request.session['referrer'] = referrer
    #logger.info("request.session: %s", str(request.session.items()))
    request_obj = { 'featured_ideas': FeaturedIdea.objects.all() }
    # return back to index for the time-being
    return render(request, 'zaplings/index.html', request_obj) 

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

    #return HttpResponse("You're voting on poll %s." % poll_id)


def record_loves(request):
    """
    process input from zaplings:loves
    create new love offer tags based on nltk stemmer match results
    redirect to zaplings:profile
    """
    try:
        userid = None
        login_log_msg = "No user session - redirecting to login"
        login_status_msg = { 'login_status_message': 'Please login to Zaplings!' }         
        try:
            userid = request.user.pk
            logger.info("Current session userid: [%s]", request.user.username) 
        except Exception as e:
            logger.info(login_log_msg)
            return render(request, 'zaplings/signup.html', login_status_msg) 

        if userid:
            if request.method == "POST":
                logger.info(request.POST)
                love_ids = set(request.POST.getlist(u'love-tag'))
                logger.info("Selected love ids: %s", str(love_ids))
                selected_loves = [ Love.objects.get(id=love_id).tagname \
                                   for love_id in love_ids ]
                logger.info("Selected love tags: %s", str(selected_loves))

                # process new love tags
                new_love_tags = request.POST.getlist(u'love-tag-new')
                logger.info("New love tags: %s", str(new_love_tags))
                if new_love_tags:
                    stemmer = SnowballStemmer('english')
                for tag in new_love_tags:
                    # stem existing tags
                    stemmed_loves = dict([(stemmer.stem(love.tagname), love.id) 
                                           for love in Love.objects.all() ])
                    
                    if not stemmer.stem(tag) in stemmed_loves.keys():
                        new_tag = Love.objects.create(tagname=tag)
                        love_ids.add(new_tag.id)
                        logger.info("Added new love tag [%s] with id [%d]", 
                                     tag, int(new_tag.id))
                    else:
                        exist_id = stemmed_loves[stemmer.stem(tag)]
                        love_ids.add(exist_id)
                        logger_msg = ' '.join(["Stem match for love tag [%s].",
                                               "Adding existing love tag id [%d]."])
                        logger.info(logger_msg, tag, int(exist_id))

                for love_id in love_ids:
                    if not UserLove.objects.filter(user_id=request.user.pk, 
                                                   love_id=love_id):
                        UserLove.objects.create(user_id=request.user.pk, 
                                                love_id=love_id)

                # pre-sort offers based on frequency of selection
                offers_freq = [ [ useroffer.offer.id 
                                for useroffer in UserOffer.objects.filter(offer_id=id) ]
                              for id in [ offer.id 
                                          for offer in Offer.objects.all() ]]
                # display first n tags
                top_offers = sorted(offers_freq, key=len, reverse=True)[:12]
                suggested_offers = Offer.objects.filter(id__in=[offerid[0] 
                                                        for offerid in top_offers])
                logger.info("top offers: %s", [ (Offer.objects.get(pk=ids[0]), len(ids)) \
  
                                                 for ids in top_offers] )
                #suggested_offers = Offer.objects.all()
                return render(request, 'zaplings/offers.html', {
                    'suggested_offers': suggested_offers
                })
            else:
                return redirect('zaplings:loves')
        else:
            logger.info("Redirecting to login")
            request_obj = { 'login_status_message': 'Please login to Zaplings!' }
            return render(request, 'zaplings/signup.html', request_obj)
    except Exception as e:
        logger.error("Error in record_loves: %s (%s)",
                      e.message, str(type(e)))
        return redirect('zaplings:error')

def record_offers(request):
    """
    process input from zaplings:offers
    create new offer tags based on nltk stemmer match results
    redirect to zaplings:profile
    """
    try:
        userid = None
        login_log_msg = "No user session - redirecting to login"
        login_status_msg = { 'login_status_message': 'Please login to Zaplings!' }         
        try:
            userid = request.user.pk
            logger.info("Current session userid: [%s]", request.user.username) 
        except Exception as e:
            logger.info(login_log_msg)
            return render(request, 'zaplings/signup.html', login_status_msg) 

        if userid:
            if request.method == "POST":
                logger.info(request.POST)
                offer_ids = set(request.POST.getlist(u'offer-tag'))
                logger.info("Selected offer ids: %s", str(offer_ids))
                selected_offers = [ Offer.objects.get(id=offer_id).tagname \
                                   for offer_id in offer_ids ]
                logger.info("Selected offer tags: %s", str(selected_offers))
                
                # process new love tags
                new_offer_tags = request.POST.getlist(u'offer-tag-new')
                logger.info("New offer tags: %s", str(new_offer_tags))
                if new_offer_tags:
                    stemmer = SnowballStemmer('english')
                for tag in new_offer_tags:
                    # stem existing tags
                    stemmed_offers = dict([(stemmer.stem(offer.tagname), offer.id)
                                           for offer in Offer.objects.all() ])
                    
                    if not stemmer.stem(tag) in stemmed_offers.keys():
                        new_tag = Offer.objects.create(tagname=tag)
                        offer_ids.add(new_tag.id)
                        logger.info("Added new offer tag [%s] with id [%d]", 
                                     tag, int(new_tag.id))
                    else:
                        exist_id = stemmed_offers[stemmer.stem(tag)]
                        offer_ids.add(exist_id)
                        logger_msg = ' '.join(["Stem match for offer tag [%s].",
                                               "Adding existing offer tag id [%d]."])
                        logger.info(logger_msg, tag, int(exist_id))

                for offer_id in offer_ids:
                    if not UserOffer.objects.filter(user_id=request.user.pk, 
                                                    offer_id=offer_id):
                        UserOffer.objects.create(user_id=request.user.pk, 
                                                 offer_id=offer_id)

                # pre-sort offers based on frequency of selection
                needs_freq = [ [ userneed.need.id 
                                for userneed in UserNeed.objects.filter(need_id=id) ]
                              for id in [ need.id 
                                          for need in Need.objects.all() ]]
                # display first n tags
                top_needs = sorted(needs_freq, key=len, reverse=True)[:12]
                suggested_needs = Need.objects.filter(id__in=[needid[0] 
                                                      for needid in top_needs])
                # suggested_needs = Need.objects.all()
                logger.info("top needs: %s", [ (Need.objects.get(pk=ids[0]), len(ids)) \
 
                                                for ids in top_needs] )
                return render(request, 'zaplings/needs.html', {
                    'suggested_needs': suggested_needs
                })
            else:
                return redirect('zaplings:loves')
        else:
            logger.info("Redirecting to login")
            request_obj = { 'login_status_message': 'Please login to Zaplings!' }
            return render(request, 'zaplings/signup.html', request_obj)
    except Exception as e:
        logger.error("Error in record_offers: %s (%s)",
                      e.message, str(type(e)))
        return redirect('zaplings:error')

def record_needs(request):
    """
    process input from zaplings:needs
    create new need tags based on nltk stemmer match results
    redirect to zaplings:profile
    """
    try:
        userid = None
        login_log_msg = "No user session - redirecting to login"
        login_status_msg = { 'login_status_message': 'Please login to Zaplings!' }         
        try:
            userid = request.user.pk
            logger.info("Current session userid: [%s]", request.user.username) 
        except Exception as e:
            logger.info(login_log_msg)
            return render(request, 'zaplings/signup.html', login_status_msg) 

        if userid:
            if request.method == "POST":
                logger.info('POST request: %s', str(request.POST))
                need_ids = set(request.POST.getlist(u'need-tag'))
                logger.info("Selected need ids: %s", str(need_ids))
                selected_needs = [ Need.objects.get(id=need_id).tagname \
                                   for need_id in need_ids ]
                logger.info("Selected need tags: %s", str(selected_needs))
                
               # process new love tags
                new_need_tags = request.POST.getlist(u'need-tag-new')
                logger.info("New need tags: %s", str(new_need_tags))
                if new_need_tags:
                    stemmer = SnowballStemmer('english')
                for tag in new_need_tags:
                    # stem existing tags
                    stemmed_needs = dict([(stemmer.stem(need.tagname), need.id) 
                                           for need in Need.objects.all() ])
                    
                    if not stemmer.stem(tag) in stemmed_needs.keys():
                        new_tag = Need.objects.create(tagname=tag)
                        need_ids.add(new_tag.id)
                        logger.info("Added new need tag [%s] with id [%d]", 
                                     tag, int(new_tag.id))
                    else:
                        exist_id = stemmed_needs[stemmer.stem(tag)]
                        need_ids.add(exist_id)
                        logger_msg = ' '.join(["Stem match for need tag [%s].",
                                               "Adding existing need tag id [%d]."])
                        logger.info(logger_msg, tag, int(exist_id))

                for need_id in need_ids:
                    if not UserNeed.objects.filter(user_id=request.user.pk, 
                                                    need_id=need_id):
                        UserNeed.objects.create(user_id=request.user.pk, 
                                                 need_id=need_id)

                # get all user tags to render profile
                user_tags = get_user_tags(userid)
                logger.info("User tags: %s", user_tags)
                return render(request, 'zaplings/profile.html', user_tags)
            else:
                logger.info('GET request: %s', str(request.GET))
                return redirect('zaplings:loves')
        else:
            logger.info("Redirecting to login")
            request_obj = { 'login_status_message': 'Please login to Zaplings!' }
            return render(request, 'zaplings/signup.html', request_obj) 
                 
    except Exception as e:
        logger.error("Error in record_need: %s (%s)",
                      e.message, str(type(e)))
        return redirect('zaplings:error')


def record_wheres(request):
    """
    process input from zaplings:where
    redirect to zaplings:profile
    """
    try:
        userid=None
        login_log_msg = "No user session - redirecting to login"
        login_status_msg = { 'login_status_message': 'Please login to Zaplings!' }
    
        try:
            userid = request.user.pk
            logger.info("Current session userid: [%s]", request.user.username)
        except Exception as e:
            logger.info(login_log_msg)
            return render(request, 'zaplings/signup.html', login_status_msg) 
    
        if not userid:
            logger.info(login_log_msg)
            return render(request, 'zaplings/signup.html', login_status_msg)
    
        if request.method == "POST":
            post = request.POST
            logger.info('POST request: %s', str(post))
    
            if not Where.objects.filter(user_id=userid):
                # create new user
                user_where = Where.objects.create(user_id=userid, 
                                                  radius=-1,
                                                  zipcode="",
                                                  hangout=True)
            else:
                # update existing user
                user_where = Where.objects.get(user_id=userid)
    
            if post.has_key('meet-local') and post.get('meet-local') == 'on':
                # radius
                if post.has_key('radius'):
                    user_where.radius = int(post.get('radius'))
                # zipcode
                if post.has_key('zipcode'):
                    user_where.zipcode = post.get('zipcode')
    
            if post.has_key('place'):
                user_where.place = post.get('place')
    
            if not post.has_key('hangout'):
                user_where.hangout = False
    
            user_where.save()
     
            user_tags = generate_user_tags(request, userid)
            return render(request, 'zaplings/profile.html', user_tags)
        else:
            logger.info('GET request - redirecting to loves')
            return redirect('zaplings:loves')
    except Exception as e:
        logger.error("Error in record_wheres: %s (%s)",
                      e.message, str(type(e)))
        return redirect('zaplings:error')


def record_whens(request):
    """
    process input from zaplings:when
    redirect to zaplings:profile
    """
    try:
        userid = request.user.pk
        logger.info("Current session userid: [%s]", request.user.username)
    except Exception as e:
        logger.info("Redirecting to login")
        request_obj = { 'login_status_message': 'Please login to Zaplings!' }
        return render(request, 'zaplings/signup.html', request_obj) 
 
    try:
        if request.method == "POST":
            post = request.POST
            logger.info('POST request: %s', str(post))

            if not When.objects.filter(user_id=userid):
                # create new user
                user_where = When.objects.create(user_id=userid,
                                                 weekdays=False,
                                                 weekends=False,
                                                 mornings=False,
                                                 afternoons=False,
                                                 evenings=False,
                                                 nights=False,
                                                 utc_offset=-5)
            else:
                # update existing user
                user_when = When.objects.get(user_id=userid)

            # weekdays
            if post.has_key('weekdays') and post['weekdays'] == 'on':
                logger.info("weekdays is set") 
                user_when.weekdays = True
            # weekends
            if post.has_key('weekends') and post['weekends'] == 'on':
                logger.info("weekends is set") 
                user_when.weekends = True
            # mornings
            if post.has_key('mornings') and post['mornings'] == 'on':
                logger.info("mornings is set") 
                user_when.mornings = True
            # afternoons
            if post.has_key('afternoons') and post['afternoons'] == 'on':
                logger.info("afternoons is set") 
                user_when.afternoons = True
            # evenings
            if post.has_key('evenings') and post['evenings'] == 'on':
                logger.info("evenings is set") 
                user_when.evenings = True
            # nights
            if post.has_key('nights') and post['nights'] == 'on':
                logger.info("nights is set") 
                user_when.nights = True
              
            user_tags = generate_user_tags(request, userid)
            return render(request, 'zaplings/profile.html', user_tags)
        else:
            logger.info('GET request: %s', str(request.GET))
            return redirect('zaplings:loves')
    except Exception as e:
        logger.error("Error in record_whens: %s (%s)",
                      e.message, str(type(e)))
        return redirect('zaplings:error')

def record_text(request):
    """
    record custom text from loves, offers, needs fields
    redirect to profile-view
    """
    try:
        userid = request.user.pk

        if userid:
            logger.info("Recording text's for userid [%s]", userid)
            love_text = request.POST['love_text'] if request.POST.has_key('love_text') \
                                                  else ''
            offer_text = request.POST['offer_text'] if request.POST.has_key('offer_text') \
                                                    else ''
            need_text = request.POST['need_text'] if request.POST.has_key('need_text') \
                                                  else ''
            if love_text:
                try:
                    LoveText.objects.create(user_id=userid, text=love_text)
                except IntegrityError:
                    lovetext = LoveText.objects.get(user_id=userid)
                    lovetext.text = love_text
                    lovetext.save()
            else:
                try:
                    love = LoveText.objects.get(user_id=userid)
                    love_text = love.text
                except Exception:
                    pass
            if offer_text:
                try:
                    OfferText.objects.create(user_id=userid, text=offer_text)
                except IntegrityError:
                    offertext = OfferText.objects.get(user_id=userid)
                    offertext.text = offer_text
                    offertext.save()
            else:
                try:
                    offer = OfferText.objects.get(user_id=userid)
                    offer_text = offer.text
                except Exception:
                    pass
            if need_text:
                try:
                    NeedText.objects.create(user_id=userid, text=need_text)
                except IntegrityError:
                    needtext = NeedText.objects.get(user_id=userid)
                    needtext.text = need_text
                    needtext.save()
            else:
                try:
                    need = NeedText.objects.get(user_id=userid)
                    need_text = need.text
                except Exception:
                    pass
        
            # render profile-view now
            #request_obj = get_user_tags(userid)
            #return render(request, 'zaplings/profile-view.html', request_obj)
            return redirect('zaplings:share')
        else:
            logger.info("Redirecting to login")
            request_obj = { 'login_status_message': 'Please login to Zaplings!' }
            return render(request, 'zaplings/signup.html', request_obj)

    except Exception as e:
        logger.error("Error in record_text: %s (%s)",
                      e.message, str(type(e)))
        return redirect('zaplings:error')


def get_user_tags(userid):
    # user loves
    user_loves = [love.love_id for love in UserLove.objects.filter(user_id=userid)]
    user_lovetags = [Love.objects.get(id=love_id).tagname for love_id in user_loves]
     # user offers
    user_offers = [offer.offer_id for offer in UserOffer.objects.filter(user_id=userid)]
    user_offertags = [Offer.objects.get(id=offer_id).tagname for offer_id in user_offers]
    # user needs
    user_needs = [need.need_id for need in UserNeed.objects.filter(user_id=userid)]
    user_needtags = [Need.objects.get(id=need_id).tagname for need_id in user_needs]

    #user love text
    user_lovetext = None
    try:
        user_lovetext = LoveText.objects.get(user_id=userid)
        user_lovetext = user_lovetext.text
    except Exception as e:
        logger.info("No love text for userid [%s]", userid)
        pass
   
    #user offer text
    user_offertext = None
    try:
        user_offertext = OfferText.objects.get(user_id=userid)
        user_offertext = user_offertext.text
    except Exception as e:
        logger.info("No offer text for userid [%s]", userid)
        pass
   
    #user need text
    user_needtext = None
    try:
        user_needtext = NeedText.objects.get(user_id=userid)
        user_needtext = user_needtext.text
    except Exception as e:
        logger.info("No need text for userid [%s]", userid)
        pass
   
    user_profile =  { 'user_lovetags': user_lovetags,
                      'user_offertags': user_offertags,
                      'user_needtags': user_needtags,
                      'love_text': user_lovetext,
                      'offer_text': user_offertext,
                      'need_text': user_needtext }
    return user_profile    

def generate_user_tags(request, userid):
    """
    obtain the set of user selected profile tags
    pass on the set of tags to profile
    """
    if userid:
        logger.info("Userid provided: [%s]", userid) 
        user_tags = get_user_tags(userid)
        logger.info("User tags: %s", user_tags)
        return render(request, 'zaplings/profile.html', user_tags)                
    else:
        logger.error('No userid provided')
        return render(request, 'zaplings/signup.html', {
            'login_status_message': "Please enter your email!"
            })    

def generate_profile(request):
    """
    obtain the set of user selected profile tags
    pass on the set of tags to profile
    """
    try:
        userid = request.user.pk

        if userid:
            logger.info("Userid provided: [%s]", userid) 
            user_tags = get_user_tags(userid)
            logger.info("User tags: %s", user_tags)
            return render(request, 'zaplings/profile.html', user_tags)                
        else:
            logger.error('No userid provided')
            return render(request, 'zaplings/signup.html', {
                'login_status_message': "Please login to Zaplings!"
                })    
    except Exception as e:
        logger.info("Redirecting to login")
        request_obj = { 'login_status_message': 'Please login to Zaplings!' }
        return render(request, 'zaplings/signup.html', request_obj)

def record_feedback(request):
    """
    record feedback to the database
    redirect to the index page with a status message
    """
    login_status_msg = ' '.join(["We'd like to be able to contact you back -",
                                 "please login to Zaplings!"])
    index_status_msg = ' '.join(["Thank you for your feedback!",
                           "It will help us build a better next version of Zaplings!"])
    try:
        userid = request.user.pk

        if userid:
            logger.info("Userid provided: [%s]", userid) 
            logger.info("POST from feedback form: %s", str(request.POST))
            feedback_type = request.POST.get('feedback-type')
            feedback_subject = request.POST.get('feedback-subject')
            feedback_response = request.POST.get('feedback-response')
            try:
                FeedBack.objects.create(user_id=userid,
                                        feedback_type=feedback_type,
                                        feedback_subject=feedback_subject,
                                        feedback_response=feedback_response)
                logger.info("Recorded feedback from [%s] on %s (%s)",
                         request.user.username,
                         feedback_subject if feedback_subject else 'No subject provided',
                         feedback_type)
                #request.QueryDict.update( { 'status_message': index_status_msg } )
                #return redirect('zaplings:index')
                return render(request, 'zaplings/index.html', {
                              'status_message': index_status_msg,
                              'featured_ideas': FeaturedIdea.objects.all() })
            except Exception as e:
                logger.error("Error recording feedback from [%s]: %s (%s)",
                              userid, e.message, str(type(e)))
                return redirect('zaplings:error')
        else:
            logger.error('No userid provided')
            return render(request, 'zaplings/signup.html', {
                'login_status_message': login_status_msg }) 
    except Exception as e:
        logger.info("Redirecting to login")
        request_obj = { 'login_status_message': login_status_msg }
        return render(request, 'zaplings/signup.html', request_obj)


def record_new_email(request):
    try:
        email = request.POST['email']
        status_message = {'REENTER': 'Please enter your email.',
                          'EXISTS': 'You are already part of Zaplings! Thanks!',
                          'SUCCESS': 'Thank you for joining Zaplings!'}
        # REENTER
        if not email or not '@' in email:
            status = 'REENTER'
            logger.info('Empty email submitted')
            request_obj = { 'featured_ideas': FeaturedIdea.objects.all(),
                            'status_message': status_message[status] }
            # return back to index for the time-being
            return render(request, 'zaplings/index.html', request_obj) 
    
        # EXISTING EMAIL
        elif User.objects.filter(username=email):
            status = 'EXISTS'
            logger.info('Email [%s] has already been submitted.', email)
            # create django user if needed
            request_obj = { 'signup_email': email }
            # return back to index for the time-being
            return render(request, 'zaplings/signup.html', request_obj) 
      
        # EXISTING USER
        elif User.objects.filter(email=email):
            status = 'EXISTS'
            # create new user (email, '')
            try:
                NewUserEmail.objects.create(email=email)
            except Exception as e:
                pass
            # generate user tags and redirect to profile
            #return render(request, 'zaplings/profile.html', {}) 
            request_obj = { 'login_email': email }
            # return back to index for the time-being
            return render(request, 'zaplings/signup.html', request_obj) 
    
        # NEW USER
        else:
            try:
                newuser = User.objects.create_user(email)
                newuser.set_password('')
                newuser.save()
                status= 'SUCCESS'
                logger.info('Created user [%s]', email)
            except IntegrityError:
                logger.error('User [%s] already exists.', email)
                status = 'EXISTS'

            #logger.info("request.session: %s", str(request.session.items()))
            if request.session.has_key('referrer'):
                referrer_username = request.session['referrer']
                logger.info("New user [%s] was referred by [%s]", 
                             email, referrer_username)
                try:
                    referrer_id = User.objects.get(username=referrer_username).pk
                    referree_id = User.objects.get(username=email).pk
                    Referrer.objects.create( referrer_id = referrer_id,
                                             referree_id = referree_id)
                    logger.info("Recorded this referral")
                except IntegrityError:
                    logger.info("This referral has already been recorded!")
                except Exception:
                    logger.info("Unable to record this referral")
            # login new user
            login_email(request, email)
  
            # generate user tags and redirect to profile
            return HttpResponseRedirect(reverse('zaplings:generate_user_tags', args=(request.user.pk,)))
    except Exception as e:
        logger.error("Error in record_new_email: %s (%s)",
                      e.message, str(type(e)))
        return redirect('zaplings:error')
             

def signup_user(request):
    status_message = { 'PASSWORD_VERIFY': 'Passwords do not match!',
                       'PASSWORD_EMPTY': 'Please type in your password',
                       'NAME_EMPTY': 'Please enter your name',
                       'EMAIL_EMPTY': 'Please enter your email',
                       'EMAIL_EXISTS': 'User is already registered with this email',
                       'USERNAME_EMPTY': 'Please pick a username',
                       'USERNAME_EXISTS': 'This username already exists',
                       'USER_UPDATED': 'Thank you for joining Zaplings!',
                       'USER_CREATED': 'Thank you for joining Zaplings!' }
    try:
        email = request.POST['user-email']
        firstname = request.POST['user-firstname']
        lastname = request.POST['user-lastname']
        username = request.POST['user-username']
        password = request.POST['user-password']
        password_verify = request.POST['user-password-verify']

        status = ''
        if password == password_verify:
            if password:
                password_valid = password
            else:
                status = 'PASSWORD_EMPTY'
        else:
            status = 'PASSWORD_VERIFY'
   
        if not email:
            status = 'EMAIL_EMPTY'
        if not firstname or not lastname:
            status = 'NAME_EMPTY'
        if not username:
            status = 'USERNAME_EMPTY'
        if User.objects.filter(username=username):
            status = 'USERNAME_EXISTS'
        if User.objects.filter(email=email):
            status = 'EMAIL_EXISTS'

        failure_keys = [key for key in status_message.keys() if 'USER_' not in key]
        if not status in failure_keys:
            if User.objects.filter(username=email):
                user = User.objects.get(username=email)
                user.username = username
                user.email = email
                status = 'USER_UPDATED'
            else:
                user = User.objects.create_user(username=username, 
                                                email=email)
                status = 'USER_CREATED'
            user.first_name = firstname
            user.last_name = lastname
            user.set_password(password_valid)
            user.save()
            user = authenticate(username=username, password=password_valid)
            if user is not None and user.is_active:
                login(request, user)
                logger.info('Logged in [%s]', user.username)
            return HttpResponseRedirect(reverse('zaplings:generate_user_tags', args=(request.user.pk,)))
        else:
            request_obj = { 'signup_status_message': status_message[status] }
            return render(request, 'zaplings/signup.html', request_obj) 
    except Exception as e:
        request_obj = { 'status_message': e.message }
        # return back to index for the time-being
        return render(request, 'zaplings/signup.html', request_obj) 

def login_email(request, email):
    user = authenticate(username=email, password='')
    # extra check enforced for active users
    if user is not None and user.is_active:
        login(request, user)
        logger.info('Logged in [%s]', email)

def login_email_password(request):
    status_message = { 'LOGIN_INCORRECT': "The login information you provided did not match our records. Please try again.",
                       'LOGIN_INCOMPLETE': "Please include both email and password." }
    error_message = None
    user = None
    try:
        login_name = request.POST['login-name']
        password = request.POST['password']
        logger.info("Requested login with login name %s", login_name)
        match = User.objects.filter(username=login_name)
        if match:
            username = login_name
        else:
            match = User.objects.filter(email=login_name)
            if match:
                username = match[0].username
            else:
                raise User.DoesNotExist
        user = authenticate(username=username, password=password)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request, user)
                auth_message = "User %s is valid, active and authenticated"
            else:
                auth_message = "The password is valid, but the account %s has been disabled!"
            logger.info(auth_message, username)
        else:
            # the authentication system was unable to verify the username and password
            error_message = status_message['LOGIN_INCORRECT']

    except KeyError:
        # Redisplay the poll voting form.
        error_message = status_message['LOGIN_INCOMPLETE']
    except User.DoesNotExist:
        error_message = status_message['LOGIN_INCORRECT']

    if error_message:
        return render(request, 'zaplings/signup.html', {
            'login_status_message': error_message
        })
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        #user_tags = generate_user_tags(user.pk)
        #return render(request, 'zaplings/profile.html', user_tags)
        return HttpResponseRedirect(reverse('zaplings:generate_user_tags', args=(request.user.pk,)))

def user_logout(request):
    status_msg = None
    try:
        username = request.user.username
        if request.user.is_authenticated():
            logout(request)
            logger.info('Logged out [%s]', username)
            status_msg = "You've been succesfully logged out!"
        else:
            status_msg = ' '.join(["You're not logged in.",
                                   "Please enter your email to enter Zaplings!"])
    except Exception as e:
        logger.error('Could not log out user [%s]', username)

    request_obj = { 'featured_ideas': FeaturedIdea.objects.all(),
                    'status_message': status_msg }
    # return back to index for the time-being
    return render(request, 'zaplings/index.html', request_obj) 

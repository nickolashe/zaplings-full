from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from zaplings.models import FeaturedIdea, Love, Offer, Need, UserLove, UserOffer, UserNeed, LoveText, OfferText, NeedText, FeedBack, UserRsvp
from django.views import generic
from django.db import IntegrityError

from nltk.stem.snowball import SnowballStemmer

import logging
import requests

logging.basicConfig(level=logging.INFO, filename="logs/views.log")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class IndexView(generic.ListView):
    template_name = 'zaplings/index.html'
    context_object_name = 'featured_ideas'

    def get_queryset(self):
        """Return the all features ideas."""
        return FeaturedIdea.objects.all()


class IndexAltView(generic.ListView):
    model = User
    template_name = 'zaplings/index-alt.html'

    
class MissionView(generic.ListView):
    model = User
    template_name = 'zaplings/our-mission.html'

    
class RsvpEmail(generic.ListView):
    model = User
    template_name = 'zaplings/rsvp-email.html'


class BlogView(generic.ListView):
    model = User
    template_name = 'zaplings/blog.html'


class LovesView(generic.ListView):
    template_name = 'zaplings/loves.html'
    context_object_name = 'suggested_loves'

    def get_queryset(self):
        """Return top suggested loves."""
        # pre-sort loves based on frequency of selection
        loves_freq = [[
            userlove.love.id
            for userlove in UserLove.objects.filter(love_id=id)]
            for id in [love.id for love in Love.objects.all()]]

        # display first n tags
        top_loves = sorted(loves_freq, key=len, reverse=True)[:12]
        suggested_loves = Love.objects.filter(
            id__in=[loveid[0] for loveid in top_loves if loveid])
        logger.info(
            "top loves: %s",
            [(Love.objects.get(pk=ids[0]), len(ids)) 
             for ids in top_loves
             if ids]
        )
        return suggested_loves


class OffersView(generic.ListView):
    template_name = 'zaplings/offers.html'
    context_object_name = 'suggested_offers'

    def get_queryset(self):
        """
        Return the top suggested offers.
        """
        # pre-sort offers based on frequency of selection
        offers_freq = [[
            useroffer.offer.id
            for useroffer in UserOffer.objects.filter(offer_id=id)]
            for id in [offer.id for offer in Offer.objects.all()]]

        # display first n tags
        top_offers = sorted(offers_freq, key=len, reverse=True)[:12]
        suggested_offers = Offer.objects.filter(
            id__in=[offerid[0] for offerid in top_offers if offerid])
        logger.info(
            "top offers: %s",
            [(Offer.objects.get(pk=ids[0]), len(ids))
             for ids in top_offers
             if ids]
        )
        return suggested_offers


class NeedsView(generic.ListView):
    template_name = 'zaplings/needs.html'
    context_object_name = 'suggested_needs'

    def get_queryset(self):
        """
        Return top suggested needs.
        """
        needs_freq = [[
            userneed.need.id
            for userneed in UserNeed.objects.filter(need_id=id)]
            for id in [need.id for need in Need.objects.all()]]

        # display first n tags
        top_needs = sorted(needs_freq, key=len, reverse=True)[:12]
        suggested_needs = Need.objects.filter(
            id__in=[needid[0] for needid in top_needs if needid])
        logger.info(
            "top needs: %s",
            [(Need.objects.get(pk=ids[0]), len(ids)) 
             for ids in top_needs
             if ids]
        )
        return suggested_needs


class RsvpView(generic.ListView):
    context_object_name = 'suggested_tags'
    template_name = 'zaplings/creatorsnight.html'
    queryset = Love.objects.all()

    def get_context_data(self, **kwargs):
        context = super(RsvpView, self).get_context_data(**kwargs)
        suggested_tags = {
            'suggested_loves': Love.objects.filter(issuggested=True),
            'suggested_offers': Offer.objects.filter(issuggested=True),
            'suggested_needs': Need.objects.filter(issuggested=True),
        }
        context.update(suggested_tags)
        # And so on for more models
        logger.info('context: %s', context)
        return context


class RsvpConfirmView(generic.ListView):
    model = User
    template_name = 'zaplings/rsvp-confirm.html'


class SignupView(generic.ListView):
    model = User
    template_name = 'zaplings/signup.html'


class MyIdeasView(generic.ListView):
    model = User
    template_name = 'zaplings/myideas.html'


class JetView(generic.ListView):
    model = User
    template_name = 'zaplings/jet.html'


class JetEditView(generic.ListView):
    model = User
    template_name = 'zaplings/jet-edit.html'


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
    request_obj = {'featured_ideas': FeaturedIdea.objects.all()}
    # return back to index for the time-being
    return render(request, 'zaplings/index.html', request_obj)


def record_loves(request, isRedirected=True):
    """
    process input from zaplings:loves
    create new love offer tags based on nltk stemmer match results
    redirect to zaplings:profile
    """
    try:
        userid = None
        login_log_msg = "No user session - redirecting to login"
        login_status_msg = {
            'login_status_message': 'Please login to Zaplings!'}
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
                selected_loves = [
                    Love.objects.get(id=love_id).tagname
                    for love_id in love_ids]
                logger.info("Selected love tags: %s", str(selected_loves))

                # process new love tags
                new_love_tags = request.POST.getlist(u'love-tag-new')
                logger.info("New love tags: %s", str(new_love_tags))
                if new_love_tags:
                    stemmer = SnowballStemmer('english')
                for tag in new_love_tags:
                    # stem existing tags
                    stemmed_loves = dict([
                        (stemmer.stem(love.tagname), love.id)
                        for love in Love.objects.all()])

                    if not stemmer.stem(tag) in stemmed_loves.keys():
                        new_tag = Love.objects.create(
                            tagname=tag,
                            issuggested=False)
                        love_ids.add(new_tag.id)
                        logger.info(
                            "Added new love tag [%s] with id [%d]",
                            tag,
                            int(new_tag.id))
                    else:
                        exist_id = stemmed_loves[stemmer.stem(tag)]
                        love_ids.add(exist_id)
                        logger_msg = ' '.join([
                            "Stem match for love tag [%s].",
                            "Adding existing love tag id [%d]."])
                        logger.info(logger_msg, tag, int(exist_id))

                for love_id in love_ids:
                    if not UserLove.objects.filter(
                        user_id=request.user.pk,
                        love_id=love_id):
                        UserLove.objects.create(
                            user_id=request.user.pk, love_id=love_id)
 
                # redirect to offers or not
                if isRedirected:
                    return redirect('zaplings:offers')
            else:
                return redirect('zaplings:creatorsnight')
        else:
            return redirect('zaplings:creatorsnight')
    except Exception as e:
        logger.error("Error in record_loves: %s (%s)",
                      e.message, str(type(e)))
        return redirect('zaplings:error')


def record_offers(request, isRedirected=True):
    """
    process input from zaplings:offers
    create new offer tags based on nltk stemmer match results
    redirect to zaplings:profile
    """
    try:
        userid = None
        login_log_msg = "No user session - redirecting to login"
        login_status_msg = {
            'login_status_message': 'Please login to Zaplings!'}
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
                selected_offers = [
                    Offer.objects.get(id=offer_id).tagname
                    for offer_id in offer_ids]
                logger.info("Selected offer tags: %s", str(selected_offers))

                # process new love tags
                new_offer_tags = request.POST.getlist(u'offer-tag-new')
                logger.info("New offer tags: %s", str(new_offer_tags))
                if new_offer_tags:
                    stemmer = SnowballStemmer('english')
                for tag in new_offer_tags:
                    # stem existing tags
                    stemmed_offers = dict([
                        (stemmer.stem(offer.tagname), offer.id)
                        for offer in Offer.objects.all()])

                    if not stemmer.stem(tag) in stemmed_offers.keys():
                        new_tag = Offer.objects.create(
                            tagname=tag,
                            issuggested=False)
                        offer_ids.add(new_tag.id)
                        logger.info(
                            "Added new offer tag [%s] with id [%d]",
                            tag,
                            int(new_tag.id))
                    else:
                        exist_id = stemmed_offers[stemmer.stem(tag)]
                        offer_ids.add(exist_id)
                        logger_msg = ' '.join([
                            "Stem match for offer tag [%s].",
                            "Adding existing offer tag id [%d]."])
                        logger.info(logger_msg, tag, int(exist_id))

                for offer_id in offer_ids:
                    if not UserOffer.objects.filter(
                        user_id=request.user.pk,
                        offer_id=offer_id):
                        UserOffer.objects.create(
                            user_id=request.user.pk,
                            offer_id=offer_id)
 
                # redirect to needs or not
                if isRedirected:
                    return redirect('zaplings:needs')
            else:
                return redirect('zaplings:creatorsnight')
        else:
            return redirect('zaplings:creatorsnight')
    except Exception as e:
        logger.error("Error in record_offers: %s (%s)",
                      e.message, str(type(e)))
        return redirect('zaplings:error')


def record_needs(request, isRedirected=True):
    """
    process input from zaplings:needs
    create new need tags based on nltk stemmer match results
    redirect to zaplings:profile
    """
    try:
        userid = None
        login_log_msg = "No user session - redirecting to login"
        login_status_msg = {
            'login_status_message': 'Please login to Zaplings!'}

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
                selected_needs = [
                    Need.objects.get(id=need_id).tagname
                    for need_id in need_ids]
                logger.info("Selected need tags: %s", str(selected_needs))

                # process new love tags
                new_need_tags = request.POST.getlist(u'need-tag-new')
                logger.info("New need tags: %s", str(new_need_tags))
                if new_need_tags:
                    stemmer = SnowballStemmer('english')
                for tag in new_need_tags:
                    # stem existing tags
                    stemmed_needs = dict([
                        (stemmer.stem(need.tagname), need.id)
                        for need in Need.objects.all()])

                    if not stemmer.stem(tag) in stemmed_needs.keys():
                        new_tag = Need.objects.create(
                            tagname=tag,
                            issuggested=False)
                        need_ids.add(new_tag.id)
                        logger.info(
                            "Added new need tag [%s] with id [%d]",
                            tag,
                            int(new_tag.id))
                    else:
                        exist_id = stemmed_needs[stemmer.stem(tag)]
                        need_ids.add(exist_id)
                        logger_msg = ' '.join([
                            "Stem match for need tag [%s].",
                            "Adding existing need tag id [%d]."])
                        logger.info(logger_msg, tag, int(exist_id))

                for need_id in need_ids:
                    if not UserNeed.objects.filter(
                        user_id=request.user.pk,
                        need_id=need_id):
                        UserNeed.objects.create(
                            user_id=request.user.pk,
                            need_id=need_id)

                # redirect to profile
                if isRedirected:
                    # generate user tags and redirect to profile
                    return HttpResponseRedirect(
                        reverse('zaplings:generate_user_tags',
                        args=(request.user.pk,)))

            else:
                return redirect('zaplings:creatorsnight')
        else:
            return redirect('zaplings:creatorsnight')

    except Exception as e:
        logger.error("Error in record_need: %s (%s)",
                      e.message, str(type(e)))
        return redirect('zaplings:error')


def record_text(request):
    """
    record custom text from loves, offers, needs fields
    redirect to profile-view
    """
    try:
        userid = request.user.pk
        want_default_text = '_on_'

        if userid:
            # user-want-mic
            want_mic = request.POST['want-mic'] \
                if 'want-mic' in request.POST else ''
            logger.info('want-mic: %s', want_mic)
            if want_mic:
                want_mic_text = request.POST['want-mic-text']
                if not want_mic_text:
                    want_mic_text = want_default_text
                try:
                    LoveText.objects.create(user_id=userid, text=want_mic_text)
                except IntegrityError:
                    want_mic_new = LoveText.objects.get(user_id=userid)
                    want_mic_new.text = want_mic_text
                    want_mic_new.save()

            # want-art
            want_art = request.POST['want-art'] \
                if 'want-art' in request.POST else ''
            logger.info('want-art: %s', want_art)
            if want_art:
                want_art_text = want_default_text
                try:
                    OfferText.objects.create(user_id=userid, text=want_art_text)
                except IntegrityError:
                    want_art_new = OfferText.objects.get(user_id=userid)
                    want_art_new.text = want_art_text
                    want_art_new.save()

            # want-featured
            want_featured = request.POST['want-featured'] \
                if 'want-featured' in request.POST else ''
            logger.info('want-featured: %s', want_featured)
            if want_featured:
                want_featured_text = request.POST['want-featured-text']
                if not want_featured_text:
                    want_featured_text = want_default_text
                try:
                    NeedText.objects.create(user_id=userid, text=want_featured_text)
                except IntegrityError:
                    want_featured_new = NeedText.objects.get(user_id=userid)
                    want_featured_new.text = want_featured_text
                    want_featured_new.save()
        else:
            return redirect('zaplings:creatorsnight')

    except Exception as e:
        logger.error("Error in record_text: %s (%s)",
                      e.message, str(type(e)))
        return redirect('zaplings:error')


def get_user_tags(userid):
    # user loves
    user_loves = [
        love.love_id for love in UserLove.objects.filter(user_id=userid)]
    user_lovetags = [
        Love.objects.get(id=love_id).tagname for love_id in user_loves]
    # user offers
    user_offers = [
        offer.offer_id for offer in UserOffer.objects.filter(user_id=userid)]
    user_offertags = [
        Offer.objects.get(id=offer_id).tagname for offer_id in user_offers]
    # user needs
    user_needs = [
        need.need_id for need in UserNeed.objects.filter(user_id=userid)]
    user_needtags = [
        Need.objects.get(id=need_id).tagname for need_id in user_needs]

    # user love text
    user_lovetext = None
    try:
        user_lovetext = LoveText.objects.get(user_id=userid)
        user_lovetext = user_lovetext.text
    except Exception:
        logger.info("No love text for userid [%s]", userid)
        pass

    # user offer text
    user_offertext = None
    try:
        user_offertext = OfferText.objects.get(user_id=userid)
        user_offertext = user_offertext.text
    except Exception:
        logger.info("No offer text for userid [%s]", userid)
        pass

    # user need text
    user_needtext = None
    try:
        user_needtext = NeedText.objects.get(user_id=userid)
        user_needtext = user_needtext.text
    except Exception:
        logger.info("No need text for userid [%s]", userid)
        pass

    user_profile = {
        'user_lovetags': user_lovetags,
        'user_offertags': user_offertags,
        'user_needtags': user_needtags,
        'love_text': user_lovetext,
        'offer_text': user_offertext,
        'need_text': user_needtext
    }
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
        return render(
            request,
            'zaplings/signup.html',
            {'login_status_message': "Please enter your email!"}
        )


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
            return render(
                request,
                'zaplings/signup.html',
                {'login_status_message': "Please login to Zaplings!"}
            )
    except Exception:
        logger.info("Redirecting to login")
        request_obj = {'login_status_message': 'Please login to Zaplings!'}
        return render(request, 'zaplings/signup.html', request_obj)


def record_feedback(request):
    """
    record feedback to the database
    redirect to the index page with a status message
    """
    login_status_msg = ' '.join([
        "We'd like to be able to contact you back -",
        "please login to Zaplings!"])
    index_status_msg = ' '.join([
        "Thank you for your feedback!",
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
                FeedBack.objects.create(
                    user_id=userid,
                    feedback_type=feedback_type,
                    feedback_subject=feedback_subject,
                    feedback_response=feedback_response)
                logger.info(
                    "Recorded feedback from [%s] on %s (%s)",
                    request.user.username,
                    feedback_subject if feedback_subject else 'no subject',
                    feedback_type)
                # request.QueryDict.update({
                #     'status_message': index_status_msg})
                # return redirect('zaplings:index')
                return render(
                    request,
                    'zaplings/index.html',
                    {'status_message': index_status_msg,
                     'featured_ideas': FeaturedIdea.objects.all()}
                )
            except Exception as e:
                logger.error(
                    "Error recording feedback from [%s]: %s (%s)",
                    userid, e.message, str(type(e)))
                return redirect('zaplings:error')
        else:
            logger.error('No userid provided')
            return render(
                request,
                'zaplings/signup.html',
                {'login_status_message': login_status_msg}
            )
    except Exception as e:
        logger.info("Redirecting to login")
        request_obj = {'login_status_message': login_status_msg}
        return render(request, 'zaplings/signup.html', request_obj)


def record_new_email(request):
    try:
        email = request.POST['user-email']
        status_message = {
            'REENTER': 'Please enter your name and email',
            'EXISTS': 'You are already part of Zaplings! Thanks!',
            'SUCCESS': 'Thank you for joining Zaplings!'}

        # REENTER
        if not email or '@' not in email:
            status = 'REENTER'
            logger.info('Empty email submitted')
            request_obj = {
                'status_message': status_message[status]
            }
            # return back to index for the time-being
            return render(request, 'zaplings/creatorsnight.html', request_obj)

        # EXISTING EMAIL
        elif User.objects.filter(username=email):
            status = 'EXISTS'
            logger.info('Email [%s] has already been submitted.', email)

        # NEW USER
        else:
            try:
                newuser = User.objects.create_user(email)
                if 'user-firstname' in request.POST:
                    newuser.first_name = request.POST['user-firstname']
                if 'user-lastname' in request.POST:
                    newuser.last_name = request.POST['user-lastname']
                if not (newuser.first_name and newuser.last_name): 
                    status = 'REENTER'
                    logger.info('User first or last name missing')
                    request_obj = {
                        'status_message': status_message[status]
                    }
                    # return back to index for the time-being
                    return render(request, 'zaplings/creatorsnight.html', request_obj)
                newuser.set_password('')
                newuser.save()
                status = 'SUCCESS'
                logger.info('Created user [%s]', email)
            except IntegrityError:
                logger.warning('User [%s] already exists.', email)
                status = 'EXISTS'

        # login user
        login_email(request, email)

        # generate user tags and redirect to profile
        # return HttpResponseRedirect(
        #     reverse('zaplings:generate_user_tags',
        #     args=(request.user.pk,)))
    except Exception as e:
        logger.error(
            "Error in record_new_email: %s (%s)", e.message, str(type(e)))
        return redirect('zaplings:error')


def process_rsvp(request):
    record_new_email(request)
    # record_loves(request, isRedirected=False)
    # record_offers(request, isRedirected=False)
    # record_needs(request, isRedirected=False)
    record_text(request)
    send_confirmation_email(request)

    new_rsvp = UserRsvp.objects.create(user_id=request.user.pk)
    logger.info("New rsvp: %s", unicode(new_rsvp))

    return redirect('zaplings:rsvp-confirm')


def send_confirmation_email(request):
    try:
        email_body = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html> <head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/> <title>Zaplings - Creators&#39; Night confirmation</title> <style>@media only screen and (min-device-width: 641px){.content{width: 640px !important;}}</style></head> <body><!--[if (gte mso 9)|(IE)]> <table width="540" align="center" cellpadding="0" cellspacing="0" border="0"> <tr> <td><![endif]--> <table class="content" align="center" cellpadding="0" cellspacing="0" border="0" style="width: 100%%; max-width: 640px; font-family: Arial;"> <tr bgcolor="#05325b" style="text-align: center;"> <td valign="bottom"> <a href="http://www.zaplings.com" target="_blank"><img src="http://www.zaplings.com/static/images/logo-email.png" alt="Zaplings" width="112px" height="51px"/></a> </td></tr><tr align="left" style="color: #05325b;"> <td style="padding: 48px;"> Hi %s,<br><br>We&#39;re excited that you will be joining us for the next Creators&#39; Night. Here&#39;s a reminder of what&#39;s in store:<br><br><strong>Featured creators</strong> <ul> <li>Music by <a href="https://shanecooley.bandcamp.com/" target="_blank">Shane Cooley &amp; The Lucky Kings</a></li><li>Art by <a href="http://www.rexhamiltonart.com" target="_blank">Rex Hamilton</a></li><li>Startup founder of <a href="http://www.peepsqueeze.com" target="_blank">Peepsqueeze</a></li><li>Photography by <a href="http://www.mynameiskat.com" target="_blank">Kat Goins</a></li></ul> <strong>Opportunities for you to create</strong> <ul> <li>Express yourself with 5-minute mic time</li><li>Brainstorm at the idea table</li><li>Make art at the bARTer table</li><li>Grow friendships with connection cards</li><li>Sell or bid in the art auction</li></ul> <p>Thank you for your help in growing this community of creators. Forward this email to friends who might be interested. Remind them to Rsvp at <a href="http://www.zaplings.com/creatorsnight" target="_blank">zaplings.com/creatorsnight</a> and arrive by 6:45pm to ensure entry.</p><p>Create on!<br>The Zaplings Team</p></td></tr></table><!--[if (gte mso 9)|(IE)]> </td></tr></table><![endif]--> </body></html>'  
        zaplings_emails = [
            'nicko.shestopalov@gmail.com',
            'danny@zaplings.com',
            'dannypernik@gmail.com',
            'drpernik@gmail.com',
            'justin.cole1981@gmail.com',
        ]
    
        user_email = request.POST['user-email']
        name = request.POST['user-firstname'] or 'there'
        response = requests.post(
            "https://api.mailgun.net/v2/mg.zaplings.com/messages",
            auth=("api", "key-9c1bcab96768c19c80966e42c7882cd0"),
            data={
                "from": "Zaplings Team <postmaster@mg.zaplings.com>",
                "to": user_email,
                "subject": "See you at Creators' Night!",
                "h:Reply-To": "danny@zaplings.com",
                "html": email_body % name    
            }
        )
    
        if response.status_code == 200:
            logger.info("Email sent to:%s", user_email)
            return True
        else:
            logger.error(
                "MailGun returned %s: %s. For email: %s",
                response.status_code,
                response.text,
                user_email
            )
            return False
    except Exception as e:
        logger.error("fatal error: %s (%s)", e.message, type(e))


def signup_user(request):
    status_message = {
        'PASSWORD_VERIFY': 'Passwords do not match!',
        'PASSWORD_EMPTY': 'Please type in your password',
        'NAME_EMPTY': 'Please enter your name',
        'EMAIL_EMPTY': 'Please enter your email',
        'EMAIL_EXISTS': 'User is already registered with this email',
        'USERNAME_EMPTY': 'Please pick a username',
        'USERNAME_EXISTS': 'This username already exists',
        'USER_UPDATED': 'Thank you for joining Zaplings!',
        'USER_CREATED': 'Thank you for joining Zaplings!'}
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

        failure_keys = [
            key for key in status_message.keys() if 'USER_' not in key]

        if status not in failure_keys:
            if User.objects.filter(username=email):
                user = User.objects.get(username=email)
                user.username = username
                user.email = email
                status = 'USER_UPDATED'
            else:
                user = User.objects.create_user(
                    username=username,
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
            return HttpResponseRedirect(
                reverse(
                    'zaplings:generate_user_tags',
                    args=(request.user.pk,)
                )
            )
        else:
            request_obj = {'signup_status_message': status_message[status]}
            return render(request, 'zaplings/signup.html', request_obj)
    except Exception as e:
        request_obj = {'status_message': e.message}
        # return back to index for the time-being
        return render(request, 'zaplings/signup.html', request_obj)


def login_email(request, email):
    user = authenticate(username=email, password='')
    # extra check enforced for active users
    if user is not None and user.is_active:
        login(request, user)
        logger.info('Logged in [%s]', email)


def login_email_password(request):
    status_message = {
        'LOGIN_INCORRECT': "The login information you provided did not match our records. Please try again.",
        'LOGIN_INCOMPLETE': "Please include both email and password."
    }
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
        # return render(request, 'zaplings/profile.html', user_tags)
        return HttpResponseRedirect(
            reverse('zaplings:generate_user_tags', args=(request.user.pk,)))


def user_logout(request):
    status_msg = None
    try:
        username = request.user.username
        if request.user.is_authenticated():
            logout(request)
            logger.info('Logged out [%s]', username)
            status_msg = "You've been succesfully logged out!"
        else:
            status_msg = ' '.join([
                "You're not logged in.",
                "Please enter your email to enter Zaplings!"])
    except Exception:
        logger.error('Could not log out user [%s]', username)

    request_obj = {
        'featured_ideas': FeaturedIdea.objects.all(),
        'status_messge': status_msg,
    }
    return render(request, 'zaplings/index.html', request_obj)

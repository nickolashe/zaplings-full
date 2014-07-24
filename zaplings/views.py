from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from zaplings.models import FeaturedIdea, Love, Offer, Need, UserLove, UserOffer, UserNeed, NewUserEmail
from django.template import RequestContext, loader
from django.views import generic
from django.db import IntegrityError
import time
import logging

logging.basicConfig(level=logging.DEBUG, filename="logs/views.log")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

#def index(request):
    #latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('polls/index.html')
    #context = RequestContext(request, {
    #    'latest_poll_list': latest_poll_list,
    #})
    #context = {'latest_poll_list': latest_poll_list}
    #return render(request, 'polls/index.html', context)
    #return HttpResponse(template.render(context))
    #output = ', '.join([p.question for p in latest_poll_list])
class SignupView(generic.ListView):
    model = User
    template_name = 'zaplings/signup.html'

    #def get_queryset(self):
    #    """Return the last five published polls."""
    #    return Poll.objects.order_by('-pub_date')[:5]

class ProfileView(generic.ListView):
    model = User
    template_name = 'zaplings/profile.html'

    #def get_queryset(self):
    #    """Return the last five published polls."""
    #    return Poll.objects.order_by('-pub_date')[:5]

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

class LovesView(generic.ListView):
    template_name = 'zaplings/loves.html'
    context_object_name = 'suggested_loves'

    def get_queryset(self):
        """Return the all suggested loves."""
        return Love.objects.all()
    
class OffersView(generic.ListView):
    template_name = 'zaplings/offers.html'
    context_object_name = 'suggested_offers'

    def get_queryset(self):
        """Return the all suggested offers."""
        return Offer.objects.all()
    
class NeedsView(generic.ListView):
    template_name = 'zaplings/needs.html'
    context_object_name = 'suggested_needs'

    def get_queryset(self):
        """Return the all suggested needs."""
        return Need.objects.all()

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

class ViewProfileHtmlView(generic.ListView):
    model = User
    template_name = 'zaplings/profile-view-html-only.html'

class IndexView(generic.ListView):
    #model = FeaturedIdea
    template_name = 'zaplings/index.html'
    context_object_name = 'featured_ideas'

    def get_queryset(self):
        """Return the all features ideas."""
        return FeaturedIdea.objects.all()

#def detail(request, poll_id):
    #poll = Poll.objects.get(id=poll_id)
    #context = {'poll': poll}
    #return render(request, 'polls/detail.html', context)
    #return HttpResponse("You're looking at poll %s." % poll_id)

#def results(request, poll_id):
    #poll = get_object_or_404(Poll, pk=poll_id)
    #return render(request, 'polls/results.html', {'poll': poll})

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
    if request.method == "POST":
        logger.info(request.POST)
        love_ids = request.POST.getlist(u'love-tag')
        logger.info("Selected love ids: %s", str(love_ids))
        selected_loves = [ Love.objects.get(id=love_id).tagname \
                           for love_id in love_ids ]
        logger.info("Selected love tags: %s", str(selected_loves))
        
        userid = request.user.pk
        logger.info("Current session userid: [%s]", request.user.username) 
    
        for love_id in love_ids:
            if not UserLove.objects.filter(user_id=request.user.pk, love_id=love_id):
                UserLove.objects.create(user_id=request.user.pk, love_id=love_id)
        # user loves
        #user_loves = [love.love_id for love in UserLove.objects.filter(user_id=userid)]
        #user_lovetags = [Love.objects.get(id=love_id).tagname for love_id in user_loves]
        #return render(request, 'zaplings/profile-text.html', {
        #    'user_lovetags': user_lovetags
        #})
        suggested_offers = Offer.objects.all()
        return render(request, 'zaplings/offers.html', {
            'suggested_offers': suggested_offers
        })
    else:
        return redirect('zaplings:loves')

def record_offers(request):
    if request.method == "POST":
        logger.info(request.POST)
        offer_ids = request.POST.getlist(u'offer-tag')
        logger.info("Selected offer ids: %s", str(offer_ids))
        selected_offers = [ Offer.objects.get(id=offer_id).tagname \
                           for offer_id in offer_ids ]
        logger.info("Selected offer tags: %s", str(selected_offers))
        
        userid = request.user.pk
        logger.info("Current session userid: [%s]", request.user.username) 
    
        for offer_id in offer_ids:
            if not UserOffer.objects.filter(user_id=request.user.pk, offer_id=offer_id):
                UserOffer.objects.create(user_id=request.user.pk, offer_id=offer_id)
        # user loves
        #user_loves = [love.love_id for love in UserLove.objects.filter(user_id=userid)]
        #user_lovetags = [Love.objects.get(id=love_id).tagname for love_id in user_loves]
        # user offers
        #user_offers = [offer.offer_id for offer in UserOffer.objects.filter(user_id=userid)]
        #user_offertags = [Offer.objects.get(id=offer_id).tagname for offer_id in user_offers]
        #return render(request, 'zaplings/profile-text.html', {
        #    'user_lovetags': user_lovetags,
        #    'user_offertags': user_offertags
        #})
        suggested_needs = Need.objects.all()
        return render(request, 'zaplings/needs.html', {
            'suggested_needs': suggested_needs
        })
    else:
        return redirect('zaplings:loves')

def record_needs(request):
    if request.method == "POST":
        logger.info('POST request: %s', str(request.POST))
        need_ids = request.POST.getlist(u'need-tag')
        logger.info("Selected need ids: %s", str(need_ids))
        selected_needs = [ Need.objects.get(id=need_id).tagname \
                           for need_id in need_ids ]
        logger.info("Selected need tags: %s", str(selected_needs))
        
        userid = request.user.pk
        logger.info("Current session userid: [%s]", request.user.username) 
    
        for need_id in need_ids:
            if not UserNeed.objects.filter(user_id=request.user.pk, need_id=need_id):
                UserNeed.objects.create(user_id=request.user.pk, need_id=need_id)
        # user loves
        user_loves = [love.love_id for love in UserLove.objects.filter(user_id=userid)]
        user_lovetags = [Love.objects.get(id=love_id).tagname for love_id in user_loves]
         # user offers
        user_offers = [offer.offer_id for offer in UserOffer.objects.filter(user_id=userid)]
        user_offertags = [Offer.objects.get(id=offer_id).tagname for offer_id in user_offers]
        # user needs
        user_needs = [need.need_id for need in UserNeed.objects.filter(user_id=userid)]
        user_needtags = [Need.objects.get(id=need_id).tagname for need_id in user_needs]
        return render(request, 'zaplings/profile-text.html', {
            'user_lovetags': user_lovetags,
            'user_offertags': user_offertags,
            'user_needtags': user_needtags
        })
    else:
        logger.info('GET request: %s', str(request.GET))
        return redirect('zaplings:loves')

def record_new_email(request):
    email = request.POST['email']
    status_message = {'REENTER': 'Please enter your email.',
                      'EXISTS': 'You are already part of Zaplings! Thanks!',
                      'SUCCESS': 'Thank you for joining Zaplings!'}
    # REENTER
    if not email or email == "" or not '@' in email:
        status = 'REENTER'
        logger.info('Empty email submitted')
    # EXISTS
    elif NewUserEmail.objects.filter(email=email):
        logger.info('Email [%s] has already been submitted.', email)
        # create django user if needed
        if not User.objects.filter(username=email):
            newuser = User.objects.create_user(email)
            newuser.set_password('')
            newuser.save()
            logger.info('Created user [%s]', email)
        login_email(request, email)
        status = 'EXISTS'
    # NEW
    else:
        # create new user (email, '')
        NewUserEmail.objects.create(email=email)
        newuser = None
        try:
            newuser = User.objects.create_user(email)
            newuser.set_password('')
            newuser.save()
            status= 'SUCCESS'
            logger.info('Created user [%s]', email)
        except IntegrityError:
            logger.info('User [%s] already exists.', email)
            status = 'EXISTS'
        login_email(request, email)
    
    request_obj = { 'featured_ideas': FeaturedIdea.objects.all(),
                    'status_message': status_message[status] }
    # return back to index for the time-being
    return render(request, 'zaplings/index.html', request_obj) 
           #if status == 'REENTER' else \
           #redirect('/loves/')

def login_email(request, email):
    user = authenticate(username=email, password='')
    # extra check enforced for active users
    if user is not None and user.is_active:
        login(request, user)
        logger.info('Logged in [%s]', email)

def login_email_password(request):
    error_message = None
    try:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request, user)
                success_message = "User %s is valid, active and authenticated"
            else:
                success_message = "The password is valid, but the account %s has been disabled!"
        else:
            # the authentication system was unable to verify the username and password
            error_message = "The username and password were incorrect."

    except (KeyError, User.DoesNotExist):
        # Redisplay the poll voting form.
        error_message = "Please include both email and password."

    if '@' not in email or len(email.split('.')) == 1:
        error_message = "Are you serious? What kind of email is this: %s?" % email

    if error_message:
        return render(request, 'zaplings/signup.html', {
            'error_message': error_message,
        })
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        #return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
        #p = get_object_or_404(User, pk=user_id)
        #return HttpResponse(success_message % email)
        
        return render(request, 'zaplings/profile-love.html', {
            'username': user.get_username()
        })

        #return HttpResponseRedirect(reverse('polls:profile', args=(user.id,)))

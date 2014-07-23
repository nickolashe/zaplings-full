from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from zaplings.models import FeaturedIdea, Love, Offer, Need, UserLove, NewUserEmail
from django.template import RequestContext, loader
from django.views import generic
from django.db import IntegrityError
import time
import logging

logging.basicConfig(level=logging.DEBUG, filename="/tmp/views.log")

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
    #return HttpResponse(output)
    #return HttpResponse("Hello, world. You're at the poll index.")
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
    
class RecordLovesView(generic.ListView):
    template_name = 'zaplings/record_loves.html'
    context_object_name = 'selected_loves'

class OffersView(generic.ListView):
    template_name = 'zaplings/offers.html'
    context_object_name = 'suggested_offers'

    def get_queryset(self):
        """Return the all suggested offers."""
        return Offer.objects.all()
    
class RecordOffersView(generic.ListView):
    template_name = 'zaplings/record_offers.html'
    context_object_name = 'selected_offers'

class NeedsView(generic.ListView):
    template_name = 'zaplings/needs.html'
    context_object_name = 'suggested_needs'

    def get_queryset(self):
        """Return the all suggested needs."""
        return Need.objects.all()

class RecordNeedsView(generic.ListView):
    template_name = 'zaplings/record_needs.html'
    context_object_name = 'selected_needs'
    
class RecordNewEmailView(generic.ListView):
    model = User    
    template_name = 'zaplings/index.html'
    
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
        print "request is POST"
        logger.info("request is POST")
        print request.POST
        logger.info(request.POST)
        logger.info(request.POST.getlist(u'love-tag'))
        selected_loves = [ Love.objects.get(id=love_id).tagname \
                           for love_id in request.POST.getlist(u'love-tag') ]
    else:
        print "request is not POST"
        logger.info("request is not POST")
        selected_loves = ["NOT POST"]
    print selected_loves
    logger.info(selected_loves)

    return render(request, 'zaplings/profile-text.html', {
    'selected_loves': selected_loves
    })

def record_new_email(request):
    email = request.POST['email']
    status_message = {'REENTER': 'Please enter your email.',
                      'EXISTS': 'You are already part of Zaplings! Thanks!',
                      'SUCCESS': 'Thank you for joining Zaplings!'}

    if not email or email == "" or not '@' in email:
        status = 'REENTER'
        logger.info('Empty email submitted')
    elif NewUserEmail.objects.filter(email=email):
        logger.info('User [%s] already exists.', email)
        login_email(request, email)
        status = 'EXISTS'
    else:
        # create new user (email, '')
        NewUserEmail.objects.create(email=email)
        newuser = None
        try:
            newuser = User.objects.create_user(email)
            newuser.set_password('')
            newuser.save()
            status= 'SUCCESS'
            logger.info('Create user [%s]', email)
        except IntegrityError:
            logger.info('User [%s] already exists.', email)
            status = 'EXISTS'
        login_email(request, email)
              
    return render(request, 'zaplings/index.html', {
        'status_message': status_message[status],
        'featured_ideas': FeaturedIdea.objects.all()
    })

def login_email(request, email):
    user = authenticate(username=email, password='')
    # extra check enforces for active users
    if user is not None and user.is_active:
        login(request, user)
        logger.info('Logged in [%s]')

def login(request):
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
            'username': user.get_username(),
            'user': user
        })

        #return HttpResponseRedirect(reverse('polls:profile', args=(user.id,)))



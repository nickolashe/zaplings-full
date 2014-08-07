from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from zaplings.models import FeaturedIdea, Love, Offer, Need, UserLove, UserOffer, UserNeed, LoveText, OfferText, NeedText, NewUserEmail, Where, When
from django.template import RequestContext, loader
from django.views import generic
from django.db import IntegrityError
import time
import logging

logging.basicConfig(level=logging.DEBUG, filename="logs/views.log")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class SignupView(generic.ListView):
    model = User
    template_name = 'zaplings/signup.html'

class ProfileView(generic.ListView):
    context_object_name = 'user_tags'    
    template_name = 'zaplings/profile.html'
    queryset = Love.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user_tags = generate_user_tags(request.user.pk)
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

class WhereView(generic.ListView):
    model = User    
    template_name = 'zaplings/where.html'

class WhenView(generic.ListView):
    model = User    
    template_name = 'zaplings/when.html'

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

class WhenView(generic.ListView):
    model = User
    template_name = 'zaplings/when.html'

class WhereView(generic.ListView):
    model = User
    template_name = 'zaplings/where.html'

class IndexView(generic.ListView):
    #model = FeaturedIdea
    template_name = 'zaplings/index.html'
    context_object_name = 'featured_ideas'

    def get_queryset(self):
        """Return the all features ideas."""
        return FeaturedIdea.objects.all()

class ErrorView(generic.ListView):
    model = User
    template_name = 'zaplings/error.html'

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
        user_tags = generate_user_tags(request, userid)
        return render(request, 'zaplings/profile.html', user_tags)
    else:
        logger.info('GET request: %s', str(request.GET))
        return redirect('zaplings:loves')

def record_whens(request):
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
            if post.has_key('meet-local') and post['meet-local'] == 'on':
                logger.info("meet-local is set") 
   
            user_tags = generate_user_tags(request, userid)
            return render(request, 'zaplings/profile.html', user_tags)
        else:
            logger.info('GET request: %s', str(request.GET))
            return redirect('zaplings:loves')
    except Exception as e:
        logger.error("Error in record_whens: %s (%s)",
                      e.message, str(type(e)))
        return redirect('zaplings:error')

def record_wheres(request):
    """
    process input from zaplings:where
    redirect to zaplings:profile
    """
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

def record_text(request):
    userid = request.user.pk
    logger.info("Recording text's for userid [%s]", userid)
    love_text = request.POST['love_text']
    offer_text = request.POST['offer_text']
    need_text = request.POST['need_text']
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
    request_obj = get_user_tags(userid)
    request_obj.update({'love_text': love_text,
                        'offer_text': offer_text,
                        'need_text': need_text
                       })
    return render(request, 'zaplings/profile-view.html', request_obj)

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
    user_tags =  { 'user_lovetags': user_lovetags,
                   'user_offertags': user_offertags,
                   'user_needtags': user_needtags }
    return user_tags    

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

def record_new_email(request):
    email = request.POST['email']
    status_message = {'REENTER': 'Please enter your email.',
                      'EXISTS': 'You are already part of Zaplings! Thanks!',
                      'SUCCESS': 'Thank you for joining Zaplings!'}
    # REENTER
    if not email or email == "" or not '@' in email:
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
        NewUserEmail.objects.create(email=email)
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
            logger.info('User [%s] already exists.', email)
            status = 'EXISTS'
        login_email(request, email)
        # generate user tags and redirect to profile
        return HttpResponseRedirect(reverse('zaplings:generate_user_tags', args=(request.user.pk,)))
             

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
            # return back to index for the time-being
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
            logger.info(auth_message)
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
    except Exception as e:
        logger.info('Could not log out user [%s]', username)

    request_obj = { 'featured_ideas': FeaturedIdea.objects.all(),
                    'status_message': status_msg }
    # return back to index for the time-being
    return render(request, 'zaplings/index.html', request_obj) 




from django.conf.urls import patterns, url

from zaplings import views

urlpatterns = patterns('',
    url(r'^/?$', views.IndexView.as_view(), name='index'),
    # user login/signup 
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^signup_user/$', views.signup_user, name='signup_user'),
    url(r'^login_email_password/$', views.login_email_password, name='login_email_password'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    # profiles
    url(r'^profile/(?P<pk>\d+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^profile-text/$', views.ProfileTextView.as_view(), name='profile-text'),
    url(r'^profile-view/$', views.ViewProfileView.as_view(), name='profile-view'),
    # user tags
    url(r'^loves/$', views.LovesView.as_view(), name='loves'),
    url(r'^offers/$', views.OffersView.as_view(), name='offers'),
    url(r'^creatorsnight/$', views.RsvpView.as_view(), name='creatorsnight'),
    url(r'^rsvp-confirm/$', views.RsvpConfirmView.as_view(), name='rsvp-confirm'),
    url(r'^(?P<userid>\d+)/generate_user_tags/$', views.generate_user_tags, name='generate_user_tags'),
    url(r'^generate_profile/$', views.generate_profile, name='generate_profile'),
    # form handlers
    url(r'^record_loves/$', views.record_loves, name='record_loves'),
    url(r'^record_offers/$', views.record_offers, name='record_offers'),
    url(r'^record_needs/$', views.record_needs, name='record_needs'),
    url(r'^record_new_email/$', views.record_new_email, name='record_new_email'),
    url(r'^record_text/$', views.record_text, name='record_text'),
    url(r'^record_feedback/$', views.record_feedback, name='record_feedback'),
    url(r'^process-rsvp/$', views.process_rsvp, name='process-rsvp'),
    # menu links
    url(r'^10-reasons/$', views.AboutView.as_view(), name='10-reasons'),
    url(r'^howitworks/$', views.HowItWorksView.as_view(), name='howitworks'),
    url(r'^getinvolved/$', views.GetInvolvedView.as_view(), name='getinvolved'),
    url(r'^faq/$', views.FaqView.as_view(), name='faq'),
    url(r'^discuss/$', views.DiscussView.as_view(), name='discuss'),
    # idea stuff
    url(r'^idea-feed/$', views.IdeaFeedView.as_view(), name='idea-feed'),
    url(r'^newidea/$', views.NewIdeaView.as_view(), name='newidea'),
    url(r'^myideas/$', views.MyIdeasView.as_view(), name='myideas'),
    url(r'^view-idea-page/$', views.ViewIdeaPageView.as_view(), name='view-idea-page'),
    url(r'^edit-idea-page/$', views.EditIdeaPageView.as_view(), name='edit-idea-page'),
    url(r'^editprofile/$', views.EditProfileView.as_view(), name='editprofile'),
    url(r'^share/$', views.ShareView.as_view(), name='share'),
    url(r'^thankyou/$', views.ThankYouView.as_view(), name='thankyou'),
    url(r'^error/$', views.ErrorView.as_view(), name='error'),
    url(r'^jet/$', views.JetView.as_view(), name='jet'),
    url(r'^jet-edit/$', views.JetEditView.as_view(), name='jet-edit')
    #url(r'^(?P<referrer>\w+)/$', views.referrer, name='referrer')
)

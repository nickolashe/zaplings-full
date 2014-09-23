from django.contrib import admin
from zaplings.models import Idea, FeaturedIdea, IdeaType, IdeaTeam, Love, Offer, Need, UserLove, UserOffer, UserNeed, LoveText, OfferText, NeedText, Where, When, FeedBack, Referrer

# Register your models here.
admin.site.register(Idea)
admin.site.register(IdeaType)
admin.site.register(IdeaTeam)
admin.site.register(FeaturedIdea)
admin.site.register(Love)
admin.site.register(Offer)
admin.site.register(Need)
admin.site.register(UserLove)
admin.site.register(UserOffer)
admin.site.register(UserNeed)
admin.site.register(LoveText)
admin.site.register(OfferText)
admin.site.register(NeedText)
admin.site.register(Where)
admin.site.register(When)
admin.site.register(FeedBack)
admin.site.register(Referrer)

from django.contrib import admin
from zaplings.models import Idea, FeaturedIdea, Love, Offer, Need, UserLove, UserOffer, UserNeed

# Register your models here.
admin.site.register(Idea)
admin.site.register(FeaturedIdea)
admin.site.register(Love)
admin.site.register(Offer)
admin.site.register(Need)
admin.site.register(UserLove)
admin.site.register(UserOffer)
admin.site.register(UserNeed)


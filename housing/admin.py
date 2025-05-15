from django.contrib import admin

# Register your models here.

from .models import *
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Accommodation)
admin.site.register(AccommodationImage)
admin.site.register(Booking)
admin.site.register(ReviewDetails)
admin.site.register(Review)
admin.site.register(LandlordSubscription)
admin.site.register(PropertyVerificationDocument)
admin.site.register(Profile)
admin.site.register(Message)
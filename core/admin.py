from django.contrib import admin

from .models import Nonprofitcharities
from .models import Ourlateststory
from .models import Gallary
from .models import Contactus
from .models import Auth_user_profile
from .models import Gender
from .models import BloodGroup
from .models import Donation
from .models import DonationType
from .models import UpcomingEvents
from .models import Subscribe
from .models import Objectives
from .models import ImageGallary
from .models import Questions
from .models import CharityType
from .models import Information
from .models import BloodStatus
from .models import AvailableBloodGroup



admin.site.register(Nonprofitcharities)
admin.site.register(Ourlateststory)
admin.site.register(Gallary)
admin.site.register(Contactus)
admin.site.register(Auth_user_profile)
admin.site.register(Gender)
admin.site.register(BloodGroup)
admin.site.register(Donation)
admin.site.register(DonationType)
admin.site.register(UpcomingEvents)
admin.site.register(Subscribe)
admin.site.register(Objectives)
admin.site.register(ImageGallary)
admin.site.register(Questions)
admin.site.register(CharityType)
admin.site.register(Information)
admin.site.register(BloodStatus)
admin.site.register(AvailableBloodGroup)


# Start => for set Auth_user_profile table inside auth_user
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class Auth_user_profileInline(admin.StackedInline):
    model = Auth_user_profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = [Auth_user_profileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# End => for set Auth_user_profile table inside auth_user

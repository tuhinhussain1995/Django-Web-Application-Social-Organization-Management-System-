from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Ourlateststory(models.Model):
    img = models.ImageField(upload_to='homePageOurLatestStory/%Y/%m/%d/')
    date = models.DateField()
    location = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=10000)


class Gallary(models.Model):
    img = models.ImageField(upload_to='homePageGallary/%Y/%m/%d/')

class Contactus(models.Model):
    location = models.CharField(max_length=100)
    phone1 = models.CharField(max_length=12)
    phone2 = models.CharField(max_length=12)
    email1 = models.EmailField()
    email2 = models.EmailField()


class Gender(models.Model):
    gender_type = models.CharField(max_length=10)

    def __str__(self):
        return self.gender_type

class BloodGroup(models.Model):
    blood_type = models.CharField(max_length=10)

    def __str__(self):
        return self.blood_type


class Auth_user_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    is_user = models.BooleanField(default=True)
    is_volunteer = models.BooleanField(default=False)
    address = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    profession = models.CharField(max_length=100, blank=True)
    educational_bg = models.CharField(max_length=100, blank=True)
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.SET_NULL, null=True)
    picture = models.ImageField(upload_to='profilePictures/%Y/%m/%d/', max_length=255, blank=True, default='profilePictures/user.png')
    facebook = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    whatsapp = models.CharField(max_length=100, blank=True)


    def __str__(self):
        if self.user.is_superuser and self.user.is_staff:
            return "{0} {1} {2} {3} {4}".format('Admin', '==>', 'Staff', '==>', self.user.username)
        elif self.user.is_superuser:
            return "{0} {1} {2}".format('Admin', '==>', self.user.username)
        elif self.user.is_staff:
            return "{0} {1} {2} {3} {4}".format('Staff', '==>', self.full_name, '==>', self.user.email)
        else:
            return "{0} {1} {2} {3} {4}".format(self.user.id, '==>', self.user.username, '==>', self.user.email)


class DonationType(models.Model):
    typeName = models.CharField(max_length=300)

    def __str__(self):
        return self.typeName


class Donation(models.Model):
    amount = models.FloatField()
    donation_date = models.DateTimeField(default=datetime.now)
    donationType = models.ForeignKey(DonationType, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{0} {1} {2} {3} {4}".format(self.user.id, '==>', self.amount, '==>', self.donation_date)


class UpcomingEvents(models.Model):
     img = models.ImageField(upload_to='homePageUpcomingEvents/%Y/%m/%d/')
     title = models.CharField(max_length=300)
     smallDesc = models.CharField(max_length=300)
     goal = models.IntegerField(blank=True, null=True)

     def __str__(self):
         return self.title


class Subscribe(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email


class Objectives(models.Model):
    img = models.ImageField(upload_to='majorObjectives/%Y/%m/%d/')
    title = models.CharField(max_length=300)
    smallDesc = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class ImageGallary(models.Model):
    img = models.ImageField(upload_to='imageGallary/%Y/%m/%d/')
    grid = models.IntegerField(default=4)



class Questions(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    question = models.CharField(max_length=300)
    question_date = models.DateTimeField(default=datetime.now)
    answer = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return "{0} {1} {2} {3} {4} {5} {6}".format(self.name, '==>', self.email, '==>', self.subject, '==>', self.answer)



class CharityType(models.Model):
    type_name = models.CharField(max_length=300)

    def __str__(self):
        return self.type_name


class Nonprofitcharities(models.Model):
    img = models.ImageField(upload_to='homePageNonProfitCharitiesPic/%Y/%m/%d/')
    title = models.CharField(max_length=100)
    smallDesc = models.CharField(max_length=1000)
    CharityType = models.ForeignKey(CharityType, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{0} {1} {2} {3} {4}".format(self.id, '==>', self.title, '==>', self.CharityType)



class Information(models.Model):
    img = models.ImageField(upload_to='information/%Y/%m/%d/')
    title = models.CharField(max_length=300)
    location = models.CharField(max_length=300)
    date = models.DateTimeField(default=datetime.now)
    desc = models.CharField(max_length=9000)
    CharityType = models.ForeignKey(CharityType, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{0} {1} {2} {3} {4}".format(self.id, '==>', self.title, '==>', self.CharityType)


class TempInfo(models.Model):
    typeNo = models.IntegerField(blank=True)


class TempSearch(models.Model):
    searchTitle = models.CharField(max_length=300)



class BloodStatus(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class AvailableBloodGroup(models.Model):
    blood_donor_id = models.IntegerField(blank=True, null=True)
    blood_donor_name = models.CharField(max_length=100, blank=True)
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.SET_NULL, null=True)
    doonation_date = models.DateTimeField(default=datetime.now)
    expire_date = models.DateTimeField(default=datetime.now)
    receiver_id = models.CharField(max_length=100, blank=True)
    receiver_name = models.CharField(max_length=100, blank=True)
    apply_date = models.DateTimeField(blank=True, null=True)
    status = models.ForeignKey(BloodStatus, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}".format(self.id, '==>', self.blood_group, '==>', self.doonation_date, '==>', self.expire_date, '==>', self.status , '==>', self.receiver_id)

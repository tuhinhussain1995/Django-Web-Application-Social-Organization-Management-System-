from django.shortcuts import render, redirect

from django.contrib.auth.models import User, auth
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q

from .models import Nonprofitcharities
from .models import Ourlateststory
from .models import Gallary
from .models import Contactus
from .models import Auth_user_profile
from .models import Donation
from .models import DonationType
from .models import UpcomingEvents
from .models import Subscribe
from .models import Objectives
from .models import ImageGallary
from .models import Questions
from .models import Information
from .models import CharityType
from .models import TempInfo
from .models import TempSearch
from .models import BloodStatus
from .models import AvailableBloodGroup


from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required


def volenteerForm(request):
    current_user = request.user

    if current_user.id is not None:
        return redirect('volenteer')
    else:
        return render(request, 'volenteerForm.html')



def volenteer(request):
    current_user = request.user

    charities = Nonprofitcharities.objects.all()
    stories = Ourlateststory.objects.all()
    upcoming = UpcomingEvents.objects.all()
    gallaries = Gallary.objects.all()
    contacts = Contactus.objects.all()

    educationDonation2 = Donation.objects.filter(donationType_id=2).aggregate(Sum('amount'))
    eduDon2 = educationDonation2['amount__sum']

    educationDonation3 = Donation.objects.filter(donationType_id=3).aggregate(Sum('amount'))
    eduDon3 = educationDonation3['amount__sum']

    educationDonation4 = Donation.objects.filter(donationType_id=4).aggregate(Sum('amount'))
    eduDon4 = educationDonation4['amount__sum']


    educationDonor2 = Donation.objects.filter(donationType_id=2).count()
    educationDonor3 = Donation.objects.filter(donationType_id=3).count()
    educationDonor4 = Donation.objects.filter(donationType_id=4).count()

    mess = 'abc'

    if current_user.id is not None:
        user = Auth_user_profile.objects.filter(user_id=current_user.id).update(is_volunteer=1)

        mess = 'volenteerSuccessful'
        return render(request, 'index.html', {'mess': mess, 'charities' : charities, 'stories' : stories, 'upcoming': upcoming, 'gallaries' : gallaries, 'contacts' : contacts, 'eduDon2': eduDon2, 'educationDonor2':educationDonor2, 'eduDon3': eduDon3, 'educationDonor3':educationDonor3, 'eduDon4': eduDon4, 'educationDonor4':educationDonor4})



    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1==password2:
                if User.objects.filter(username=username).exists():
                    user = auth.authenticate(username=username, password=password1)
                    if user is not None:
                        auth.login(request, user)

                        current_user = request.user
                        auth_user = Auth_user_profile.objects.filter(user_id=current_user.id).update(is_volunteer=1)

                        mess = 'volenteerSuccessful'
                        return render(request, 'index.html', {'mess': mess, 'charities' : charities, 'stories' : stories, 'upcoming': upcoming, 'gallaries' : gallaries, 'contacts' : contacts, 'eduDon2': eduDon2, 'educationDonor2':educationDonor2, 'eduDon3': eduDon3, 'educationDonor3':educationDonor3, 'eduDon4': eduDon4, 'educationDonor4':educationDonor4})


                    else:
                        messages.info(request, 'Username already exists')
                        return redirect('volenteerForm')

                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already exists')
                    return redirect('volenteerForm')
                else:
                    user = User.objects.create_user(username=username, password=password1, email=email)
                    user.save();

                    user = auth.authenticate(username=username, password=password1)

                    auth.login(request, user)

                    current_user = request.user
                    user_profile = Auth_user_profile.objects.create(is_user=1, is_volunteer=1, user_id = current_user.id)
                    user_profile.save();

                    mess = 'volenteerSuccessful'
                    return render(request, 'index.html', {'mess': mess, 'charities' : charities, 'stories' : stories, 'upcoming': upcoming, 'gallaries' : gallaries, 'contacts' : contacts, 'eduDon2': eduDon2, 'educationDonor2':educationDonor2, 'eduDon3': eduDon3, 'educationDonor3':educationDonor3, 'eduDon4': eduDon4, 'educationDonor4':educationDonor4})


            else:
                messages.info(request, 'Please, Enter Same Password')
                return redirect('volenteerForm')
        else:
            return render(request, 'volenteerForm.html')



from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from .utils import render_to_pdf

class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('invoice.html')

        current_user = request.user
        auth_user_profile = Auth_user_profile.objects.filter(user_id = current_user.id)
        users = User.objects.filter(id = current_user.id)


#############################################################################################################
        authUP = Auth_user_profile.objects.filter(user_id = current_user.id).values_list()
        myList3 = list(authUP)
        print("*******************************************")
        print(myList3)
        print(myList3[0][1])
############################################################################################################

        availableBG = AvailableBloodGroup.objects.filter(receiver_id = myList3[0][0], status_id=3)



        pdf = render_to_pdf('invoice.html', {'auth_user_profile' : auth_user_profile, 'users': users, 'availableBG':availableBG})

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")



def receiveBlood(request):
    current_user = request.user

    if current_user.id is not None:
        return render(request, 'receiverBloodForm.html')
    else:
        return render(request, 'register.html')


def receiveBloodSuccessful(request):
    current_user = request.user

    bloodGroup = request.POST['bloodGroup']

    if bloodGroup == "Blood Group":
        messages.info(request, 'Please Sir')
        messages.info(request, 'Enter a Valid Blood Group')
        return redirect('receiveBlood')

    BGID = 0

    if bloodGroup == "A+":
        BGID = 1
    elif bloodGroup == "A-":
        BGID = 2
    elif bloodGroup == "B+":
        BGID = 3
    elif bloodGroup == "B-":
        BGID = 4
    elif bloodGroup == "AB+":
        BGID = 5
    elif bloodGroup == "AB-":
        BGID = 6
    elif bloodGroup == "O+":
        BGID = 7
    elif bloodGroup == "O-":
        BGID = 8

#########################################################################################################
#########################################################################################################

    current_user = request.user

    currUser = Auth_user_profile.objects.filter(user_id=current_user.id).values_list()
    myList = list(currUser[0])
    print(myList[2])

##############################################################################################

    availBlood = AvailableBloodGroup.objects.filter(blood_group_id=BGID).values_list()
    myList2 = list(availBlood)
    print(myList2)

    myVal = 0

    for x in myList2:
        if x[9] == 1 and x[3]==BGID:
            myVal = x[0]
            break

#############################################################################################################
    authUP = Auth_user_profile.objects.filter(user_id = current_user.id).values_list()
    myList3 = list(authUP)

    print(myList3)
    print(myList3[0][1])
############################################################################################################

    abc = AvailableBloodGroup.objects.filter(receiver_id=myList3[0][0]).values_list()
    myList5 = list(abc)
    print(myList5)

    myboolean = False

    for x in myList5:
        if x[9] == 3:
            myboolean = True
            break

    if myboolean:
        messages.info(request, 'Sorry Sir !!!')
        messages.info(request, 'You Have to Collect Your Previous Order First.')
        messages.info(request, 'Then You Can Apply For New Order.')
        return redirect('receiveBlood')


    import datetime
    now = datetime.datetime.now()

##########################################################################################################
#########################################################################################################

    if myVal == 0:
        messages.info(request, 'Sorry Sir !!!')
        messages.info(request, 'Your Expected Blood Group Is Currently Unavailable :(')
        return redirect('receiveBlood')
    else:
        user = AvailableBloodGroup.objects.filter(id=myVal).update(receiver_id=myList[0], receiver_name=myList[2], status_id=3, apply_date=now)

        return redirect('/pdf')


#    if AvailableBloodGroup.objects.filter(blood_group=BGID).exists():
#        user = AvailableBloodGroup.objects.filter(blood_group=BGID).update(receiver_id=current_user.id, receiver_name=myList[2])
#
#        return redirect('/pdf')



def donationForm(request):
    current_user = request.user

    if current_user.id is not None:
        return render(request, 'donationForm.html')
    else:
        return render(request, 'newDonorRegistration.html')


def donationForm2(request):
    current_user = request.user

    if current_user.id is not None:
        return render(request, 'donationForm2.html')
    else:
        return render(request, 'newDonorRegistration2.html')


def donationForm3(request):
    current_user = request.user

    if current_user.id is not None:
        return render(request, 'donationForm3.html')
    else:
        return render(request, 'newDonorRegistration3.html')


def donationForm4(request):
    current_user = request.user

    if current_user.id is not None:
        return render(request, 'donationForm4.html')
    else:
        return render(request, 'newDonorRegistration4.html')



def donate(request):
    current_user = request.user

    if current_user.id is not None:
        if request.method == 'POST':
            amount = request.POST['amount']

            return render(request, 'donate.html', {'totalAmount': amount})

        else:
            return render(request, 'donationForm.html')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            amount = request.POST['amount']

            if password1==password2:
                if User.objects.filter(username=username).exists():
                    user = auth.authenticate(username=username, password=password1)
                    if user is not None:
                        auth.login(request, user)
                        amount = request.POST['amount']

                        return render(request, 'donate.html', {'totalAmount': amount})

                    else:
                        messages.info(request, 'Username already exists')
                        return redirect('donationForm')

                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already exists')
                    return redirect('donationForm')
                else:
                    user = User.objects.create_user(username=username, password=password1, email=email)
                    user.save();

                    user = auth.authenticate(username=username, password=password1)

                    auth.login(request, user)

                    current_user = request.user
                    user_profile = Auth_user_profile.objects.create(is_user=1, is_volunteer=0, user_id = current_user.id)
                    user_profile.save();

                    return render(request, 'donate.html', {'totalAmount': amount})

            else:
                messages.info(request, 'Please, Enter Same Password')
                return redirect('donationForm')
        else:
            return render(request, 'newDonorRegistration.html')



def donate2(request):
    current_user = request.user

    if current_user.id is not None:
        if request.method == 'POST':
            amount = request.POST['amount']

            return render(request, 'donate2.html', {'totalAmount': amount})

        else:
            return render(request, 'donationForm2.html')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            amount = request.POST['amount']

            if password1==password2:
                if User.objects.filter(username=username).exists():
                    user = auth.authenticate(username=username, password=password1)
                    if user is not None:
                        auth.login(request, user)
                        amount = request.POST['amount']

                        return render(request, 'donate2.html', {'totalAmount': amount})

                    else:
                        messages.info(request, 'Username already exists')
                        return redirect('donationForm2')

                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already exists')
                    return redirect('donationForm2')
                else:
                    user = User.objects.create_user(username=username, password=password1, email=email)
                    user.save();

                    user = auth.authenticate(username=username, password=password1)

                    auth.login(request, user)

                    current_user = request.user
                    user_profile = Auth_user_profile.objects.create(is_user=1, is_volunteer=0, user_id = current_user.id)
                    user_profile.save();

                    return render(request, 'donate2.html', {'totalAmount': amount})

            else:
                messages.info(request, 'Please, Enter Same Password')
                return redirect('donationForm2')
        else:
            return render(request, 'newDonorRegistration2.html')



def donate3(request):
    current_user = request.user

    if current_user.id is not None:
        if request.method == 'POST':
            amount = request.POST['amount']

            return render(request, 'donate3.html', {'totalAmount': amount})

        else:
            return render(request, 'donationForm3.html')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            amount = request.POST['amount']

            if password1==password2:
                if User.objects.filter(username=username).exists():
                    user = auth.authenticate(username=username, password=password1)
                    if user is not None:
                        auth.login(request, user)
                        amount = request.POST['amount']

                        return render(request, 'donate3.html', {'totalAmount': amount})

                    else:
                        messages.info(request, 'Username already exists')
                        return redirect('donationForm3')

                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already exists')
                    return redirect('donationForm3')
                else:
                    user = User.objects.create_user(username=username, password=password1, email=email)
                    user.save();

                    user = auth.authenticate(username=username, password=password1)

                    auth.login(request, user)

                    current_user = request.user
                    user_profile = Auth_user_profile.objects.create(is_user=1, is_volunteer=0, user_id = current_user.id)
                    user_profile.save();

                    return render(request, 'donate3.html', {'totalAmount': amount})

            else:
                messages.info(request, 'Please, Enter Same Password')
                return redirect('donationForm3')
        else:
            return render(request, 'newDonorRegistration3.html')



def donate4(request):
    current_user = request.user

    if current_user.id is not None:
        if request.method == 'POST':
            amount = request.POST['amount']

            return render(request, 'donate4.html', {'totalAmount': amount})

        else:
            return render(request, 'donationForm4.html')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            amount = request.POST['amount']

            if password1==password2:
                if User.objects.filter(username=username).exists():
                    user = auth.authenticate(username=username, password=password1)
                    if user is not None:
                        auth.login(request, user)
                        amount = request.POST['amount']

                        return render(request, 'donate4.html', {'totalAmount': amount})

                    else:
                        messages.info(request, 'Username already exists')
                        return redirect('donationForm4')

                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already exists')
                    return redirect('donationForm4')
                else:
                    user = User.objects.create_user(username=username, password=password1, email=email)
                    user.save();

                    user = auth.authenticate(username=username, password=password1)

                    auth.login(request, user)

                    current_user = request.user
                    user_profile = Auth_user_profile.objects.create(is_user=1, is_volunteer=0, user_id = current_user.id)
                    user_profile.save();

                    return render(request, 'donate4.html', {'totalAmount': amount})

            else:
                messages.info(request, 'Please, Enter Same Password')
                return redirect('donationForm4')
        else:
            return render(request, 'newDonorRegistration4.html')




@login_required
def successful(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        status = 'successful'

        current_user = request.user
        user_id = current_user.id

        donate = Donation.objects.create(amount=amount, user_id=user_id, donationType_id=1)
        donate.save();

        return redirect('totallySuccessful')

    else:
        return redirect('/')



@login_required
def successful2(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        status = 'successful'

        current_user = request.user
        user_id = current_user.id

        donate = Donation.objects.create(amount=amount, user_id=user_id, donationType_id=2)
        donate.save();

        return redirect('totallySuccessful')

    else:
        return redirect('/')



@login_required
def successful3(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        status = 'successful'

        current_user = request.user
        user_id = current_user.id

        donate = Donation.objects.create(amount=amount, user_id=user_id, donationType_id=3)
        donate.save();

        return redirect('totallySuccessful')

    else:
        return redirect('/')



@login_required
def successful4(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        status = 'successful'

        current_user = request.user
        user_id = current_user.id

        donate = Donation.objects.create(amount=amount, user_id=user_id, donationType_id=4)
        donate.save();

        return redirect('totallySuccessful')

    else:
        return redirect('/')



@login_required
def totallySuccessful(request):
    current_user = request.user

    if current_user.id is not None:
        status = 'Successful'
        user_id = current_user.id
        donation = Donation.objects.filter(user_id=user_id)

        return render(request, 'successful.html', {'donation': donation, 'status' : status})
    else:
        return redirect('/')



from django.db.models import Avg, Max, Min, Sum
def index(request):
    charities = Nonprofitcharities.objects.all()
    stories = Ourlateststory.objects.all()
    upcoming = UpcomingEvents.objects.all()
    gallaries = Gallary.objects.all()
    contacts = Contactus.objects.all()

    educationDonation2 = Donation.objects.filter(donationType_id=2).aggregate(Sum('amount'))
    eduDon2 = educationDonation2['amount__sum']

    educationDonation3 = Donation.objects.filter(donationType_id=3).aggregate(Sum('amount'))
    eduDon3 = educationDonation3['amount__sum']

    educationDonation4 = Donation.objects.filter(donationType_id=4).aggregate(Sum('amount'))
    eduDon4 = educationDonation4['amount__sum']


    educationDonor2 = Donation.objects.filter(donationType_id=2).count()
    educationDonor3 = Donation.objects.filter(donationType_id=3).count()
    educationDonor4 = Donation.objects.filter(donationType_id=4).count()

    return render(request, 'index.html', {'charities' : charities, 'stories' : stories, 'upcoming': upcoming, 'gallaries' : gallaries, 'contacts' : contacts, 'eduDon2': eduDon2, 'educationDonor2':educationDonor2, 'eduDon3': eduDon3, 'educationDonor3':educationDonor3, 'eduDon4': eduDon4, 'educationDonor4':educationDonor4})


def about(request):

    gallaries = Gallary.objects.all()
    contacts = Contactus.objects.all()

    auth_user_profile = Auth_user_profile.objects.filter(is_volunteer = 1)
    page = request.GET.get('page', 1)

    paginator = Paginator(auth_user_profile, 8)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'about.html', {'users': users, 'gallaries' : gallaries, 'contacts' : contacts, 'auth_user_profile': auth_user_profile})


def objectives(request):
    current_user = request.user

    gallaries = Gallary.objects.all()
    contacts = Contactus.objects.all()
    objectives = Objectives.objects.all()
    imageGallary = ImageGallary.objects.all()


    return render(request, 'objectives.html', {'gallaries' : gallaries, 'contacts' : contacts, 'objectives' : objectives, 'imageGallary' : imageGallary})


def contact(request):
    current_user = request.user

    gallaries = Gallary.objects.all()
    contacts = Contactus.objects.all()

    return render(request, 'contact.html', {'gallaries' : gallaries, 'contacts' : contacts})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email)
                user.save();

                user = auth.authenticate(username=username, password=password1)

                auth.login(request, user)

                current_user = request.user
                user_profile = Auth_user_profile.objects.create(is_user=1, is_volunteer=0, user_id = current_user.id)
                user_profile.save();

                messages.info(request, 'Registration Successful')
                return redirect('index')
        else:
            messages.info(request, 'Please Enter Same Password')
            return redirect('register')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Sorry, You Entered Wrong Information')
            messages.info(request, 'Please Try Again')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')



def subscribe(request):
    charities = Nonprofitcharities.objects.all()
    stories = Ourlateststory.objects.all()
    upcoming = UpcomingEvents.objects.all()
    gallaries = Gallary.objects.all()
    contacts = Contactus.objects.all()

    educationDonation2 = Donation.objects.filter(donationType_id=2).aggregate(Sum('amount'))
    eduDon2 = educationDonation2['amount__sum']

    educationDonation3 = Donation.objects.filter(donationType_id=3).aggregate(Sum('amount'))
    eduDon3 = educationDonation3['amount__sum']

    educationDonation4 = Donation.objects.filter(donationType_id=4).aggregate(Sum('amount'))
    eduDon4 = educationDonation4['amount__sum']


    educationDonor2 = Donation.objects.filter(donationType_id=2).count()
    educationDonor3 = Donation.objects.filter(donationType_id=3).count()
    educationDonor4 = Donation.objects.filter(donationType_id=4).count()

    mess = 'abc'

    if request.method == 'POST':
        email = request.POST['email']

        if Subscribe.objects.filter(email=email).exists():
            mess = 'unsuccessful'
            return render(request, 'index.html', {'mess': mess, 'charities' : charities, 'stories' : stories, 'upcoming': upcoming, 'gallaries' : gallaries, 'contacts' : contacts, 'eduDon2': eduDon2, 'educationDonor2':educationDonor2, 'eduDon3': eduDon3, 'educationDonor3':educationDonor3, 'eduDon4': eduDon4, 'educationDonor4':educationDonor4})

        else:
            subs = Subscribe.objects.create(email=email)
            subs.save();

            mess = 'successful'
            return render(request, 'index.html', {'mess': mess, 'charities' : charities, 'stories' : stories, 'upcoming': upcoming, 'gallaries' : gallaries, 'contacts' : contacts, 'eduDon2': eduDon2, 'educationDonor2':educationDonor2, 'eduDon3': eduDon3, 'educationDonor3':educationDonor3, 'eduDon4': eduDon4, 'educationDonor4':educationDonor4})


    return render(request, 'index.html', {'mess':mess, 'charities' : charities, 'stories' : stories, 'upcoming': upcoming, 'gallaries' : gallaries, 'contacts' : contacts, 'eduDon2': eduDon2, 'educationDonor2':educationDonor2, 'eduDon3': eduDon3, 'educationDonor3':educationDonor3, 'eduDon4': eduDon4, 'educationDonor4':educationDonor4})




def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def myAccount(request):
    current_user = request.user

    gallaries = Gallary.objects.all()
    contacts = Contactus.objects.all()
    auth_user_profile = Auth_user_profile.objects.filter(user_id = current_user.id)

    return render(request, 'profile.html', {'gallaries' : gallaries, 'contacts' : contacts, 'auth_user_profile': auth_user_profile})


@login_required
def updateProfile(request):
    current_user = request.user

    gallaries = Gallary.objects.all()
    contacts = Contactus.objects.all()
    auth_user_profile = Auth_user_profile.objects.filter(user_id = current_user.id)

    return render(request, 'updateProfile.html', {'gallaries' : gallaries, 'contacts' : contacts, 'auth_user_profile': auth_user_profile})


@login_required
def updateProfileInfo(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        is_volunteer = request.POST['is_volunteer']
        address = request.POST['address']
        age = request.POST['age']
        gender = request.POST['gender']
        profession = request.POST['profession']
        educational_bg = request.POST['educational_bg']
        blood_group = request.POST['blood_group']

        current_user = request.user
        newevent = Auth_user_profile.objects.get(user_id = current_user.id)

        if newevent.is_volunteer:
            facebook = request.POST['facebook']
            twitter = request.POST['twitter']
            instagram = request.POST['instagram']
            whatsapp = request.POST['whatsapp']
        else:
            facebook = ''
            twitter = ''
            instagram = ''
            whatsapp = ''


        user = Auth_user_profile.objects.filter(user_id=current_user.id).update(full_name=full_name, is_volunteer=is_volunteer, address=address, age=age, gender_id=gender, profession=profession, educational_bg=educational_bg, blood_group_id=blood_group, facebook=facebook, twitter=twitter, instagram=instagram, whatsapp=whatsapp)

        return redirect('myAccount')


@login_required
def updateProfilePic(request):
    current_user = request.user

    gallaries = Gallary.objects.all()
    contacts = Contactus.objects.all()
    auth_user_profile = Auth_user_profile.objects.filter(user_id = current_user.id)

    return render(request, 'updateProfilePic.html', {'gallaries' : gallaries, 'contacts' : contacts, 'auth_user_profile': auth_user_profile})



from django.core.files.storage import FileSystemStorage
@login_required
def uploadPic(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['picture']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)

        # url = fs.url(name)

        current_user = request.user
        user = Auth_user_profile.objects.filter(user_id=current_user.id).update(picture=name)


        return redirect('myAccount')


@login_required
def changePassword(request):
    current_user = request.user

    gallaries = Gallary.objects.all()
    contacts = Contactus.objects.all()
    auth_user_profile = Auth_user_profile.objects.filter(user_id = current_user.id)

    return render(request, 'changePassword.html', {'gallaries' : gallaries, 'contacts' : contacts, 'auth_user_profile': auth_user_profile})


@login_required
def changePasswordDone(request):
    if request.method == 'POST':
        oldPassword = request.POST['oldPassword']
        newPassword1 = request.POST['newPassword1']
        newPassword2 = request.POST['newPassword2']

        current_user = request.user

        user = auth.authenticate(username=current_user.username, password=oldPassword)
        if user is not None:

            if newPassword1==newPassword2:

                u = User.objects.get(username = current_user.username)
                u.set_password(newPassword1)
                u.save()

                user = auth.authenticate(username=current_user.username, password=newPassword1)
                if user is not None:
                    auth.login(request, user)
                    return redirect('myAccount')
                else:
                    messages.info(request, 'Sorry, You Entered Wrong Information')
                    messages.info(request, 'Please Try Again')
                    return render(request, 'login.html')
            else:
                return render(request, 'changePassword.html')

        else:
            return render(request, 'changePassword.html')
    else:
        return render(request, 'changePassword.html')






@login_required
def activities(request):
    current_user = request.user

    gallaries = Gallary.objects.all()
    contacts = Contactus.objects.all()
    auth_user_profile = Auth_user_profile.objects.filter(user_id = current_user.id)

    if current_user.id is not None:
        status = 'Successful'
        user_id = current_user.id
        donation = Donation.objects.filter(user_id=user_id)
        hasRecord = Donation.objects.filter(user_id=user_id).count()


        user_questions = Questions.objects.filter(user_id = current_user.id)
        hasQuestion = Questions.objects.filter(user_id=user_id).count()

#############################################################################################################
        authUP = Auth_user_profile.objects.filter(user_id = current_user.id).values_list()
        myList3 = list(authUP)

        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(myList3)
        print(myList3[0][1])
############################################################################################################

        abailableBG = AvailableBloodGroup.objects.filter(receiver_id=myList3[0][0])
        hasRecord1 = AvailableBloodGroup.objects.filter(receiver_id=myList3[0][0]).count()

        return render(request, 'activities.html', {'user_questions' : user_questions, 'hasQuestion': hasQuestion , 'abailableBG' : abailableBG, 'hasRecord1' : hasRecord1, 'donation': donation, 'status' : status, 'gallaries' : gallaries, 'contacts' : contacts, 'auth_user_profile': auth_user_profile, 'hasRecord': hasRecord})

    else:
        return redirect('/')



def question(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        question = request.POST['message']

        current_user = request.user

        import datetime
        now = datetime.datetime.now()

        ques = Questions.objects.create(name=name, email = email, subject=subject, question=question, user_id = current_user.id, question_date=now, answer="Not Answered Yet")
        ques.save();


        gallaries = Gallary.objects.all()
        contacts = Contactus.objects.all()
        mess = 'succ'
        return render(request, 'contact.html', {'gallaries' : gallaries, 'contacts' : contacts, 'mess': mess})
    else:
        mess = 'unsucc'
        return render(request, 'contact.html', {'gallaries' : gallaries, 'contacts' : contacts, 'mess': mess})



def information(request):
    if request.method == 'POST':
        chaTypeId = request.POST['chaTypeId']

        user = TempInfo.objects.filter(id=1).update(typeNo=chaTypeId)
        return redirect('mainInfo')
    else:
        return redirect('/')



def mainInfo(request):
    chaTypeId = TempInfo.objects.values_list('typeNo', flat=True).get(id=1)

    type = CharityType.objects.filter(id = chaTypeId)
    allData = Information.objects.filter(CharityType_id=chaTypeId)

    gallaries = Gallary.objects.all()
    contacts = Contactus.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(allData, 3)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'information.html', {'users': users, 'gallaries' : gallaries, 'contacts' : contacts, 'type' : type})


def search(request):
    if request.method == 'POST':
        mySearch = request.POST['mySearch']

        user = TempSearch.objects.filter(id=1).update(searchTitle=mySearch)
        return redirect('mainSearch')
    else:
        return redirect('/')


def mainSearch(request):
    mySearch = TempSearch.objects.values_list('searchTitle', flat=True).get(id=1)

    match = Information.objects.filter(Q(title__icontains=mySearch) | Q(desc__icontains=mySearch) | Q(location__icontains=mySearch))

    gallaries = Gallary.objects.all()
    contacts = Contactus.objects.all()

    if match:
        page = request.GET.get('page', 1)

        paginator = Paginator(match, 3)

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        return render(request, 'search.html', {'users': users, 'gallaries' : gallaries, 'contacts' : contacts})
    else:
        messages.error(request, 'No Result Found')
        return render(request, 'search.html', {'gallaries' : gallaries, 'contacts' : contacts})

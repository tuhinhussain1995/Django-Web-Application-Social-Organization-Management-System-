from django.urls import path
from core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('objectives', views.objectives, name='objectives'),
    path('contact', views.contact, name='contact'),






    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('myAccount', views.myAccount, name='myAccount'),


    path('donationForm', views.donationForm, name='donationForm'),
    path('donationForm2', views.donationForm2, name='donationForm2'),
    path('donationForm3', views.donationForm3, name='donationForm3'),
    path('donationForm4', views.donationForm4, name='donationForm4'),
    path('donate', views.donate, name='donate'),
    path('donate2', views.donate2, name='donate2'),
    path('donate3', views.donate3, name='donate3'),
    path('donate4', views.donate4, name='donate4'),
    path('successful', views.successful, name='successful'),
    path('successful2', views.successful2, name='successful2'),
    path('successful3', views.successful3, name='successful3'),
    path('successful4', views.successful4, name='successful4'),
    path('totallySuccessful', views.totallySuccessful, name='totallySuccessful'),


    path('receiveBlood', views.receiveBlood, name='receiveBlood'),
    path('receiveBloodSuccessful', views.receiveBloodSuccessful, name='receiveBloodSuccessful'),



    path('updateProfile', views.updateProfile, name='updateProfile'),
    path('changePassword', views.changePassword, name='changePassword'),
    path('changePasswordDone', views.changePasswordDone, name='changePasswordDone'),
    path('activities', views.activities, name='activities'),
    path('updateProfileInfo', views.updateProfileInfo, name='updateProfileInfo'),
    path('updateProfilePic', views.updateProfilePic, name='updateProfilePic'),
    path('uploadPic', views.uploadPic, name='uploadPic'),

    path('subscribe', views.subscribe, name='subscribe'),

    path('volenteerForm', views.volenteerForm, name='volenteerForm'),
    path('volenteer', views.volenteer, name='volenteer'),
    path('question', views.question, name='question'),

    path('information', views.information, name='information'),
    path('mainInfo', views.mainInfo, name='mainInfo'),

    path('search', views.search, name='search'),
    path('mainSearch', views.mainSearch, name='mainSearch'),


]

from django.urls import path
from .views import  home, post, edit_post, search, profile, upload, contact, privacy_policy


urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload, name='upload'),
    path('post/<str:post_url>', post, name='post'),
    path('post/<str:post_url>/edit/', edit_post, name='edit_post'),
    path('search/', search, name='search'),
    path('accounts/profile/', profile, name='profile'),

    path('contact', contact, name='contact'),
    path('privacy-policy', privacy_policy, name='privacy-policy'),
]

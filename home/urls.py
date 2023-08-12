from django.urls import path, re_path
from .views import  home, post, edit_post, search, profile, upload, contact, privacy_policy


urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload, name='upload'),
    path('posts/', home, name='posts'),
    re_path('^posts/(?P<post_url>[\w-]+)/$', post, name='post'),
    path('posts/<str:post_url>/edit/', edit_post, name='edit_post'),
    path('search/', search, name='search'),
    path('accounts/profile/', profile, name='profile'),

    path('contact', contact, name='contact'),
    path('privacy-policy', privacy_policy, name='privacy-policy'),
]

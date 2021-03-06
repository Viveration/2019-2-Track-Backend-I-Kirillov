from django.urls import path
from userprofile.views import contacts, profile, user_search


urlpatterns = [
    path('contacts/<int:uid>', contacts, name='contacts'),
    path('<int:uid>', profile, name='profile'),
    path('searchuser', user_search, name='search_user'),
]

"""
URL mappings for the user API.
"""
from django.urls import path

from user import views

app_name = 'user'

# define a URL mattern and a URL called 'create/'. Any request passed to that
# URL is going to be handled by the view we define here.
# The name 'create' is used for the reverse lookup in the test_user_api
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
]

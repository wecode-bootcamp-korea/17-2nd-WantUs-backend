from django.urls import path

from user.views import SignView, ProfileView

urlpatterns = [
    path('/sign', SignView.as_view()),
    path('/profile', ProfileView.as_view())
]

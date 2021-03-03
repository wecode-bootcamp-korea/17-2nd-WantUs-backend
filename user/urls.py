from django.urls import path

from user.views import SignView

urlpatterns = [
    path('/sign', SignView.as_view())
]

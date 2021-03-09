from django.urls import path

from apply.views import ApplyView

urlpatterns = [
    path('', ApplyView.as_view())
]
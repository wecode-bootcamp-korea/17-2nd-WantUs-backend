from django.urls import path

from apply.views import ApplyView, MyWantUsView

urlpatterns = [
    path('', ApplyView.as_view()),
    path('/mywanted', MyWantUsView.as_view())
]

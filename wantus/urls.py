from django.urls import path, include

from posting.views   import MainView

urlpatterns = [
    path('user', include('user.urls')),
    path('posting', include('posting.urls')),
    path('main', MainView.as_view()),
    path('resume', include('resume.urls')),
]

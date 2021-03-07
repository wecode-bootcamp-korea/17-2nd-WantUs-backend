from django.urls import path

from resume.views import ResumeFilewUploadView

urlpatterns = [
        path('/upload', ResumeFilewUploadView.as_view()),
        ]

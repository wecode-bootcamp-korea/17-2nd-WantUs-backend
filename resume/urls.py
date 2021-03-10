from django.urls import path

from resume.views import (
        ResumeFilewUploadView,
        ResumePartialView,
        ResumeView,
        )

urlpatterns = [
    path('/upload', ResumeFilewUploadView.as_view()),
    path('', ResumeView.as_view()),
    path('/<int:resume_id>', ResumePartialView.as_view()),
    path('/upload/<int:resume_id>', ResumeFilewUploadView.as_view()),
        ]

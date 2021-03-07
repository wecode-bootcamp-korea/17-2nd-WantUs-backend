from django.urls import path

from resume.views import ResumeFilewUploadView, ResumePartialView

urlpatterns = [
    path('/upload', ResumeFilewUploadView.as_view()),
    path('/<int:resume_id>', ResumePartialView.as_view())
        ]

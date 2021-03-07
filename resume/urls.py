from django.urls    import path

from .views         import ResumeMainView

urlpatterns = [
    path('/list', ResumeMainView.as_view()),
        ]

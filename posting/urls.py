from django.urls   import path
from posting.views import PostingDetailView, RelatedPostingView

urlpatterns = [
    path('/<int:posting_id>', PostingDetailView.as_view()),
    path('/<int:posting_id>/related-posting', RelatedPostingView.as_view()),
]

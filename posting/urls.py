from django.urls   import path
from posting.views import PostingDetailView, RelatedPostingView, PostingBookmarkView, PostingLikeView

urlpatterns = [
    path('/<int:posting_id>', PostingDetailView.as_view()),
    path('/<int:posting_id>/related-posting', RelatedPostingView.as_view()),
    path('/like/<int:posting_id>', PostingLikeView.as_view()),
    path('/bookmark/<int:posting_id>', PostingBookmarkView.as_view()),
        ]

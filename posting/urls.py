from django.urls   import path
from posting.views import PostingDetailView

urlpatterns = [
    path('/<int:posting_id>', PostingDetailView.as_view())
]

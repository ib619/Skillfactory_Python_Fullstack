from django.urls import path
from.views import PostList, PostDetail, PostSearch, PostCreateView, PostUpdateView, PostDeleteView


urlpatterns = [
    path('news/', PostList.as_view(), name='posts'),
    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='posts_search'),
    path('news/add', PostCreateView.as_view(), name='post_create'),
    path('news/<int:pk>/edit', PostUpdateView.as_view(), name='post_update'),
    path('news/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
]
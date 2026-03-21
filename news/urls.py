
from django.urls import path

from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, NewsSearchView

urlpatterns = [
               path('search/', NewsSearchView.as_view(), name='news_search'),
               path('', PostListView.as_view(), name='post_list'),
               path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
               path('create/', PostCreateView.as_view(), name='news_create'),
               path('articles/create/', PostCreateView.as_view(), name='articles_create'),
               path('news/<int:pk>/update/', PostUpdateView.as_view(), name='news_update'),
               path('articles/<int:pk>/update/', PostUpdateView.as_view(), name='articles_update'),
               path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='news_delete'),
               path('articles/<int:pk>/delete/', PostDeleteView.as_view(), name='articles_delete'),
]
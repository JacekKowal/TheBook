from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index-view'),
    path('', views.HomeView.as_view(), name='home-view'),
    path('create_post/', views.PostCreateView.as_view(), name='create-post'),
    path('delete_post/<int:pk>', views.PostDeleteView.as_view(), name='post-delete'),
    path('update_post/<int:pk>', views.PostUpdateView.as_view(), name='post-view'),
    path('post_like/<int:pk>', views.PostLike.as_view(), name='post-like'),
    path('add_comment/<int:pk>', views.AddComment.as_view(), name='add-comment'),

]

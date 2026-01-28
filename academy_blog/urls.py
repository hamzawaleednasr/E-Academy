from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_view'),
    path('<int:id>/', views.ArticleListView.as_view(), name='article_view'),
    path('create/', views.ArticleCreateView.as_view(), name='article_create'), 
    path('edit/<int:pk>/', views.ArticleUpdateView.as_view(), name='article_update'), 
    path('show/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('delete/<int:pk>/', views.ArticleDeleteView.as_view(), name='article_delete'),
]
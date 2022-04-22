from django.urls import path
from . import views


urlpatterns = [
    path('articles/', views.article_list), # 전체 글 조회 url
    path('articles/<int:article_pk>/', views.article_detail), # 글 조회
    path('articles/<int:article_pk>/comments/', views.comment_create),
    path('comments/', views.comment_list),
    path('comments/<int:comment_pk>/', views.comment_detail),
    ]

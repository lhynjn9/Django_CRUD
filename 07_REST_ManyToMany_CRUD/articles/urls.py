from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.urls import path
from . import views

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
    path('articles/', views.article_list), # 전체 글 조회 url
    path('articles/<int:article_pk>/',views.article_detail), # 개별 글 조회 url
    path('articles/<int:article_pk>/comments/', views.comment_create),  # 댓글 생성 url
    path('comments/', views.comment_list), # 전체 댓글 조회 url
    path('comments/<int:comment_pk>/', views.comment_detail), # 댓글 조회, 삭제, 수정 url
    path('cards/', views.card_list), # 카드 조회 url
    path('cards/<int:card_pk>/', views.card_detail), # 개별 카드 조회 url
    path('<int:card_pk>/register/<int:article_pk>/', views.register),
    path('swagger/', schema_view.with_ui('swagger')),
    ]

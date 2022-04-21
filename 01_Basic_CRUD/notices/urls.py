from django.urls import path
from . import views

# 동일한 url이름을 구분하기 위한 app_name 작성
app_name = 'notices'
urlpatterns = [
    # name : url의 이름 설정
    path('', views.index, name='index'), # 전체 게시글 조회 url
    path('new/', views.new, name='new'), # 게시글 생성 url
    path('create/', views.create, name='create'),
    # Variable Routing
    path('<int:pk>/', views.detail, name='detail'), # 개별 게시글 상세 페이지 url
    path('<int:pk>/delete/', views.delete, name='delete'), # 개별 게시글 삭제 url
    path('<int:pk>/edit/', views.edit, name='edit'), # 개별 게시글 수정 url
    path('<int:pk>/update/', views.update, name='update'),
]
from django.urls import path
from . import views

# 동일한 url이름을 구분하기 위한 app_name 작성
app_name = 'notices'
urlpatterns = [
    # name : url의 이름 설정
    path('', views.index, name='index'), # 전체 게시글 조회 url
    path('create/', views.create, name='create'),# 게시글 생성 url
    # Variable Routing
    path('<int:pk>/', views.detail, name='detail'), # 개별 게시글 상세 페이지 url
    path('<int:pk>/delete/', views.delete, name='delete'), # 개별 게시글 삭제 url
    path('<int:pk>/update/', views.update, name='update'), # 개별 게시글 수정 url
    path('<int:pk>/comments/', views.comment_create, name='comment_create'), # 댓글 작성 url
    path('<int:notice_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'), # 댓글 삭제 url
]
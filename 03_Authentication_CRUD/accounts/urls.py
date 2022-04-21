from django.urls import path
from . import views

# 동일한 url이름을 구분하기 위한 app_name 작성
app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name = 'login'), # 로그인 url
    path('logout/', views.logout, name = 'logout'), # 로그아웃 url
    path('signup/', views.singup, name = 'signup'), # 회원가입 url
    path('delete/', views.delete, name = 'delete'), # 회원탈퇴 url
    path('update/', views.update, name = 'update'), # 회원정보 수정 url
    # # password/는 기존 url과 맞춰준 것
    path('password/', views.change_password, name = 'change_password'), # 비밀번호 수정 url
]
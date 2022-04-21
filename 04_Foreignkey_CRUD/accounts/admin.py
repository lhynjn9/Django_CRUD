from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Custom User 모델 등록
# 이후 관리자 페이지에 사용자(들)이 생성됨 : 새로운 사용자 그룹(?)이 생성
admin.site.register(User, UserAdmin)
from django.db import models
from django.contrib.auth.models import AbstractUser

# 내장 User 모델
# 일부 프로젝트는 내장 User 모델이 제공하는 인증 요구사항이 적절하지 않을 수 있음
# Django에서는 AUTH_USER_MODEL 값을 제공하여 재정의할 수 있도록 함
class User(AbstractUser):
    # Follow 구현을 위한 M:N 관계 설정(재귀 관계)
    # symmetrical : 재귀적 관게를 의미, False를 설정하여 자동 참조(서로 참조)를 하지 않도록 함
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
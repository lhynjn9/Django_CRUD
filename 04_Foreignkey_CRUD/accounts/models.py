from django.db import models
from django.contrib.auth.models import AbstractUser

# 내장 User 모델
# 일부 프로젝트는 내장 User 모델이 제공하는 인증 요구사항이 적절하지 않을 수 있음
# Django에서는 AUTH_USER_MODEL 값을 제공하여 재정의할 수 있도록 함
class User(AbstractUser):
    pass
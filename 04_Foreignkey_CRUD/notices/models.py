from django.db import models
from django.conf import settings

# Model 클래스를 상속 받음
class Notice(models.Model):
    # user와 Notice의 1:N 외래키 설정
    # user 모델 참조는 함수(get_user_model())로 진행하지 않고, settings.AUTH_USER_MODEL(반환값은 문자열임)로 진행
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    # 외래키 설정
    # 참조하는 모델명_id로 데이터베이스 필드 명이 생성됨
    # 명시적 모델관계를 위해 클래스명을 소문자 단수형으로 작성하는 것이 바람직함
    # article과 Comments의 1:N 외래키 설정
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE) # 마이그레이션하면 마지막에 생성됨
    # user와 Comments의 1:N 외래키 설정
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content =  models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
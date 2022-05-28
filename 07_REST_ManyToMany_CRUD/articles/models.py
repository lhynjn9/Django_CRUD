from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    # article과 1:N 관계를 위한 외래키 설정
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Card(models.Model):
    # article과 M:N 관계
    articles = models.ManyToManyField(Article, related_name='cards')
    name = models.CharField(max_length=100)
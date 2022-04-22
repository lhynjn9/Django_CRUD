from rest_framework import serializers
from .models import Article

# ModelSerializer : 모델에 맞춰 자동으로 필드를 생성해 직렬화해줌
# 게시글 쿼리셋을 직렬화
class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'

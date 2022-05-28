# 유지보수 및 관리를 위해 분리

from rest_framework import serializers
from ..models import Comment
# ModelSerializer : 모델 필드에 해당하는 필드가 있는 Serializer 클래스를 자동으로 만들 수 있는 shortcut
# 자동 필드 생성, create, update의 간단한 기본 구현

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        # form-data로 부터 정보를 받아 직렬화 과정에서 유효성 검사를 통과하지 못한 필드를 읽기 전용으로 설정하여
        # 직렬화 하지 않고 반환 값에만 해당 필드가 포함되도록 설정
        # 필드를 오버라이드 하거나 추가한 경우 read_only_field 설정 불가
        read_only_fields = ('article',)
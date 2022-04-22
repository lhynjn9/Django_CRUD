from rest_framework import serializers
from .models import Article, Comment
# ModelSerializer : 모델 필드에 해당하는 필드가 있는 Serializer 클래스를 자동으로 만들 수 있는 shortcut
# 자동 필드 생성, create, update의 간단한 기본 구현

class ArticleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('id', 'title',)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        # form-data로 부터 정보를 받아 직렬화 과정에서 유효성 검사를 통과하지 못한 필드를 읽기 전용으로 설정하여
        # 직렬화 하지 않고 반환 값에만 해당 필드가 포함되도록 설정
        # 필드를 오버라이드 하거나 추가한 경우 read_only_field 설정 불가
        read_only_fields = ('article',)


class ArticleSerializer(serializers.ModelSerializer):
    # many : 단일 객체가 아닐 경우, True로 설정
    # form-data로 부터 정보를 받아 직렬화 과정에서 유효성 검사를 통과하지 못한 필드를 읽기 전용으로 설정하여
    # 직렬화 하지 않고 반환 값에만 해당 필드가 포함되도록 설정
    # comment_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # 참조된 대상의 참조하는 대상의 표현에 포함되거나 중첩될 수 있음
    # 이러한 중첩 관계를 직렬화의 필드로 사용 가능 : 두 클랫의 상하위치 변경
    comment_set = CommentSerializer(many=True, read_only=True)
    # 특정 게시글에 작성된 댓글의 개수 구하기
    # commet_set 처럼 자동으로 구성되는 필드가 아닌 별도의 값을 위한 필드를 사용할 경우
    # 직접 필드를 작성해야 함 :source
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'



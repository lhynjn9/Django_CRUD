from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
# get_list_or_404 : filter 함수를 통한 객체
from django.shortcuts import get_list_or_404, get_object_or_404
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer
from .models import Article, Comment
from articles import serializers

# 전체 게시글글 조회, 생성
# @api_view() : 기본적으로 GET 메소드만 허용되고, DRF에서 필수적으로 작성해야하 정상 동작
@api_view(['GET', 'POST'])
def article_list(request):
    # 전체     게시글 조회
    if request.method == 'GET':
        # articles = Article.objects.all()
        articles = get_list_or_404(Article)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    # 게시글 생성
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        # raise_exception : 유효성 검사 오류가 있는 경우 예외를 발생시키기 위해 사용 할 수 있음
        # 따라서 오류에 따른 return문이 없어도 됨
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# 게시글 조회, 삭제, 수정
@api_view(['GET', 'DELETE', 'PUT'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    # 게시글 조회
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    # 게시글 삭제
    elif request.method == 'DELETE':
        article.delete()
        data = {
            'delete': f'데이터 {article_pk}번이 삭제되었습니다.',
        }
        
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    # 게시글 수정
    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, request.data)
        # serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

# 댓글 조회, 삭제, 수정
@api_view(['GET'])
def comment_list(request):
    comments = get_list_or_404(Comment)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    # 댓글 조회
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data) 

    # 댓글 삭제
    elif request.method == 'DELETE':
        comment.delete()
        data = {
            'delete': f'데이터 {comment_pk}번이 삭제되었습니다.',
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    # 댓글 수정
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, request.data)
        # serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

# 댓글 생성
@api_view(['POST'])
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    # raise_exception : 유효성 검사 오류가 있는 경우 예외를 발생시키기 위해 사용 할 수 있음
    # 따라서 오류에 따른 return문이 없어도 됨
    if serializer.is_valid(raise_exception=True):
        # 저장하는 시점에서 필요한 참조하는 모델의 추가적인 데이터 삽입
        serializer.save(article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
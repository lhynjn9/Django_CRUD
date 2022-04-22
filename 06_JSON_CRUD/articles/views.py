from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from django.core import serializers
from .serializers import ArticleSerializer
from .models import Article

# HTML을 응답하는 서버
def article_html(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/article.html', context)

# JsonResponse 객체를 활용한 JSON 데이터 응답
def article_json_1(request):
    articles = Article.objects.all()
    articles_json = [] # 리스트 내에

    for article in articles:
        # 딕셔너리 형태로 저장
        articles_json.append(
            {
                'id': article.pk,
                'title': article.title,
                'content': article.content,
                'created_at': article.created_at,
                'updated_at': article.updated_at,
            }
        )
    # JsonResponse 객체 : JSON으로 응답하는 객체
    # safe : 전송데이터가 딕셔너리가 아니거나, 딕셔너리 이외의 객체를 직렬화하려면 False로 설정해야함(기본값 : True)
    return JsonResponse(articles_json, safe=False)

# Django 내장 HttpResponse 객체를 활용한 JSON 데이터 응답
def article_json_2(request):
    articles = Article.objects.all()
    # 주어진 모델 정보를 활용하여 필드를 개별적으로 만들 필요 없음
    # 직렬화: 복잡한 데이터 타입을 쉽게 변환 가능한 파이썬 데이터타입으로 변환하는 과정
    data = serializers.serialize('json', articles)
    return HttpResponse(data, content_type='application/json')

# Django REST framework(DRF) 라이브러리를 사용한 JSON 응답
# @api_view(['GET'])
@api_view()
def article_json_3(request):
    articles = Article.objects.all()
    # many : 단일 객체가 아닐 경우, True로 설정
    serializer = ArticleSerializer(articles, many=True)
    # DRF의 Response를 활용하여 직렬화된 JSON 객체 응답
    return Response(serializer.data)

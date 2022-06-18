from django.urls import path
from . import views


urlpatterns = [
    path('html/', views.article_html), # HTML을 응답 url
    path('json-1/', views.article_json_1), # JsonResponse 객체를 활용한 JSON 데이터 응답 url
    path('json-2/', views.article_json_2), # Django 내장 HttpResponse 객체를 활용한 JSON 데이터 응답 url
    path('json-3/', views.article_json_3), # Django REST framework(DRF) 라이브러리를 사용한 JSON 응답 url
]

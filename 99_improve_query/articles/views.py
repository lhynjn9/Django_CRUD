from django.shortcuts import render
from .models import Article, Comment
from django.db.models import Count
# Create your views here.
def index_1(request):
    
    # articles = Article.objects.order_by('-pk')
    # <!-- index-1에서 평가가 반복적으로 이루어지는 부분을 개선 -->
    articles = Article.objects.annotate(Count('comment')).order_by('-pk')
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index_1.html', context)


def index_2(request):
    # articles = Article.objects.order_by('-pk')
    # 1:N 에서 반복적으로 N이 1을 참조
    # 한번에 모든 것을 가져옴 : select_related
    articles = Article.objects.select_related('user').order_by('-pk')
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index_2.html', context)


def index_3(request):
    # articles = Article.objects.order_by('-pk')
    # 1:N 에서 반복적으로 1이 N을 역참조
    # 한번에 모든 것을 가져옴 : prefetch_related
    articles = Article.objects.prefetch_related('comment_set').order_by('-pk')
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index_3.html', context)


# 참조, 역참조를 한번에 해결하기 위해 임포트
from django.db.models import Prefetch


def index_4(request):
    # 참조와 역참조의 동시 발생
    # articles = Article.objects.order_by('-pk')
    articles = Article.objects.select_related('user').order_by('-pk')
    articles = Article.objects.prefetch_related(Prefetch('comment_set', queryset=Comment.objects.select_related('user'))).order_by('-pk')

    context = {
        'articles': articles,
    }
    return render(request, 'articles/index_4.html', context)

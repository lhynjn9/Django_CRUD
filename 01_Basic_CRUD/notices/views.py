from django.shortcuts import render, redirect
from .models import Notice


# Read : 전체 게시글 조회
def index(request):
    notices = Notice.objects.all()[::-1]
    context = {
        'notices' : notices
    }
    return render(request, 'notices/index.html', context) # 전체 게시글 목록을 반환

# Create : 게시글 생성
def new(request):
    return render(request, 'notices/new.html')

def create(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    notice = Notice(title=title, content=content) # 입력받은 값을 Notice에 저장
    notice.save() # DB에 저장
    
    # 새 url로 요청 전송
    return redirect('notices:detail', notice.pk)

# Read : 개별 게시글 조회
def detail(request, pk):
    notice = Notice.objects.get(pk=pk)
    context = {
        'notice' : notice,
    }
    
    return render(request, 'notices/detail.html', context)

# Delete : 게시글 삭제
def delete(request, pk):
    notice = Notice.objects.get(pk=pk)
    # POST일 경우에만 삭제 : 보안 문제
    if request.method == 'POST':
        notice.delete()
        return redirect('notices:index')
    # POST가 아닐 경우, 삭제 버튼이 있는 detail 페이지로 redirect
    else:
        return redirect('notices:detail', notice.pk)

# Update : 게시글 수정
def edit(request, pk):
    notice = Notice.objects.get(pk=pk)
    context = {
        'notice' : notice,
    }
    return render(request, 'notices/edit.html', context)

def update(request, pk):
    notice = Notice.objects.get(pk=pk)
    notice.title = request.POST.get('title')
    notice.content = request.POST.get('content')
    notice.save()
    return redirect('notices:detail', notice.pk)
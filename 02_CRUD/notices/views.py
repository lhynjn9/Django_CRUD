from django.shortcuts import render, redirect, get_object_or_404
from .models import Notice
from .forms import NoticeForm
# HTTP 기능을 지원하는 데코레이터
from django.views.decorators.http import require_http_methods, require_POST, require_safe


# Read : 전체 게시글 조회
@require_safe # GET만을 허용
def index(request):
    notices = Notice.objects.order_by('-pk')
    context = {
        'notices' : notices
    }
    return render(request, 'notices/index.html', context) # 전체 게시글 목록을 반환


# Create : 게시글 생성
# new와 create 함수가 method만 다를 뿐 같은 역할을 하고 있음
@require_http_methods(['GET', 'POST']) # 특정 메소드 요청만 허용
def create(request):
    # POST일 경우, create 역할
    if request.method == 'POST':
        # ModelForm을 이용하여 데이터를 받음
        form = NoticeForm(request.POST)
        # is_valid() : 데이터의 유효성 검사, boolean으로 결과를 반환
        if form.is_valid():
            notice = form.save() # DB에 저장    
            # 새 url로 요청 전송
            return redirect('notices:detail', notice.pk)
        
    # POST가 아닌 경우, new 역할 
    else:
        form = NoticeForm()
    # 유효성 검사를 통과하지 못한 경우
    context = {
        'form' : form,
    }
    return render(request, 'notices/create.html', context)

# Read : 개별 게시글 조회
@require_safe # GET만을 허용
def detail(request, pk):
    # get()을 호출하며, 상황에 따라 적절한 예외처리 진행
    notice = get_object_or_404(Notice, pk=pk)
    context = {
        'notice' : notice,
    }
    
    return render(request, 'notices/detail.html', context)

# Delete : 게시글 삭제
@require_POST # POST만을 허용 : 조건문을 통해 POST 이외의 메소드 요청을 처리할 이유가 사라짐
def delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    notice.delete()
    return redirect('notices:index')



# Update : 게시글 수정
# edit과 update 함수가 method만 다를 뿐 같은 역할을 하고 있음
@require_http_methods(['GET', 'POST']) # 특정 메소드 요청만 허용
def update(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    # POST일 경우, update 역할
    if request.method == 'POST':
        # ModelForm을 이용하여 데이터를 받음
        form = NoticeForm(request.POST, instance=notice)
        # is_valid() : 데이터의 유효성 검사, boolean으로 결과를 반환
        if form.is_valid():
            form.save()
            return redirect('notices:detail', notice.pk)

    # POST가 아닌 경우, edit 역할 
    else:
        form = NoticeForm(instance=notice)
    # 유효성 검사를 통과하지 못한 경우
    context = {
        'form' : form,
        'notice' : notice,
    }
    return render(request, 'notices/update.html', context)
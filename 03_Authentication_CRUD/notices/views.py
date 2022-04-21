from django.shortcuts import render, redirect, get_object_or_404
from .models import Notice
from .forms import NoticeForm
# HTTP 기능을 지원하는 데코레이터
from django.views.decorators.http import require_http_methods, require_POST, require_safe
# 로그인한 사용자만 접근 가능하도록 제한하는 데코레이터
# 인증 성공 시, 사용자가 redirect 되어야하는 경로는 next라는 쿼리 문자열 매개변수에 저장됨
# 비로그인 상태에서 로그인 상태에만 접근 가능한 경로를 입력하여 url에서 next에 해당하는 변수 확인 가능
from django.contrib.auth.decorators import login_required


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
@login_required 
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
# 데코레이터의 충돌 발생 : 로그인 검증 후, next 경로로 redirect 될 때 GET으로 처리되어
# POST 데이터를 잃어버리고, @require_POST와 충돌발생 
# login_required를 내부에서 처리  
@require_POST # POST만을 허용 : 조건문을 통해 POST 이외의 메소드 요청을 처리할 이유가 사라짐
def delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.user.is_authenticated:
        # 삭제를 요청한 유저와 작성한 유저가 같아야 삭제 가능
        if request.user == notice.user:
            notice.delete()
    return redirect('notices:index')



# Update : 게시글 수정
# edit과 update 함수가 method만 다를 뿐 같은 역할을 하고 있음
@login_required 
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
from django.shortcuts import render, redirect, get_object_or_404
from .models import Notice, Comment
from .forms import NoticeForm, CommentForm
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
            # 작성자 정보를 포함시켜야 함
            notice = form.save(commit=False)
            notice.user = request.user
            notice.save() # DB에 저장    
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

# Read : 개별 게시글 조회, 댓글 조회
@require_safe # GET만을 허용
def detail(request, pk):
    # get()을 호출하며, 상황에 따라 적절한 예외처리 진행
    notice = get_object_or_404(Notice, pk=pk)
    # CommentForm을 이용한 댓글 출력
    comment_form = CommentForm()
    # 조회한 notice의 모든 댓글을 조회 : 역참조
    comments = notice.comment_set.all()
    context = {
        'notice' : notice,
        'comment_form' : comment_form,
        'comments' : comments,
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
    return redirect('notices:detail', notice.pk)



# Update : 게시글 수정
# edit과 update 함수가 method만 다를 뿐 같은 역할을 하고 있음
@login_required 
@require_http_methods(['GET', 'POST']) # 특정 메소드 요청만 허용
def update(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    # 자신이 작성한 글만 수정
    if request.user == notice.user:
        # POST일 경우, update 역할
        if request.method == 'POST':
            # ModelForm을 이용하여 데이터를 받음
            form = NoticeForm(request.POST, instance=notice)
            # is_valid() : 데이터의 유효성 검사, boolean으로 결과를 반환
            if form.is_valid():
                notice = form.save()
                return redirect('notices:detail', notice.pk)

        # POST가 아닌 경우, edit 역할 
        else:
            form = NoticeForm(instance=notice)
    # 본인이 작성한 글이 아닌 경우
    else:
        return redirect('notices:index')

    context = {
        'form' : form,
        'notice' : notice,
    }
    return render(request, 'notices/update.html', context)

# Create : 댓글 생성
@require_POST
def comment_create(request, pk):
    # 기존 detail 페이지에서 댓글 작성이 처리가 되고 있음
    # 따라서 POST에 대한 처리만 하면 됨
    # 만약 댓글 작성에 대한 단독 페이지가 있다면, GET이 필요
    # 인증된 사용자만 접근
    if request.user.is_authenticated:
        notice = get_object_or_404(Notice, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # commit=False : 아직 데이터베이스에 저장되지 않은 인스턴스를 반환
            # 어떤 게시글에 작성하는지를 제외하였기 때문에
            # commit을 이용하여 DB에 저장은 안하지만 인스턴스만 리턴으로 제공하겠다는 의미로 작성해줌
            # 즉, 누락했던 글을 작성할 시간이 생김
            comment = comment_form.save(commit=False)
            # 누락했던 값을 몇번 게시글에 작성될 글인지 작성하고
            comment.notice = notice
            # 현재 댓글을 달려는 사용자를 외래키로 추가해야 댓글이 달림
            # user와 comments를 1:N 으로 관계를 설정하였기 때문
            comment.user = request.user
            # 저장
            comment.save()
        return redirect('notices:detail', notice.pk)
    # 사용자 인증에 실패한 경우
    return redirect('accounts:login')

# Delete : 댓글 생성
# 현재 없는 notice의 pk를 얻기 위한 방법 2 : variable routing
# def comment_delete(request, article_pk, comment_pk):
# 2번을 사용, 이유는 url 구조의 일관성 유지를 위해
@require_POST
def comment_delete(request, notice_pk, comment_pk):
    # 인증된 사용자만 접근
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        # 현재 없는 notice의 pk를 얻기 위한 방법 1. notice = comment.notice.pk
        # 인증된 사용자 중 댓글 작성자와 같은 사람만 삭제 가능
        # 가리는 것보다 view에서 막는게 더 좋음, 보안 신경 쓰기
        if request.user == comment.user:
            comment.delete()
    return redirect('notices:detail', notice_pk)


@require_POST
def likes(request, notice_pk):
    if request.user.is_authenticated:
        notice = get_object_or_404(Notice, pk=notice_pk)
        # 이 게시글에 좋아요를 누른 유저 목록에 현재 요청하는 유저가 있다면
        # exists : 쿼리셋에 결과의 포함여부에 따라 boolean 형식으로 결과 반환
        if notice.like_users.filter(pk=request.user.pk).exists():
            # 좋아요 취소
            notice.like_users.remove(request.user)
        else:
            notice.like_users.add(request.user)
        return redirect('notices:index')
    return redirect('accounts:login')
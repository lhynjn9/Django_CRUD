import django
from django.shortcuts import render, redirect, get_object_or_404
# login 함수와 view의 login 함수명이 동일하여 충돌이 발생할 수 있어, 재명명
from django.contrib.auth import login as auth_login
# logout 함수와 view의 logout 함수명이 동일하여 충돌이 발생할 수 있어, 재명명
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_http_methods, require_POST
# login, signup, change_password
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
# 로그인한 사용자만 접근 가능하도록 제한하는 데코레이터
from django.contrib.auth.decorators import login_required
# update, signup : 재정의 form 사용
from .forms import CustomUserChangeForm, CustomUserCreationForm
# 암호 변경 시, 세션 무효화 방지
from django.contrib.auth import update_session_auth_hash, get_user_model

# 세션 생성
@require_http_methods(['GET', 'POST']) # 특정 메서드만 처리하도록 데코레이터 추가
def login(request):
    # 로그인 상태의 사용자가 접근한다면, 로그인 로직을 할 필요가 없으므로 첫 화면으로 redirect 진행
    if request.user.is_authenticated:
        return redirect('notices:index')
    if request.method == 'POST':
        # DB를 변경하는 것이 아닌 단순히 인증(세션 생성)을 위한 것이므로 Form Class사용
        # AuthenticationForm는 request를 첫번재 인자로 취하는 Form Class로 로그인을 위한 인증된 사용자 객체를 만들기 위해 사용됨
        # Form Class인 것은 매개변수로도 확인할 수 있음, ModelForm은 매개변수가 request.POST로 시작
        # 사용자 로그인을 위함 AuthenticationForm으로 데이터를 받음
        form = AuthenticationForm(request, request.POST)
        # 유효성 검사
        if form.is_valid():
            # 로그인 함수를 이용하여 세션에 user의 id를 저장
            # 브라우저에는 세션 키만 제공하고, 데이터는 서버가 가지고 있음
            # get_user() : AuthenticationForm의 인스턴스 메서드로 유효성 검사 통과 시, 로그인 한 사용자 객체를 할당
            # 세션 생성 -> 데이터베이스의 장고 세션 테이블에서 생성확인 가능
            auth_login(request, form.get_user()) 
            # 로그인이 중간에 정상적으로 진행될 경우, 기존 주소로 redirect하기 위해 next(@login_required)에 저장된 주소를 처리해줌
            # 처리하지 않으면 기존에 로그인 후 redirect 한 주소로 이동
            return redirect(request.GET.get('next') or 'notices:index')

    # 전달되는 로그인 데이터가 없다면(=POST가 아닌 GET 메소드로 단순 조회일 경우)
    else: 
        # 기본 객체를 받음
        form = AuthenticationForm()

    context = {
        'form' : form
    }
    return render(request, 'accounts/login.html', context)

# 세션 삭제
@require_POST
def logout(request):
    # 로그인 상태의 사용자만 로그아웃에 접근 가능해야 함
    if request.user.is_authenticated:
        auth_logout(request) # 세션 삭제 : 이전 사용자의 세션 데이터에 액세스 하는 것을 방지하기 위함
    return redirect('notices:index')

# 회원가입
@require_http_methods(['GET', 'POST']) # 특정 메서드만 처리하도록 데코레이터 추가
def singup(request):
    # 인증되지 않은 사용자만 회원가입 진행 가능
    if request.user.is_authenticated:
        return redirect('notices:index')
    # 회원가입 정보가 전달된다면
    if request.method == 'POST':
        # 전달받은 데이터를 저장하고
        # 커스텀한 User 모델로 대체한 form 사용
        form = CustomUserCreationForm(request.POST)
        # 전달받은 데이터의 유효성을 검사
        if form.is_valid():
            # 유효하다면, 저장
            user = form.save()
            # 저장한 사용자 객체 정보로 회원가입 후, 자동 로그인 진행
            # 로그인 함수 사용
            auth_login(request, user)
            return redirect('notices:index')

    # 전달되는 데이터가 없다면(=POST가 아닌 GET 메소드로 단순 조회일 경우)
    else:
        # 기본 객체를 저장
        # 커스텀 User 모델로 대체한 form 사용
        form = CustomUserCreationForm()
    
    context = {
        'form' : form,
    }

    return render(request, 'accounts/signup.html', context)

# 회원탈퇴
@require_POST
def delete(request):
    # 로그인한 회원만 접근가능해야함
    if request.user.is_authenticated:
        # 로그인한 회원의 회원탈퇴 진행
        request.user.delete()
        # 탈퇴 후, 세션 데이터도 삭제
        # 로그아웃 함수 이용
        # 세션 데이터를 먼저 삭제할 경우, 회원 정보가 없어 탈퇴를 진행할 수 없음
        auth_logout(request)
    return redirect('notices:index')


# 회원정보수정
# 사용자 정보 및 권한 변경을 위한 Form이 있지만, 사용자에 따라 접근 할 수 정보가 달라야 하므로
# UserChangeForm의 필드를 선택하여 제공할 필요가 있음(이를 위해 forms.py 생성)
# 수정한 form(CustomUserChangeForm)을 이용하여 작성
@login_required # 로그인한 사용자만 접근 가능
@require_http_methods(['GET', 'POST']) # 특정 메서드만 처리하도록 데코레이터 추가
def update(request):
    # 수정된 정보가 들어온다면,
    if request.method == 'POST':
        # 저장하고
        form = CustomUserChangeForm(request.POST, instance=request.user)
        # 유효성 검사를 진행
        if form.is_valid():
            # 유효하다면, 저장
            form.save()
            return redirect('notices:index')

    # 전달되는 데이터가 없다면(=POST가 아닌 GET 메소드로 단순 조회일 경우)
    else:
        # 기본 객체 저장
        form = CustomUserChangeForm(instance=request.user)
    
    context = {
        'form' : form,
    }

    return render(request, 'accounts/update.html', context)

# 비밀번호 변경
@login_required # 로그인한 사용자만 접근 가능
@require_http_methods(['GET', 'POST']) # 특정 메서드만 처리하도록 데코레이터 추가
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('notices:index')
    
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form' : form,
    }
    return render(request, 'accounts/change_password.html', context)

# 사용자 프로필 조회
def profile(request, username):
    User = get_user_model()
    person = get_object_or_404(User, username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)

# 팔로우 관계 설정
@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:
        # 현재 팔로우를 당한 사람 : you
        you = get_object_or_404(get_user_model(), pk=user_pk)
        # 그 팔로우를 요청한 사람 : me
        me = request.user

        if me != you:
            # 현재 팔로우를 하고 있는 상태이면
            if you.followers.filter(pk=me.pk).exists():
                # 언팔로우
                you.followers.remove(me)
            # 현재 팔로우를 하지 않은 상태이면
            else:
                # 팔로우
                you.followers.add(me)
        return redirect('accounts:profile', you.username)
    return redirect('accounts:login')
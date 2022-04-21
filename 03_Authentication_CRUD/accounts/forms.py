from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model


# 사용자 정보 및 권한 변경을 위한 Form이 있지만, 사용자에 따라 접근 할 수 정보가 달라야 하므로
# UserChangeForm의 필드를 선택하여 제공할 필요가 있음(이를 위해 forms.py 생성)
# 회원정보 수정 form
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        # 커스텀 User 모델로 대체
        # get_user_model()은 현재 활성화된 사용자 모델을 반환
        model = get_user_model() # User
        # 필요한 필드만 선택해서 작성
        fields = ('email', 'first_name', 'last_name',)


 
class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        # 커스텀 User 모델로 대체
        # get_user_model()은 현재 활성화된 사용자 모델을 반환
        model = get_user_model()
        #회원가입시, 이메일 추가
        fields = UserCreationForm.Meta.fields + ('email', )

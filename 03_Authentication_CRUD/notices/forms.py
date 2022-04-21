from django import forms
from .models import Notice

# Form 선언
# class NoticeForm(forms.Form):
#     title = forms.CharField(max_length=10)
#     content = forms.CharField()

# Form으로 선언한 것을 ModelForm으로 선언
class NoticeForm(forms.ModelForm):
    # widgets을 활용한 input 요소 표현
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'my-title form-control',
                'placeholder': '제목을 입력해주세요',
            }
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'my-content form-control',
            }
        ),
        error_messages={
            'required': '내용을 입력해주세요',
        }
    )

    class Meta:
        # 어떤 모델을 기반으로 Form을 작성할 것인지 작성
        model = Notice 
        fields = '__all__'
        # exclude : 특정 필드를 제외할 때 사용, fields와 동시 사용 불가
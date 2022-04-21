from django.contrib import admin
from .models import Notice


# model에 정의한 필드의 값을 admin 페이지에 출력하도록 설정
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'content', 'created_at', 'updated_at',)

# admin site에 Notice 객체를 register하겠다는 의미
admin.site.register(Notice, NoticeAdmin)

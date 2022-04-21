from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # app url mapping : 각 앱들의 url을 포함시킴
    path('notices/', include('notices.urls')),
    path('accounts/', include('accounts.urls')),
]
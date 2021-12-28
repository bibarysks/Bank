from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('bank.urls', namespace='bank')),
    path('admin/', admin.site.urls),
]


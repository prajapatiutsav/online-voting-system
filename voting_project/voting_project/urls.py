from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),   # ✅ MUST BE HERE
    path('', include('voting_app.urls')),
]   
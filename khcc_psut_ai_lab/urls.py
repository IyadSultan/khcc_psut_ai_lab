from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analytics/', include('gold_analytics.urls')),
    # ... your other URL patterns
] 
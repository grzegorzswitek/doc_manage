"""panel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin

from .settings import STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT
from .views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, Zarejestruj, index

urlpatterns = [
    path('zarejestruj/', Zarejestruj.as_view(), name='zarejestruj'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('dokumentacja/', include('dokumentacja.urls')),
    path('admin/', admin.site.urls),
    path('', index, name='index'),
] + static(STATIC_URL, document_root=STATIC_ROOT) \
  + static(MEDIA_URL, document_root=MEDIA_ROOT)

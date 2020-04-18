"""social_network URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from social.views import Post_view, Like_view, Analitic_view, User_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/post/', Post_view.as_view()),
    path('api/', include('rest_auth.urls')),
    path('api/register/', include('rest_auth.registration.urls')),
    path('api/like/', Like_view.as_view()),
    path('api/analitics/', Analitic_view.as_view()),
    path('api/user_detail/', User_view.as_view())

]

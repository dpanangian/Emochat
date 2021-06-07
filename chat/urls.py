from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.signup import SignUpView
from core.login import UserLoginView


urlpatterns = [

    path('admin/', admin.site.urls),

    path('', include('core.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

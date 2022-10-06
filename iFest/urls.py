"""iFest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from ifest2022 import views
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^$', views.welcome, name='welcome'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    #path('register', views.register, name='register'),
    path('home/', views.home, name='home'),
    path("signup/", views.signup, name="signup"),
    path('login_page/', views.home, name='login_page'),
    path('logout_page/', views.home, name="logout_page"),
    # path('profile/', views.profile, name='profile'),
    # path('editProfile/', views.editProfile, name='editProfile'),
    path('profile/', views.home, name='profile'),
    path('editProfile/', views.home, name='editProfile'),

    # path('events/', views.events, name='events'),
    # path('pronites/', views.pronites, name='pronites'),
    # path('speakers/', views.speakers, name='speakers'),
    # path('dashboard/',views.dashboard, name='dashboard'),
    # path('moreInfo/', views.moreInfo, name='moreInfo'),
    # path('team/', views.ifestTeam, name='ifestTeam'),
    # path('sponsors/', views.sponsors, name='sponsors'),
    
    # path('reset_password/',
    #      auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
    #      name="reset_password"),

    # path('reset_password_sent/',
    #      auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
    #      name="password_reset_done"),

    # path('reset/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
    #      name="password_reset_confirm"),

    # path('reset_password_complete/',
    #      auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),
    #      name="password_reset_complete"),

    # path('iohunt/', include('iohunt.urls')),
    # path('quiz/', include('quiz.urls'))

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
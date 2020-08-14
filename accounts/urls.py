from django.urls import path
from django.contrib.auth import views as auth_views


from .views import signup, logoutfunc

urlpatterns = [
    path('signup/', signup, name="signup"),
    path('logout/', logoutfunc, name="logout"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]

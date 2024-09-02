from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name = "home"),
    path("login",views.loginpage, name="login"),
    path("handleSignup", views.handleSignup,name="handleSignup"),
    path("handleLogin", views.handleLogin,name="handleLogin"),
    path("handleLogout", views.handleLogout,name="handleLogout"),
    path("update", views.update, name="update"),
    path("signup", views.signup, name="signup"),
    path("createpost", views.createpost, name="createpost"),
]


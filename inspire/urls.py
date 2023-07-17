from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup, name="signup"),
    path("login", views.loginpage, name="login"),
    path("feed", views.feed, name="feed"),
    path("forgotpassword", views.forgotpassword, name="forgotpassword"),
    path("forgotpassword/change", views.changepassword, name="changepassword"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path("account", views.account, name="account"),
    path("account/settings", views.accountsettings, name="accountsettings"),
    path("staff", views.staff, name="staff"),
    path("staff/post/<slug:ptype>", views.staffpost, name="staffpost"),
    path("jsondata/<slug:data>/<int:minlimit>/<int:maxlimit>", views.jsondata, name="jsondatanoti"),
    path("jsondata/<slug:data>/<slug:avoid>/<int:maxPost>/<slug:postid>", views.jsondata, name="jsondatarelated"),
    path("post/<slug:postid>", views.post, name="post"),
]
from django.urls import path, re_path
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
    path("staff/post/<str:ptype>", views.staffpost, name="staffpost"),
    path("jsondata/<str:data>/<int:minlimit>/<int:maxlimit>", views.jsondata, name="jsondatanoti"),
    path("jsondata/<str:data>/<str:avoid>/<int:maxPost>/<str:postid>", views.jsondata, name="jsondatarelated"),
    path("jsondata/<str:data>/<str:avoid>/<str:query>/<int:maxPost>", views.jsondata, name="jsondataresults"),
    path("jsondata/<str:data>/<str:avoid>/<str:query>/<int:maxPost>/<str:cattype>/<str:order>", views.jsondata, name="jsondatacats"),
    path("jsondata/<str:data>/<str:avoid>/<int:maxPost>/<str:order>/fav", views.jsondata, name="jsondatafav"),
    path("post/<str:postid>", views.post, name="post"),
    path("search/<str:query>", views.search, name="search"),
    path("tag/<str:qtag>", views.tag, name="tag"),
    path("category", views.categories, name="categories"),
    re_path(r"^category/(?P<path>.*)/$", views.categories, name="categories"),
    path("favourites", views.favourites, name="favourites")
]
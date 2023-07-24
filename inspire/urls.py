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
    path("staff/post/<slug:ptype>", views.staffpost, name="staffpost"),
    path("jsondata/<slug:data>/<int:minlimit>/<int:maxlimit>", views.jsondata, name="jsondatanoti"),
    path("jsondata/<slug:data>/<slug:avoid>/<int:maxPost>/<slug:postid>", views.jsondata, name="jsondatarelated"),
    path("jsondata/<slug:data>/<slug:avoid>/<slug:query>/<int:maxPost>", views.jsondata, name="jsondataresults"),
    path("jsondata/<slug:data>/<slug:avoid>/<slug:query>/<int:maxPost>/<slug:cattype>/<slug:order>", views.jsondata, name="jsondatacats"),
    path("jsondata/<slug:data>/<slug:avoid>/<int:maxPost>/<slug:order>/fav", views.jsondata, name="jsondatafav"),
    path("post/<slug:postid>", views.post, name="post"),
    path("search/<slug:query>", views.search, name="search"),
    path("tag/<slug:qtag>", views.tag, name="tag"),
    path("category", views.categories, name="categories"),
    re_path(r"^category/(?P<path>.*)/$", views.categories, name="categories"),
    path("favourites", views.favourites, name="favourites")
]
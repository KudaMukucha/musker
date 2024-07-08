from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('profile-list',views.profile_list,name='profile-list'),
    path('profile/<int:pk>/',views.profile,name='profile'),
    path('profile/followers/<int:pk>/',views.followers,name='followers'),
    path('profile/follows/<int:pk>/',views.follows,name='follows'),
    path('login/',views.login_user,name='login'),
    path('logout',views.logout_user,name='logout'),
    path('register',views.register_user, name ='register'),
    path('update-user',views.update_user,name='update-user'),
    path('meep-like/<int:pk>/',views.meep_like,name='meep-like'),
    path('meep-show/<int:pk>/',views.meep_show,name='meep-show'),
    path('unfollow/<int:pk>/',views.unfollow,name='unfollow'),
    path('follow/<int:pk>/',views.follow,name='follow'),
    path('delete-meep/<int:pk>/',views.delete_meep,name='delete-meep'),
    path('edit-meep/<int:pk>/',views.edit_meep,name='edit-meep'),
    path('search/',views.search,name='search'),
    path('search-user/',views.search_user,name='search-user'),
]
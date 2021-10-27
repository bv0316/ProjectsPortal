from django.urls import path
from .import views
import users

urlpatterns=[
 path('login/', views.loginPage, name='login'),
 path('logout/', views.logoutUser, name = 'logout'),
  path('register/', views.registerUser, name = 'register'),
 path('', views.profiles, name='profiles'),
 path('profile/<str:pk>/', views.userProfile, name= 'user-profile'),
 path('account/', views.userAccount, name= 'account'),
 path('edit-account/', views.editAccount, name='edit-account'),
 path('create-projects/', views.createCurrentProject, name = 'create-projects'),
 path('update-projects/<str:pk>/', views.updateCurrentProject, name= 'update-projects'),
 path('delete-projects/<str:pk>/', views.deleteCurrentProject, name= 'delete-projects'),
 path('inbox/', views.inbox, name='inbox'),
 path('message/<str:pk>/', views.viewMessage, name='message'),
 path('create-message/<str:pk>/', views.createMessage, name='create-message')
]
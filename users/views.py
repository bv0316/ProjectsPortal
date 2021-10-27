from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, ProjectForm, MessageForm
from .models import Profile, Skill
from django.db.models import Q
from .utils import searchProfiles, paginateProfile

# Create your views here.
def loginPage(request):
 page ='login'
 if request.user.is_authenticated:
  return redirect('profiles')
 if request.method =='POST':
  print(request.POST)
  username = request.POST['username']
  password = request.POST['password']
  try:
   user = User.objects.get(username= username)
  except:
   messages.error(request,'User does not exist') 
  user = authenticate(request, username= username, password=password) 
  if user is not None:
   login(request, user)
   return redirect(request.GET['next'] if 'next' in request.GET else 'profiles' )
  else:
   messages.error(request,'Username or Pasword is incorrect') 
 return render(request, 'users/login_registration.html')

def logoutUser(request):
 logout(request)
 messages.info(request, 'User logged out')
 return redirect('login')

def registerUser(request):
 page ='register'
 form = CustomUserCreationForm()
 if request.method =='POST':
  form = CustomUserCreationForm(request.POST)
  if form.is_valid():
   user = form.save(commit=False)
   user.username = user.username.lower()
   user.save()

   messages.success(request, 'User was created successfully')

   login(request, user)
   return redirect('edit-account')
  else:
   messages.error(request, "An error has occured during registration")

 context ={'page':page, 'form':form}
 return render(request, 'users/login_registration.html', context)

def profiles(request):
 profiles, search_query=searchProfiles(request)
 custom_range, profiles = paginateProfile(request, profiles, 2)
 context = {"profiles":profiles, 'search_query':search_query, 'custom_range':custom_range}
 return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
 profile = Profile.objects.get(id=pk)
 projects = profile.skill_set.all()
 context ={'profile':profile, 'projects':projects}
 return render(request, 'users/user-profile.html', context)

@login_required(login_url="login")
def userAccount(request):
 profile = request.user.profile
 currentprojects = profile.skill_set.all()
 allprojects = profile.project_set.all()
 context ={'profile':profile, 'currentprojects':currentprojects, 'allprojects':allprojects}
 return render(request, 'users/account.html', context)

@login_required(login_url="login")
def editAccount(request):
 profile = request.user.profile
 form= ProfileForm(instance=profile)
 
 if request.method =='POST':
  form = ProfileForm(request.POST, request.FILES, instance =profile)
  if form.is_valid():
   form.save()

   return redirect('account')
 context ={'form': form}
 return render(request, 'users/profile_form.html', context)

@login_required(login_url="login")
def createCurrentProject(request):
 profile = request.user.profile
 currentprojects = profile.skill_set.all()
 form = ProjectForm()
 if request.method =='POST':
  form = ProjectForm(request.POST, request.FILES)
  if form.is_valid():
   project =form.save(commit=False)
   project.owner =profile
   project.save()
   return redirect('projects')

 context ={'form':form}
 return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def updateCurrentProject(request, pk):
 profile = request.user.profile 
 project = profile.skill_set.get(id=pk)
 form = ProjectForm(instance =project)
 if request.method =='POST':
  form = ProjectForm(request.POST,request.FILES, instance =project)
  if form.is_valid():
   form.save()
   return redirect('projects')

 context ={'form':form}
 return render(request, 'projects/project_form.html', context) 


@login_required(login_url="login")
def deleteCurrentProject(request, pk):
 profile = request.user.profile 
 project = profile.skill_set.get(id=pk)
 context = {'object':project}
 if request.method =='POST':
  project.delete()
  return redirect('projects')

 return render(request, 'projects/delete_template.html', context)

@login_required(login_url="login")
def inbox(request):
  profile = request.user.profile
  messageRequests = profile.messages.all()
  unreadCount = messageRequests.filter(is_read=False).count()
  context ={'messageRequests':messageRequests, 'unreadCount':unreadCount}
  return render(request, 'users/inbox.html', context)

def viewMessage(request, pk):
  profile = request.user.profile
  message = profile.messages.get(id=pk)
  if message.is_read== False:
    message.is_read =True
    message.save()
  context ={'message':message}
  return render(request, 'users/message.html', context)

def createMessage(request, pk):
  recipient = Profile.objects.get(id=pk)
  form = MessageForm()
  try:
    sender = request.user.profile
  except:
    sender =None
  if request.method =='POST':
    form = MessageForm(request.POST)
    if form.is_valid():
      message = form.save(commit=False)
      message.sender = sender
      message.recipient = recipient

      if sender:
        message.name = sender.name
        message.email = sender.email
      message.save() 
      messages.success(request, "Your message was sent successfully!")   
      return redirect('user-profile', pk= recipient.id) 
  context ={'recipient':recipient, 'form':form}
  return render(request, 'users/message_form.html', context)
  
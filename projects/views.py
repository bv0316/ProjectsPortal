from django.core import paginator
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils import searchProjects, paginateProjects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
# Create your views here.


def projects(request):
  projects, search_query= searchProjects(request)
  custom_range, projects = paginateProjects(request,projects, 3)
  context ={'projects':projects, 'search_query':search_query, 'custom_range': custom_range}
  return render(request, 'projects/projects.html', context)

def project(request, pk):
    projObj = Project.objects.get(id=pk)
    form = ReviewForm()
    if request.method =='POST':
      form = ReviewForm(request.POST)
      review = form.save(commit=False)
      review.project = projObj
      review.owner = request.user.profile
      review.save()
      messages.success(request,"Your Review was Successfully Posted")  
      return redirect('project', pk=projObj.id)

    print('projObj', projObj)
    return render(request, 'projects/single-project.html', {'project':projObj, 'form':form})

@login_required(login_url="login")
def createProject(request):
 profile = request.user.profile
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
def updateProject(request, pk):
 profile = request.user.profile 
 project = profile.project_set.get(id=pk)
 form = ProjectForm(instance =project)
 if request.method =='POST':
  form = ProjectForm(request.POST,request.FILES, instance =project)
  if form.is_valid():
   form.save()
   return redirect('projects')

 context ={'form':form}
 return render(request, 'projects/project_form.html', context) 

@login_required(login_url="login")
def deleteProject(request, pk):
 profile = request.user.profile 
 project = profile.project_set.get(id=pk)
 context = {'object':project}
 if request.method =='POST':
  project.delete()
  return redirect('projects')

 return render(request, 'projects/delete_template.html', context)
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from userprofile.models import Profile
from .models import *
from .forms import *


@login_required
@transaction.atomic
def add_project(request):
  current_user = get_object_or_404(Profile, user=request.user)
  if current_user.designation == 'man':
    if request.method == 'POST':
      project_form = ProjectForm(request.POST)

      if project_form.is_valid():
          project = project_form.save()
          messages.success(request, "Project Created Successfully")
          return redirect('detail-project', project.id)
      else:
          messages.error(request, "Project Creation Failed.")
    else:
        project_form = ProjectForm(request.POST)

    return render(request, "add_project.html", {'project_form': project_form})

  else:
    raise Http404

@login_required
@transaction.atomic
def update_project(request, id):
  current_user = get_object_or_404(Profile, user=request.user)
  if current_user.designation == 'man':
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
      project_form = ProjectForm(request.POST, instance=project)
      if project_form.is_valid():
          project_form.save()
          messages.success(request, "Project Updated Successfully")
          return redirect('detail-project', project.id)
      else:
          messages.error(request, "Project Updation Failed")
    else:
      project_form = ProjectForm(instance=project)
    return render(request, "add_project.html", {'project_form': project_form})
  else:
    raise Http404


@login_required
def delete_project(request, id):

  current_user = get_object_or_404(Profile, user=request.user)
  if current_user.designation == 'man':
    project = Project.objects.get(id = id)
    try:
      project.delete()
    except:

      return render(request, "delete_project.html", {'title':'Deletion Failed',
        'msg':"Deletion Failed. Employees are currently working on this project, so It can't be deleted."})

    messages.success(request, "Project Removed!")
  else:
    raise Http404

  return redirect('list-project')




class DetailProject(LoginRequiredMixin, DetailView):

  redirect_field_name = 'rt'
  template_name = 'view_project.html'
  context_object_name = 'project'
  allow_empty = False
  queryset = Project.objects.all()

  def get_context_data(self, **kwargs):
    context = super(DetailProject, self).get_context_data(**kwargs)

    current_user = get_object_or_404(Profile, user=self.request.user)
    context['designation'] = current_user.designation
    employees = Profile.objects.filter(project=get_object_or_404(Project, pk=self.kwargs['pk']))
    qaes = employees.filter(designation='qae')
    devs = employees.filter(designation='dev')
    print(qaes)
    print(devs)
    context['qaes'] = qaes
    context['devs'] = devs
    return context

  def get_object(self):
    current_user = get_object_or_404(Profile, user=self.request.user)
    if current_user.designation == 'man' or current_user.designation == 'qae' or (current_user.project and current_user.project.id == self.kwargs['pk']):
      return Project.objects.get(id=self.kwargs['pk'])
    else:
      raise Http404


class ListProjects(LoginRequiredMixin, ListView):

  redirect_field_name = 'rt'
  model = Project
  template_name = 'list_projects.html'
  context_object_name = 'project_list'
  # allow_empty = False

  def get_queryset(self):
    current_user = get_object_or_404(Profile, user=self.request.user)
    if current_user.designation == 'man' or current_user.designation == 'qae':
      return Project.objects.all()
    else:
      raise Http404

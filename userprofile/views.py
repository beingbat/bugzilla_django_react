from http.client import HTTPResponse
from operator import index
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from userprofile.models import Profile
from django.http import Http404, HttpResponse as hr
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
import userprofile.forms as ff
from django.contrib import messages


def index_page(request):
  if(request.user.is_authenticated):
    profile = Profile.objects.get(pk=request.user).designation
  else:
    profile = ""

  print(type(profile), ": ", profile, "\n")

  context = {
    "user": request.user,
    "user_type": profile,
    }

  return render(request, 'index.html', context)

@login_required
@transaction.atomic
def add_user(request):
    try:
      current_user = Profile.objects.get(user=request.user)
      if current_user.designation == 'man':
        if request.method == 'POST':
              user_form = ff.UserRegisterForm(request.POST)
              cust_form = ff.ProfileForm(request.POST)
              if user_form.is_valid() and cust_form.is_valid():
                  user = user_form.save()
                  profile = cust_form.save()
                  profile.user = user
                  profile.save()
                  messages.success(request, f'Account has been created! You can now log in.')
                  return redirect('dashboard')
              else:
                  messages.error(request, f'Please correct the errors.')
        else:
            user_form = ff.UserRegisterForm(request.POST)
            profile_form = ff.ProfileForm(request.POST)
        return render(request, "user_add.html", {'user_form': user_form, 'profile_form': profile_form})
      else:
        raise Http404
    except:
      raise Http404


@login_required
def delete_user(request, id):
    try:
      current_user = Profile.objects.get(user=request.user)
      if current_user.designation == 'man':
        u = User.objects.get(id = id)
        u.delete()
        messages.success(request, "The user is deleted")
      else:
        raise Http404
    except:
      raise Http404

    return redirect(index_page)


class UserDetailView(LoginRequiredMixin, DetailView):

  redirect_field_name = 'rt'

  template_name = 'profile_view.html'
  context_object_name = 'user_profile'
  allow_empty = False
  queryset = Profile.objects.all()

  def get_object(self):

    try:
      current_user = Profile.objects.get(user=self.request.user)
      if current_user.designation == 'man':
        return Profile.objects.get(user=User.objects.get(id=self.kwargs['pk']))
      else:
        raise Http404
    except:
      raise Http404


class UserListView(LoginRequiredMixin, ListView):

  redirect_field_name = 'rt'
  model = Profile

  template_name = 'profile_list.html'
  context_object_name = 'user_list'
  allow_empty = False

  def get_queryset(self):
        try:
          current_user = Profile.objects.get(user=self.request.user)
          if current_user.designation == 'man':
            return Profile.objects.filter(designation=self.kwargs['slug'])
          else:
            raise Http404
        except:
          raise Http404

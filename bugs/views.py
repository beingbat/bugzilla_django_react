from django.shortcuts import render
from django.http import HttpResponse


def view_bug(request):
  return render(request, "view_bug.html", {})

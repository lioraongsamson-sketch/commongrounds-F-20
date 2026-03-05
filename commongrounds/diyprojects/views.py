from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Project


class ProjectListView(ListView):
    model = Project
    template_name = "project_list.html"


class ProjectDetailView(DetailView):
    model = Project
    template_name = "project_detail.html"

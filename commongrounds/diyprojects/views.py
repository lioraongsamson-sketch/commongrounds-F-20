from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import Avg

from .models import Project, Favorite, ProjectReview, ProjectRating
from .forms import ProjectForm, ReviewForm, RatingForm
from accounts.mixins import RoleRequiredMixin


class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = "project_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            context['created_projects'] = Project.objects.filter(creator=profile)
            context['favorited_projects'] = Project.objects.filter(favorites__profile=profile)
            context['reviewed_projects'] = Project.objects.filter(reviews__reviewer=profile)

        return context


class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'project'
    template_name = "project_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()

        context['average_rating'] = project.ratings.aggregate(avg=Avg('score'))['avg']

        context['reviews'] = project.reviews.all()
        context['favorites_count'] = project.favorites.count()

        if self.request.user.is_authenticated:
            context['user_has_favorited'] = project.favorites.filter(
                profile=self.request.user.profile
            ).exists()
        else:
            context['user_has_favorited'] = False

        context['rating_form'] = RatingForm()
        context['review_form'] = ReviewForm()
        
        return context

    def post(self, request, *args, **kwargs):
        project = self.get_object()

        if not request.user.is_authenticated:
            return redirect('/accounts/login/')

        if 'rate' in request.POST:
            form = RatingForm(request.POST)
            if form.is_valid():
                rating = form.save(commit=False)
                rating.project = project
                rating.profile = request.user.profile
                rating.save()

        if 'review' in request.POST:
            form = ReviewForm(request.POST, request.FILES)
            if form.is_valid():
                review = form.save(commit=False)
                review.project = project
                review.reviewer = request.user.profile
                review.save()

        if 'favorite' in request.POST:
            project.favorites.get_or_create(
                profile=request.user.profile
            )

        return redirect('diyprojects:project_detail', pk=project.pk)


class ProjectCreateView(RoleRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_create.html'
    success_url = reverse_lazy('diyprojects:project_list')

    required_role = "Project Creator"

    def form_valid(self, form):
        form.instance.creator = self.request.user.profile
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ProjectUpdateView(RoleRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_update.html'
    success_url = reverse_lazy('diyprojects:project_list')

    required_role = "Project Creator"

    def get_queryset(self):
        return Project.objects.filter(creator=self.request.user.profile)

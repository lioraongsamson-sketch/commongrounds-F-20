from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .models import Commission, Job
from django.db.models import Sum, Q
from .forms import JobApplicationForm, CommissionForm


class CommissionListView(ListView):
    model = Commission
    template_name = "request_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            pf = self.request.user.profile
            ctx['created_commissions'] = Commission.objects.filter(
                maker=pf
            ).distinct()
            ctx['applied_commissions'] = Commission.objects.filter(
                job__applications__applicant=pf
            ).distinct()
            ctx['remaining_commissions'] = Commission.objects.exclude(
                job__applications__applicant=pf).exclude(
                maker=pf
            ).distinct()
        else:
            ctx['all_commissions'] = Commission.objects.all()

        return ctx


class CommissionDetailView(DetailView):
    model = Commission
    template_name = "request_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        jobs = self.object.job.all()

        total_manpower = jobs.aggregate(Sum('manpower_required'))[
            'manpower_required__sum'] or 0

        accepted_signees = jobs.aggregate(
            accepted=Sum('applications', filter=Q(
                applications__status='A'))
        )['accepted'] or 0

        ctx['total_manpower'] = total_manpower
        ctx['open_manpower'] = total_manpower - accepted_signees
        return ctx

    def post(self, request, *args, **kwargs):
        form = JobApplicationForm(request.POST)
        self.object = self.get_object()

        if form.is_valid():
            form.save()
            return self.get(request, *args, **kwargs)

        else:
            self.object_list = self.get_queryset()
            ctx = self.get_context_data(**kwargs)
            ctx['application'] = form
            return self.render_to_response(ctx)


class CommissionCreateView(LoginRequiredMixin, CreateView):
    model = Commission
    template_name = "request_form.html"
    form_class = CommissionForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['previous'] = 'Create a'
        return ctx

    def post(self, request, *args, **kwargs):
        form = CommissionForm(request.POST)
        if form.is_valid():
            form.instance.maker = self.request.user.profile
            form.save()
            return self.get(request, *args, **kwargs)
        else:
            self.object_list = self.get_queryset(**kwargs)
            ctx = self.get_context_data(**kwargs)
            ctx['form'] = form
            return self.render_to_response(ctx)


class CommissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Commission
    template_name = "request_form.html"
    fields = '__all__'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['previous'] = 'Update your'
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommissionForm(request.POST, instance=self.object)
        if form.is_valid():
            form.instance.maker = self.request.user.profile
            form.save()

            jobs = form.instance.job.all()
            all_jobs_full = all(j.status == j.STATUSES[1] for j in jobs)

            if jobs.exists() and all_jobs_full:
                form.status = Commission.STATUSES[1]

            form.save()

            return redirect(form.instance.get_absolute_url())

        else:
            self.object_list = self.get_queryset(**kwargs)
            ctx = self.get_context_data(**kwargs)
            ctx['form'] = form
            return self.render_to_response(ctx)

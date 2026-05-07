from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .models import Commission, Job
from django.db.models import Sum, Q
from .forms import JobApplicationForm, CommissionForm, JobFormSet
from accounts.mixins import RoleRequiredMixin


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


class CommissionCreateView(RoleRequiredMixin, LoginRequiredMixin, CreateView):
    model = Commission
    template_name = "request_form.html"
    form_class = CommissionForm
    required_role = "Commission Maker"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['previous'] = 'Create a'
        if 'job_formset' not in ctx:
            ctx['job_formset'] = JobFormSet()
        print(str("HELLO") + str(ctx['job_formset']))
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = None
        form = CommissionForm(request.POST)
        job_formset = JobFormSet(request.POST)

        if form.is_valid() and job_formset.is_valid():
            commission = form.save(commit=False)
            commission.maker = self.request.user.profile
            commission.save()
            job_formset.instance = commission
            job_formset.save()
            return redirect(form.instance.get_absolute_url())
        else:
            ctx = self.get_context_data(**kwargs)
            ctx['form'] = form
            ctx['job_formset'] = job_formset
            return self.render_to_response(ctx)


class CommissionUpdateView(RoleRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Commission
    template_name = "request_form.html"
    form_class = CommissionForm
    required_role = "Commission Maker"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['previous'] = 'Update your'
        if 'job_formset' not in ctx:
            ctx['job_formset'] = JobFormSet(instance=self.object)
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommissionForm(request.POST, instance=self.object)
        job_formset = JobFormSet(request.POST, instance=self.object)

        if form.is_valid() and job_formset.is_valid():
            form.instance.maker = self.request.user.profile
            commission = form.save()

            for job_form in job_formset:
                if job_form.cleaned_data and not job_form.cleaned_data.get('DELETE', False):
                    if job_form.cleaned_data.get('role') and job_form.cleaned_data.get('manpower_required'):
                        job = job_form.save(commit=False)
                        job.commission = commission
                        job.save()

            commission.update_status()
            return redirect(commission.get_absolute_url())

        else:
            ctx = self.get_context_data(**kwargs)
            ctx['form'] = form
            ctx['job_formset'] = job_formset
            return self.render_to_response(ctx)

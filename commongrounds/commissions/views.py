from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Commission, Job
from django.db.models import Sum, Q
from .forms import JobApplicationForm, CommissionForm


# STATUSES = [('O', 'Open'), ('F', 'Full'),('C', 'Completed'), ('D', 'Discontinued')]

class CommissionListView(ListView):
    model = Commission
    template_name = "request_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            pf = self.request.user.profile
            ctx['created_commissions'] = Commission.objects.filter(
                maker=pf
            )
            ctx['applied_commissions'] = Commission.objects.filter(
                job__job_application__applicant=pf
            )
            ctx['remaining_commissions'] = Commission.objects.exclude(
                job__job_application__applicant=pf).exclude(
                maker=pf
                ) 
        else:
            ctx['all_commissions'] = Commission.objects.all()

        return ctx

    # NOT COMPLETED: SORTING


class CommissionDetailView(DetailView):
    model = Commission
    template_name = "request_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        jobs = self.object.job.all()

        total_manpower = jobs.aggregate(Sum('manpower_required'))
        mp = total_manpower['manpower_required__sum'] or 0

        accepted_signees = jobs.aggregate(
            accepted=Sum('job_application', filter=Q(job_application__status='A'))
        )['accepted'] or 0


        ctx['total_manpower'] = mp
        ctx['open_manpower'] = mp - accepted_signees

        return ctx
    
    def post(self, request, *args, **kwargs):
        job_app = JobApplicationForm(request.POST)
        self.object = self.get_object()

        if job_app.is_valid():
            job_app.save()
            return self.get(request, *args,**kwargs)

        else:
            self.object_list = self.get_queryset()
            ctx = self.get_context_data(**kwargs)
            ctx['application'] = job_app
            return self.render_to_response(ctx)



class CommissionCreateView(LoginRequiredMixin, CreateView):
    model = Commission
    template_name = "request_form.html"
    form_class = CommissionForm

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



class CommissionUpdateView(UpdateView):
    model = Commission
    template_name = "request_form.html"
    fields = '__all__'

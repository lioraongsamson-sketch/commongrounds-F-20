from django.contrib import admin
from .models import Commission, CommissionType, Job, JobApplication


class CommissionTypeInline(admin.TabularInline):
    model = Commission


class CommissionInline(admin.TabularInline):
    model = Job


class JobInline(admin.TabularInline):
    model = JobApplication


class CommissionTypeAdmin(admin.ModelAdmin):
    model = CommissionType
    inlines = [CommissionTypeInline,]


class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    inlines = [CommissionInline,]


class JobAdmin(admin.ModelAdmin):
    model = Job
    inlines = [JobInline,]


class JobApplicationAdmin(admin.ModelAdmin):
    model = JobApplication


admin.site.register(CommissionType, CommissionTypeAdmin)
admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)

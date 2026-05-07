from django.db import models
from django.urls import reverse
from accounts.models import Profile


class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Commission(models.Model):
    STATUSES = [('O', 'Open'), ('F', 'Full')]

    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.ForeignKey(
        CommissionType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='commissions'
    )
    maker = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        related_name='commissions'
    )
    people_required = models.PositiveIntegerField()
    status = models.CharField(choices=STATUSES, default=STATUSES[0])
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('commissions:request_detail', args=[str(self.id)])

    class Meta:
        ordering = ["created_on"]


class Job(models.Model):
    STATUSES = [('O', 'Open'), ('F', 'Full')]
    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        null=True,
        related_name='job'
    )
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(choices=STATUSES, default=STATUSES[0])

    def __str__(self):
        return str(self.commission.title + ": " + self.role)
    
    def get_accepted_apps(self):
        return self.job_application.filter(status=JobApplication.STATUSES[1][0]).count()
    
    def is_full(self):
        return self.get_accepted_apps() >= self.manpower_required

    class Meta:
        ordering = ["status", "-manpower_required", "role"]


class JobApplication(models.Model):
    STATUSES = [('P', 'Pending'), ('A', 'Accepted'), ('R', 'Rejected')]
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        null=True,
        related_name='job_application'
    )
    applicant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        related_name='job_application'
    )
    status = models.CharField(choices=STATUSES, default=STATUSES[0])
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.applicant.display_name + ": " + self.job.role)

    class Meta:
        ordering = ["status", "-applied_on"]

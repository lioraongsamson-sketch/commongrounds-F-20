from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import Profile


class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name']


class Project(models.Model):
    STATUS_CHOICES = [
        ('Backlog', 'Backlog'),
        ('To-Do', 'To-Do'),
        ('Done', 'Done'),
    ]
    
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='project'
    )
    creator = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True
    )
    description = models.TextField()
    materials = models.TextField()
    steps = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('diyprojects:project_detail', args=[str(self.id)])

    class Meta:
        ordering = ['-created_on']


class Favorite(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="favorites")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_favorited = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile} - {self.project}"


class ProjectReview(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.TextField()
    image = models.ImageField(upload_to='reviews/', blank=True, null=True)

    def __str__(self):
        return f"Review by {self.reviewer}"


class ProjectRating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="ratings")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f"{self.score} - {self.project}"

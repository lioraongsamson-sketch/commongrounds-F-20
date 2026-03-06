from django.contrib import admin

from .models import Project, ProjectCategory


class ProjectCategoryInLine(admin.TabularInline):
    model = Project


class ProjectAdmin(admin.ModelAdmin):
    model = ProjectCategory
    inlines = [ProjectCategoryInLine,]


admin.site.register(ProjectCategory, ProjectAdmin)

from django.contrib import admin

from .models import Project, ProjectCategory


class ProjectCategoryInLine(admin.TabularInline):
    model = Project


class ProjectAdmin(admin.ModelAdmin):
    model = Project


class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory
    inlines = [ProjectCategoryInLine,]


admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Project, ProjectAdmin)

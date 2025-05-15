from django.contrib import admin
from .models import Project, ProjectImage, Partner, ProjectPhase, ProjectOutcome, Tag


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 100px; max-width: 100px;" />'
        return "No Image"

    image_preview.allow_tags = True
    image_preview.short_description = "Preview"


class ProjectPhaseInline(admin.TabularInline):
    model = ProjectPhase
    extra = 1


class ProjectOutcomeInline(admin.TabularInline):
    model = ProjectOutcome
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "year", "location", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "description", "location")
    list_filter = ("category", "year", "tags")
    filter_horizontal = ("tags",)
    inlines = [
        ProjectImageInline,
        ProjectPhaseInline,
        ProjectOutcomeInline,
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ["created_at", "updated_at"]
        return []


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    filter_horizontal = ("projects",)

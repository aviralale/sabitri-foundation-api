from django.contrib import admin
from .models import TeamMember, Contact, Testimonial, ContactFAQ, MembershipFAQ


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    """Admin configuration for TeamMember model."""

    list_display = ("name", "designation", "role", "order", "is_active")
    list_filter = ("is_active", "role")
    search_fields = ("name", "designation", "bio")
    ordering = ("order", "name")
    list_editable = ("order", "is_active")
    fieldsets = (
        (
            "Personal Information",
            {"fields": ("name", "designation", "role", "bio", "image")},
        ),
        ("Contact Information", {"fields": ("email", "linkedin_profile")}),
        ("Display Settings", {"fields": ("order", "is_active")}),
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin configuration for Contact model."""

    list_display = ("full_name", "email", "inquiry_type", "created_at", "responded")
    list_filter = ("inquiry_type", "responded", "created_at")
    search_fields = ("first_name", "last_name", "email", "message")
    readonly_fields = ("created_at", "updated_at")
    list_editable = ("responded",)
    fieldsets = (
        (
            "Contact Information",
            {"fields": ("first_name", "last_name", "email", "phone_number")},
        ),
        ("Inquiry Details", {"fields": ("inquiry_type", "message")}),
        ("Response", {"fields": ("responded", "response_notes")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Admin configuration for Testimonial model."""

    list_display = ("name", "designation", "company", "rating", "is_featured")
    list_filter = ("is_featured", "rating")
    search_fields = ("name", "designation", "company", "message")
    list_editable = ("is_featured", "rating")
    fieldsets = (
        ("Author Information", {"fields": ("name", "designation", "company", "image")}),
        ("Testimonial Content", {"fields": ("message", "rating")}),
        ("Display Settings", {"fields": ("is_featured",)}),
    )


@admin.register(ContactFAQ)
class ContactFAQAdmin(admin.ModelAdmin):
    """Admin configuration for ContactFAQ model."""

    list_display = ("question", "category", "order", "is_published")
    list_filter = ("is_published", "category")
    search_fields = ("question", "answer")
    list_editable = ("order", "is_published")
    fieldsets = (
        ("FAQ Content", {"fields": ("question", "answer", "category")}),
        ("Display Settings", {"fields": ("order", "is_published")}),
    )


@admin.register(MembershipFAQ)
class MembershipFAQAdmin(admin.ModelAdmin):
    """Admin configuration for MembershipFAQ model."""

    list_display = ("question", "category", "order", "is_published")
    list_filter = ("is_published", "category")
    search_fields = ("question", "answer")
    list_editable = ("order", "is_published")
    fieldsets = (
        ("FAQ Content", {"fields": ("question", "answer", "category")}),
        ("Display Settings", {"fields": ("order", "is_published")}),
    )

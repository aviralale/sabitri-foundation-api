from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class TimeStampedModel(models.Model):
    """Abstract base model with created and modified timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TeamMember(TimeStampedModel):
    """Model for team members."""

    name = models.CharField(_("Full Name"), max_length=65)
    designation = models.CharField(_("Job Title"), max_length=100)
    role = models.CharField(_("Role"), max_length=40)
    bio = models.TextField(_("Biography"), blank=True)
    image = models.ImageField(_("Profile Image"), upload_to="team_members/")
    email = models.EmailField(_("Email Address"), blank=True)
    linkedin_profile = models.URLField(_("LinkedIn Profile"), blank=True)
    order = models.PositiveIntegerField(
        _("Display Order"), default=0, help_text=_("Order in which team member appears")
    )
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Team Member")
        verbose_name_plural = _("Team Members")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Contact(TimeStampedModel):
    """Model for contact form submissions."""

    INQUIRY_CHOICES = [
        ("partnership", _("Partnership Inquiry")),
        ("volunteer", _("Volunteering")),
        ("donation", _("Donation")),
        ("media", _("Media Inquiry")),
        ("careers", _("Careers")),
        ("other", _("Other")),
    ]

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message=_(
            "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        ),
    )

    first_name = models.CharField(_("First Name"), max_length=24)
    last_name = models.CharField(_("Last Name"), max_length=24)
    email = models.EmailField(_("Email Address"))
    phone_number = models.CharField(
        _("Phone Number"), validators=[phone_regex], max_length=20, blank=True
    )
    inquiry_type = models.CharField(
        _("Inquiry Type"), max_length=50, choices=INQUIRY_CHOICES, default="general"
    )
    message = models.TextField(_("Message"))
    responded = models.BooleanField(_("Responded"), default=False)
    response_notes = models.TextField(_("Response Notes"), blank=True)

    class Meta:
        verbose_name = _("Contact Submission")
        verbose_name_plural = _("Contact Submissions")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Testimonial(TimeStampedModel):
    """Model for client testimonials."""

    name = models.CharField(_("Full Name"), max_length=65)
    designation = models.CharField(_("Job Title"), max_length=100)
    company = models.CharField(_("Company"), max_length=100, blank=True)
    message = models.TextField(_("Testimonial Message"))
    image = models.ImageField(
        _("Profile Image"), upload_to="testimonials/", null=True, blank=True
    )
    is_featured = models.BooleanField(_("Featured"), default=False)
    rating = models.PositiveSmallIntegerField(
        _("Rating"),
        choices=[(i, str(i)) for i in range(1, 6)],
        default=5,
        help_text=_("Rating from 1-5 stars"),
    )

    class Meta:
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonials")
        ordering = ["-is_featured", "-created_at"]

    def __str__(self):
        return f"{self.name}, {self.designation}"


class ContactFAQ(TimeStampedModel):
    """Model for frequently asked questions in the contact page."""

    question = models.TextField(_("Question"))
    answer = models.TextField(_("Answer"))
    category = models.CharField(_("Category"), max_length=50, blank=True)
    order = models.PositiveIntegerField(_("Display Order"), default=0)
    is_published = models.BooleanField(_("Published"), default=True)

    class Meta:
        verbose_name = _("Contact FAQ")
        verbose_name_plural = _("Contact FAQs")
        ordering = ["order", "question"]

    def __str__(self):
        return self.question


class MembershipFAQ(TimeStampedModel):
    """Model for frequently asked questions in the contact page."""

    question = models.TextField(_("Question"))
    answer = models.TextField(_("Answer"))
    category = models.CharField(_("Category"), max_length=50, blank=True)
    order = models.PositiveIntegerField(_("Display Order"), default=0)
    is_published = models.BooleanField(_("Published"), default=True)

    class Meta:
        verbose_name = _("Membership FAQ")
        verbose_name_plural = _("Membership FAQs")
        ordering = ["order", "question"]

    def __str__(self):
        return self.question

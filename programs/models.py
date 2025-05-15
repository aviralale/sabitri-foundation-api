from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Project(models.Model):
    CATEGORY_CHOICES = [
        ("Education", "Education"),
        ("Health", "Health"),
        ("Environment", "Environment"),
        ("Infrastructure", "Infrastructure"),
        ("Youth Development", "Youth Development"),
        ("Other", "Other"),
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    year = models.CharField(max_length=20)
    description = models.TextField()
    full_description = models.TextField()
    location = models.CharField(max_length=255)
    beneficiaries = models.CharField(max_length=255)
    duration = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, related_name="projects", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="project_images/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image for {self.project.title} ({self.order})"


class Partner(models.Model):
    name = models.CharField(max_length=255)
    projects = models.ManyToManyField(Project, related_name="partners")

    def __str__(self):
        return self.name


class ProjectPhase(models.Model):
    project = models.ForeignKey(
        Project, related_name="phases", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    complete = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} - {self.project.title}"


class ProjectOutcome(models.Model):
    project = models.ForeignKey(
        Project, related_name="outcomes", on_delete=models.CASCADE
    )
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Outcome for {self.project.title}"

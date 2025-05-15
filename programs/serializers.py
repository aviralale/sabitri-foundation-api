from rest_framework import serializers
from .models import Project, ProjectImage, Partner, ProjectPhase, ProjectOutcome, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class ProjectImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    class Meta:
        model = ProjectImage
        fields = ["id", "image", "image_url", "order"]


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ["id", "name"]


class ProjectPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPhase
        fields = ["id", "name", "duration", "complete", "order"]


class ProjectOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectOutcome
        fields = ["id", "description", "order"]


class ProjectListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category = serializers.CharField(source="get_category_display")
    tags = TagSerializer(many=True, read_only=True)

    def get_image(self, obj):
        # Get the first image of the project or return None
        first_image = obj.images.first()
        if first_image and first_image.image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(first_image.image.url)
            return first_image.image.url
        return None

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "description",
            "year",
            "image",
            "tags",
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)
    partners = PartnerSerializer(many=True, read_only=True)
    phases = ProjectPhaseSerializer(many=True, read_only=True)
    outcomes = ProjectOutcomeSerializer(many=True, read_only=True)
    related_projects = serializers.SerializerMethodField()
    category = serializers.CharField(source="get_category_display")
    tags = TagSerializer(many=True, read_only=True)

    def get_related_projects(self, obj):
        # Find related projects automatically based on shared attributes
        # Prioritize projects with same category and shared tags

        # Start with projects in the same category (excluding the current project)
        same_category = Project.objects.filter(category=obj.category).exclude(id=obj.id)

        # Find projects with shared tags
        projects_with_shared_tags = (
            Project.objects.filter(tags__in=obj.tags.all())
            .exclude(id=obj.id)
            .distinct()
        )

        # Combine and prioritize projects with both same category and shared tags
        # (they'll appear first in the list)
        related = list(
            same_category.filter(
                id__in=projects_with_shared_tags.values_list("id", flat=True)
            )
        )

        # Add remaining projects with shared tags
        for project in projects_with_shared_tags:
            if project not in related:
                related.append(project)

        # Add remaining projects with same category
        for project in same_category:
            if project not in related:
                related.append(project)

        # Limit to 5 related projects
        related = related[:5]

        # Serialize projects
        serialized_projects = []
        for project in related:
            # Get the first image or None
            first_image = project.images.first()
            image_url = None
            if first_image and first_image.image:
                request = self.context.get("request")
                if request:
                    image_url = request.build_absolute_uri(first_image.image.url)
                else:
                    image_url = first_image.image.url

            serialized_projects.append(
                {
                    "id": project.id,
                    "title": project.title,
                    "slug": project.slug,
                    "category": project.get_category_display(),
                    "image": image_url,
                }
            )

        return serialized_projects

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "year",
            "description",
            "full_description",
            "location",
            "beneficiaries",
            "duration",
            "images",
            "partners",
            "phases",
            "outcomes",
            "related_projects",
            "tags",
            "created_at",
            "updated_at",
        ]

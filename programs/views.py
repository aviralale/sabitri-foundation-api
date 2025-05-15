from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, ProjectImage, Partner, ProjectPhase, ProjectOutcome, Tag
from .serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    ProjectImageSerializer,
    PartnerSerializer,
    ProjectPhaseSerializer,
    ProjectOutcomeSerializer,
    TagSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint for projects
    """

    queryset = Project.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["category", "year", "tags"]
    search_fields = ["title", "description", "location"]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

    @action(detail=False)
    def categories(self, request):
        """Returns all available project categories"""
        categories = [
            {"id": choice[0], "name": choice[1]} for choice in Project.CATEGORY_CHOICES
        ]
        return Response(categories)

    @action(detail=False)
    def years(self, request):
        """Returns all project years"""
        years = Project.objects.values_list("year", flat=True).distinct()
        return Response(sorted(years, reverse=True))

    @action(detail=False)
    def tags(self, request):
        """Returns all project tags"""
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def related(self, request, slug=None):
        """Returns related projects for a specific project"""
        project = self.get_object()

        # Find related projects based on same category and shared tags
        same_category = Project.objects.filter(category=project.category).exclude(
            id=project.id
        )
        projects_with_shared_tags = (
            Project.objects.filter(tags__in=project.tags.all())
            .exclude(id=project.id)
            .distinct()
        )

        # Combine and prioritize projects with both same category and shared tags
        related = list(
            same_category.filter(
                id__in=projects_with_shared_tags.values_list("id", flat=True)
            )
        )

        # Add remaining projects with shared tags
        for related_project in projects_with_shared_tags:
            if related_project not in related:
                related.append(related_project)

        # Add remaining projects with same category
        for related_project in same_category:
            if related_project not in related:
                related.append(related_project)

        # Limit to 5 related projects
        related = related[:5]

        serializer = ProjectListSerializer(
            related, many=True, context={"request": request}
        )
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint for tags
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "slug"


class ProjectImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for project images
    """

    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer
    filterset_fields = ["project"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context


class PartnerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for partners
    """

    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer


class ProjectPhaseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for project phases
    """

    queryset = ProjectPhase.objects.all()
    serializer_class = ProjectPhaseSerializer
    filterset_fields = ["project", "complete"]


class ProjectOutcomeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for project outcomes
    """

    queryset = ProjectOutcome.objects.all()
    serializer_class = ProjectOutcomeSerializer
    filterset_fields = ["project"]

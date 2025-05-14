from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import TeamMember, Contact, Testimonial, ContactFAQ, MembershipFAQ
from .serializers import (
    TeamMemberSerializer,
    ContactSerializer,
    TestimonialSerializer,
    ContactFAQSerializer,
    MembershipFAQSerializer,
)


class TeamMemberViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing TeamMember instances."""

    queryset = TeamMember.objects.filter(is_active=True)
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["role"]
    search_fields = ["name", "designation", "bio"]
    ordering_fields = ["order", "name"]

    def get_queryset(self):
        """
        This view should return a list of all active team members
        for regular users and all team members for admin users.
        """
        if self.request.user.is_staff:
            return TeamMember.objects.all()
        return TeamMember.objects.filter(is_active=True)


class ContactViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Contact instances."""

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["inquiry_type", "responded"]
    search_fields = ["first_name", "last_name", "email", "message"]
    ordering_fields = ["created_at"]

    def get_permissions(self):
        """
        Allow anyone to create a contact submission,
        but only authenticated users can view or modify them.
        """
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(detail=True, methods=["post"])
    def mark_responded(self, request, pk=None):
        """
        Custom action to mark a contact submission as responded.
        """
        contact = self.get_object()
        contact.responded = True
        contact.response_notes = request.data.get(
            "response_notes", contact.response_notes
        )
        contact.save()
        return Response({"status": "contact marked as responded"})


class TestimonialViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Testimonial instances."""

    queryset = Testimonial.objects.filter(is_featured=True)
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["rating", "is_featured"]
    search_fields = ["name", "designation", "company", "message"]
    ordering_fields = ["created_at", "rating"]

    def get_queryset(self):
        """
        This view should return a list of all featured testimonials
        for regular users and all testimonials for admin users.
        """
        if self.request.user.is_staff:
            return Testimonial.objects.all()
        return Testimonial.objects.filter(is_featured=True)


class ContactFAQViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing ContactFAQ instances."""

    queryset = ContactFAQ.objects.filter(is_published=True)
    serializer_class = ContactFAQSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category", "is_published"]
    search_fields = ["question", "answer", "category"]
    ordering_fields = ["order"]

    def get_queryset(self):
        """
        This view should return a list of all published FAQs
        for regular users and all FAQs for admin users.
        """
        if self.request.user.is_staff:
            return ContactFAQ.objects.all()
        return ContactFAQ.objects.filter(is_published=True)


class MembershipFAQViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing ContactFAQ instances."""

    queryset = MembershipFAQ.objects.filter(is_published=True)
    serializer_class = MembershipFAQSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category", "is_published"]
    search_fields = ["question", "answer", "category"]
    ordering_fields = ["order"]

    def get_queryset(self):
        """
        This view should return a list of all published FAQs
        for regular users and all FAQs for admin users.
        """
        if self.request.user.is_staff:
            return ContactFAQ.objects.all()
        return ContactFAQ.objects.filter(is_published=True)

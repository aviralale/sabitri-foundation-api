from rest_framework import serializers
from .models import TeamMember, Contact, Testimonial, ContactFAQ, MembershipFAQ


class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer for the TeamMember model."""

    class Meta:
        model = TeamMember
        fields = [
            "id",
            "name",
            "designation",
            "role",
            "bio",
            "image",
            "email",
            "linkedin_profile",
            "order",
            "is_active",
            "created_at",
            "updated_at",
        ]


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for the Contact model."""

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Contact
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "phone_number",
            "inquiry_type",
            "message",
            "responded",
            "response_notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["responded", "response_notes"]


class TestimonialSerializer(serializers.ModelSerializer):
    """Serializer for the Testimonial model."""

    class Meta:
        model = Testimonial
        fields = [
            "id",
            "name",
            "designation",
            "company",
            "message",
            "image",
            "is_featured",
            "rating",
            "created_at",
            "updated_at",
        ]


class ContactFAQSerializer(serializers.ModelSerializer):
    """Serializer for the ContactFAQ model."""

    class Meta:
        model = ContactFAQ
        fields = [
            "id",
            "question",
            "answer",
            "category",
            "order",
            "is_published",
            "created_at",
            "updated_at",
        ]


class MembershipFAQSerializer(serializers.ModelSerializer):
    """Serializer for the MembershipFAQ model."""

    class Meta:
        model = MembershipFAQ
        fields = [
            "id",
            "question",
            "answer",
            "category",
            "order",
            "is_published",
            "created_at",
            "updated_at",
        ]

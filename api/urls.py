from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r"team-members", views.TeamMemberViewSet, basename="team-member")
router.register(r"contact", views.ContactViewSet, basename="contact")
router.register(r"testimonials", views.TestimonialViewSet, basename="testimonial")
router.register(r"contact-faqs", views.ContactFAQViewSet, basename="contact-faq")

# The API URLs are determined automatically by the router
urlpatterns = [
    path("", include(router.urls)),
]

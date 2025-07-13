from django.urls import path
from .views import (
    BlogListView,
    BlogDetailView,
    BlogCommentCreateView,
    EventListView,
    EventDetailView,
    ServiceListView,
    BloodInventoryListView,
    VaccineInventoryListView,
    BloodRequestCreateView,
    BloodDonationInterestCreateView,
)

urlpatterns = [
    path("blogs/", BlogListView.as_view(), name="blog-list"),
    path("blogs/<slug:slug>/", BlogDetailView.as_view(), name="blog-detail"),
    path(
        "blogs/<int:blog_id>/comments/",
        BlogCommentCreateView.as_view(),
        name="blog-comment",
    ),
    path("events/", EventListView.as_view(), name="event-list"),
    path("events/<int:id>/", EventDetailView.as_view(), name="event-detail"),
    path("services/", ServiceListView.as_view(), name="service-list"),
    path("blood-inventory/", BloodInventoryListView.as_view(), name="blood-inventory"),
    path(
        "vaccine-inventory/",
        VaccineInventoryListView.as_view(),
        name="vaccine-inventory",
    ),
    path("request-blood/", BloodRequestCreateView.as_view(), name="request-blood"),
    path(
        "donate-interest/",
        BloodDonationInterestCreateView.as_view(),
        name="donate-interest",
    ),
]

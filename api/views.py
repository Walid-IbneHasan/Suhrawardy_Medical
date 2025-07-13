from rest_framework import generics, permissions
from core.models import (
    Blog,
    Event,
    BloodInventory,
    VaccineInventory,
    Service,
    BlogComment,
    BloodRequest,
    BloodDonationInterest,
)
from .serializers import (
    BlogSerializer,
    BlogCommentSerializer,
    EventSerializer,
    BloodInventorySerializer,
    VaccineInventorySerializer,
    ServiceSerializer,
    BloodRequestSerializer,
    BloodDonationInterestSerializer,
)


class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.filter(published=True)
    serializer_class = BlogSerializer


class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.filter(published=True)
    serializer_class = BlogSerializer
    lookup_field = "slug"


class BlogCommentCreateView(generics.CreateAPIView):
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, blog_id=self.kwargs["blog_id"])


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = "id"

class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class BloodInventoryListView(generics.ListAPIView):
    queryset = BloodInventory.objects.all()
    serializer_class = BloodInventorySerializer


class VaccineInventoryListView(generics.ListAPIView):
    queryset = VaccineInventory.objects.all()
    serializer_class = VaccineInventorySerializer


class BloodRequestCreateView(generics.CreateAPIView):
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BloodDonationInterestCreateView(generics.CreateAPIView):
    queryset = BloodDonationInterest.objects.all()
    serializer_class = BloodDonationInterestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

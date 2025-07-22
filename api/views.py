from rest_framework import generics, permissions
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from core.models import (
    About,
    Achievement,
    Blog,
    Event,
    BloodInventory,
    Mission,
    TeamMember,
    VaccineInventory,
    Service,
    Activity,
    TopDonor,
    BlogComment,
    BloodRequest,
    BloodDonationInterest,
    User,
    Image,
)
from .serializers import (
    AboutSerializer,
    AchievementSerializer,
    BlogSerializer,
    BlogCommentSerializer,
    EventSerializer,
    BloodInventorySerializer,
    MissionSerializer,
    TeamMemberSerializer,
    VaccineInventorySerializer,
    ServiceSerializer,
    ActivitySerializer,
    TopDonorSerializer,
    BloodRequestSerializer,
    BloodDonationInterestSerializer,
    UserSerializer,
    ImageSerializer,
)


# Public Views
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


class AboutListView(generics.ListAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer


class AchievementListView(generics.ListAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer


class TeamMemberListView(generics.ListAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer


class MissionListView(generics.ListAPIView):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer


# Admin Views
class AdminBlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class AdminBlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "slug"
    parser_classes = [MultiPartParser, FormParser]


class AdminEventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class AdminEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"
    parser_classes = [MultiPartParser, FormParser]


class AdminServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminUser]


class AdminServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"


class AdminActivityListCreateView(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAdminUser]


class AdminActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"


class AdminTopDonorListCreateView(generics.ListCreateAPIView):
    queryset = TopDonor.objects.all()
    serializer_class = TopDonorSerializer
    permission_classes = [IsAdminUser]


class AdminTopDonorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TopDonor.objects.all()
    serializer_class = TopDonorSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"


class AdminBloodInventoryListCreateView(generics.ListCreateAPIView):
    queryset = BloodInventory.objects.all()
    serializer_class = BloodInventorySerializer
    permission_classes = [IsAdminUser]


class AdminBloodInventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BloodInventory.objects.all()
    serializer_class = BloodInventorySerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"


class AdminVaccineInventoryListCreateView(generics.ListCreateAPIView):
    queryset = VaccineInventory.objects.all()
    serializer_class = VaccineInventorySerializer
    permission_classes = [IsAdminUser]


class AdminVaccineInventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VaccineInventory.objects.all()
    serializer_class = VaccineInventorySerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"


class AdminBlogCommentListCreateView(generics.ListCreateAPIView):
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AdminBlogCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"


class AdminBloodRequestListCreateView(generics.ListCreateAPIView):
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AdminBloodRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"


class AdminBloodDonationInterestListCreateView(generics.ListCreateAPIView):
    queryset = BloodDonationInterest.objects.all()
    serializer_class = BloodDonationInterestSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AdminBloodDonationInterestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BloodDonationInterest.objects.all()
    serializer_class = BloodDonationInterestSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"


class AdminUserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"


class AdminImageListCreateView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAdminUser]


class AdminImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"


class AdminAboutListCreateView(generics.ListCreateAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class AdminAboutDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"
    parser_classes = [MultiPartParser, FormParser]


class AdminAchievementListCreateView(generics.ListCreateAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAdminUser]


class AdminAchievementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"


class AdminTeamMemberListCreateView(generics.ListCreateAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class AdminTeamMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"
    parser_classes = [MultiPartParser, FormParser]


class AdminMissionListCreateView(generics.ListCreateAPIView):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [IsAdminUser]


class AdminMissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"

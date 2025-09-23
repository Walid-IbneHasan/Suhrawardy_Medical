from rest_framework import generics, permissions
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.utils import timezone

from core.models import (
    About,
    Achievement,
    Blog,
    BloodDonor,
    Event,
    BloodInventory,
    HomeAbout,
    HomeAboutAchievement,
    Mission,
    MissionStatement,
    PDFDocument,
    TeamMember,
    VaccineInventory,
    Service,
    Activity,
    TopDonor,
    BlogComment,
    BloodRequest,
    BloodDonationInterest,
    BloodDonation,
    User,
    Image,
)
from .serializers import (
    AboutSerializer,
    AchievementSerializer,
    BlogSerializer,
    BlogCommentSerializer,
    BloodDonorSerializer,
    EventSerializer,
    BloodInventorySerializer,
    HomeAboutAchievementSerializer,
    HomeAboutSerializer,
    MissionSerializer,
    MissionStatementSerializer,
    PDFDocumentSerializer,
    TeamMemberSerializer,
    VaccineInventorySerializer,
    ServiceSerializer,
    ActivitySerializer,
    TopDonorSerializer,
    BloodRequestSerializer,
    BloodDonationInterestSerializer,
    BloodDonationSerializer,
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


def _auto_expire_events():
    """Deactivate any events whose date has already passed."""
    Event.objects.filter(is_active=True, date__lt=timezone.now()).update(
        is_active=False
    )


class UpcomingEventListView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        _auto_expire_events()
        # Only active, future or today — order soonest first
        return Event.objects.filter(is_active=True).order_by("date")


class PastEventListView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        _auto_expire_events()
        # Everything deactivated — newest past events first
        return Event.objects.filter(is_active=False).order_by("-date")


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


class MyBloodRequestListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BloodRequestSerializer

    def get_queryset(self):
        return BloodRequest.objects.filter(user=self.request.user).order_by("-id")


class MyDonationInterestListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BloodDonationInterestSerializer

    def get_queryset(self):
        return BloodDonationInterest.objects.filter(user=self.request.user).order_by(
            "-id"
        )


class MyDonationListCreateView(generics.ListCreateAPIView):
    """
    Normal users:
      - GET: see only their donations
      - POST: log a new donation (enforces 3-month rule)
    Admins can still use admin endpoints for full visibility.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BloodDonationSerializer

    def get_queryset(self):
        return BloodDonation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()  # serializer sets user from request + updates last_donation_date


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


class HomeAboutListView(generics.ListAPIView):
    queryset = HomeAbout.objects.all()
    serializer_class = HomeAboutSerializer


class MissionStatementListView(generics.ListAPIView):
    queryset = MissionStatement.objects.all()
    serializer_class = MissionStatementSerializer


class HomeAboutAchievementListView(generics.ListAPIView):
    queryset = HomeAboutAchievement.objects.all()
    serializer_class = HomeAboutAchievementSerializer


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


class AdminDonationListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = BloodDonationSerializer
    queryset = (
        BloodDonation.objects.select_related("user")
        .all()
        .order_by("-donation_date", "-id")
    )


class AdminDonationDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = BloodDonationSerializer
    queryset = BloodDonation.objects.select_related("user").all()
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


class AdminBloodDonorListCreateView(generics.ListCreateAPIView):
    queryset = BloodDonor.objects.all()
    serializer_class = BloodDonorSerializer
    permission_classes = [IsAdminUser]


class AdminBloodDonorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BloodDonor.objects.all()
    serializer_class = BloodDonorSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"


class AdminPDFDocumentListCreateView(generics.ListCreateAPIView):
    queryset = PDFDocument.objects.all()
    serializer_class = PDFDocumentSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class AdminPDFDocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PDFDocument.objects.all()
    serializer_class = PDFDocumentSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"
    parser_classes = [MultiPartParser, FormParser]


class ConvertDueInterestsView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        today = timezone.now().date()
        due = BloodDonationInterest.objects.select_related("user").filter(
            available_date__lte=today, donation__isnull=True
        )

        created = 0
        with transaction.atomic():
            for interest in due:
                donation = BloodDonation.objects.create(
                    user=interest.user,
                    blood_group=interest.blood_group or interest.user.blood_group or "",
                    donation_date=interest.available_date,
                    contact_info=interest.contact_info,
                    notes=f"Auto-converted from donation interest on {interest.available_date}",
                )
                # link back to the interest & update user's last_donation_date
                interest.donation = donation
                interest.save(update_fields=["donation"])

                if (
                    not interest.user.last_donation_date
                    or donation.donation_date > interest.user.last_donation_date
                ):
                    interest.user.last_donation_date = donation.donation_date
                    interest.user.save(update_fields=["last_donation_date"])

                created += 1

        return Response({"converted": created})


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


class AdminHomeAboutListCreateView(generics.ListCreateAPIView):
    queryset = HomeAbout.objects.all()
    serializer_class = HomeAboutSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminHomeAboutDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HomeAbout.objects.all()
    serializer_class = HomeAboutSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"


class AdminMissionStatementListCreateView(generics.ListCreateAPIView):
    queryset = MissionStatement.objects.all()
    serializer_class = MissionStatementSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminMissionStatementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MissionStatement.objects.all()
    serializer_class = MissionStatementSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"


class AdminHomeAboutAchievementListCreateView(generics.ListCreateAPIView):
    queryset = HomeAboutAchievement.objects.all()
    serializer_class = HomeAboutAchievementSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminHomeAboutAchievementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HomeAboutAchievement.objects.all()
    serializer_class = HomeAboutAchievementSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"

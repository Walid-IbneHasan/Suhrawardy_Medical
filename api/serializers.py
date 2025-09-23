from datetime import timedelta
from rest_framework import serializers
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
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "name",
            "phone",
            "blood_group",
            "address",
            "last_donation_date",
            "is_staff",
            "is_superuser",
            "date_joined",
            "password",
            "confirm_password",
        ]
        read_only_fields = ["date_joined", " name"]

    def get_name(self, obj):
        """
        Combines first and last name into a single 'name' field.
        Falls back to email if names are not set.
        """
        first_name = obj.first_name.strip() if obj.first_name else ""
        last_name = obj.last_name.strip() if obj.last_name else ""

        full_name = f"{first_name} {last_name}".strip()

        return full_name if full_name else obj.email

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        if data.get("is_superuser") and not data.get("is_staff"):
            data["is_staff"] = True  # Ensure is_staff is True when is_superuser is True
        return data

    def validate_last_donation_date(self, value):
        if value and value > timezone.now().date():
            raise serializers.ValidationError(
                "Last donation date cannot be in the future."
            )
        return value

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        user = User.objects.create_user(
            email=validated_data["email"],
            password=password,
            username=validated_data.get("username"),
            is_staff=validated_data.get("is_staff", False),
            is_superuser=validated_data.get("is_superuser", False),
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        validated_data.pop("confirm_password", None)
        if validated_data.get("is_superuser") and not validated_data.get("is_staff"):
            validated_data["is_staff"] = (
                True  # Ensure is_staff is True when is_superuser is True
            )
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image", "blog", "event", "team_member", "about"]
        read_only_fields = ["blog", "event", "team_member", "about"]


class BlogSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    image_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
        allow_empty=True,
    )

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",  # keep exposed, but read-only
            "content",
            "created_at",
            "published",
            "images",
            "image_files",
        ]
        read_only_fields = ["created_at", "slug", "images"]

    def create(self, validated_data):
        image_files = validated_data.pop("image_files", [])
        blog = Blog.objects.create(**validated_data)  # slug auto-generates
        for image_file in image_files:
            Image.objects.create(blog=blog, image=image_file)
        return blog

    def update(self, instance, validated_data):
        image_files = validated_data.pop("image_files", None)
        # don’t allow slug changes from payload
        validated_data.pop("slug", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if image_files is not None:
            Image.objects.filter(blog=instance).delete()
            for image_file in image_files:
                Image.objects.create(blog=instance, image=image_file)
        return instance


class BlogCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = BlogComment
        fields = ["id", "user", "blog", "comment", "created_at"]
        read_only_fields = ["user", "created_at"]


class EventSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    image_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
        allow_empty=True,
    )
    description = serializers.CharField(allow_blank=True)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "location",
            "date",
            "is_active",
            "images",
            "image_files",
        ]

    def create(self, validated_data):
        image_files = validated_data.pop("image_files", [])
        event = Event.objects.create(**validated_data)
        for image_file in image_files:
            Image.objects.create(event=event, image=image_file)
        return event

    def update(self, instance, validated_data):
        image_files = validated_data.pop("image_files", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if image_files is not None:
            Image.objects.filter(event=instance).delete()
            for image_file in image_files:
                Image.objects.create(event=instance, image=image_file)
        return instance


class BloodInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodInventory
        fields = ["id", "group", "available"]


class VaccineInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineInventory
        fields = ["id", "type", "available"]


class ServiceSerializer(serializers.ModelSerializer):
    description = serializers.CharField(allow_blank=True)

    class Meta:
        model = Service
        fields = ["id", "name", "description"]


class ActivitySerializer(serializers.ModelSerializer):
    description = serializers.CharField(allow_blank=True)

    class Meta:
        model = Activity
        fields = ["id", "title", "description", "date"]


class TopDonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopDonor
        fields = ["id", "name", "blood_group", "donations"]


class BloodRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = BloodRequest
        fields = [
            "id",
            "user",
            "blood_group",
            "location",
            "contact",
            "reason",
            "date_required",
            "collection_location",
        ]
        read_only_fields = ["user"]


class BloodDonationInterestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    donation_id = serializers.IntegerField(source="donation.id", read_only=True)

    class Meta:
        model = BloodDonationInterest
        fields = [
            "id",
            "user",
            "blood_group",
            "available_date",
            "contact_info",
            "donation_id",
        ]
        read_only_fields = ["user", "donation_id"]

    def validate(self, data):
        """
        Enforce the 3-month rule using only confirmed donations (BloodDonation),
        and compare against the chosen available_date.
        """
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return data

        available_date = data.get("available_date")
        if not available_date:
            return data

        # Look up the user's latest confirmed donation
        latest = (
            BloodDonation.objects.filter(user=user).order_by("-donation_date").first()
        )

        if latest and available_date < (latest.donation_date + timedelta(days=90)):
            raise serializers.ValidationError(
                {
                    "available_date": (
                        f"You can donate only after 3 months from your last donation on {latest.donation_date}."
                    )
                }
            )

        # Prefer the user's blood group if set and request didn't specify
        if user.blood_group and not data.get("blood_group"):
            data["blood_group"] = user.blood_group

        return data


class BloodDonationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = BloodDonation
        fields = [
            "id",
            "user",
            "blood_group",
            "donation_date",
            "contact_info",
            "notes",
            "created_at",
        ]
        read_only_fields = ["user", "created_at"]

    def validate_donation_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Donation date cannot be in the future.")
        return value

    def validate(self, data):
        """
        Enforce 90-day spacing by checking nearest existing donations before/after
        the submitted donation_date for this user.
        """
        user = self.context["request"].user if "request" in self.context else None
        if not user or not user.is_authenticated:
            return data

        donation_date = data.get("donation_date")
        if not donation_date:
            return data

        qs = BloodDonation.objects.filter(user=user)

        prev_donation = (
            qs.filter(donation_date__lt=donation_date)
            .order_by("-donation_date")
            .first()
        )
        if prev_donation and donation_date < (
            prev_donation.donation_date + timedelta(days=90)
        ):
            raise serializers.ValidationError(
                {
                    "donation_date": f"You must wait 3 months after your previous donation on {prev_donation.donation_date}."
                }
            )

        next_donation = (
            qs.filter(donation_date__gt=donation_date).order_by("donation_date").first()
        )
        if next_donation and next_donation.donation_date < (
            donation_date + timedelta(days=90)
        ):
            raise serializers.ValidationError(
                {
                    "donation_date": f"This date conflicts with an existing donation on {next_donation.donation_date} (less than 3 months apart)."
                }
            )

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        donation = BloodDonation.objects.create(user=user, **validated_data)
        # Keep profile convenience field in sync with the latest donation
        if (
            not user.last_donation_date
            or donation.donation_date > user.last_donation_date
        ):
            user.last_donation_date = donation.donation_date
            user.save(update_fields=["last_donation_date"])
        return donation

class BloodDonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodDonor
        fields = [
            'id',
            'name',
            'batch',
            'blood_group',
            'phone',
            'last_donated_date',
            'gender',
            'created_at',
        ]
        read_only_fields = ['created_at']

class PDFDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFDocument
        fields = ['id', 'file', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class AboutSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = About
        fields = [
            "id",
            "title",
            "description",
            "years_experience",
            "patients_served",
            "satisfaction_rate",
            "image",
            "images",
        ]

    def create(self, validated_data):
        image = validated_data.pop("image", None)
        about = About.objects.create(**validated_data)
        if image:
            Image.objects.create(about=about, image=image)
        return about

    def update(self, instance, validated_data):
        image = validated_data.pop("image", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if image:
            Image.objects.filter(about=instance).delete()
            Image.objects.create(about=instance, image=image)
        return instance


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ["id", "title", "description", "icon"]


class TeamMemberSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = TeamMember
        fields = ["id", "name", "role", "specialty", "image", "images"]

    def create(self, validated_data):
        image = validated_data.pop("image", None)
        team_member = TeamMember.objects.create(**validated_data)
        if image:
            Image.objects.create(team_member=team_member, image=image)
        return team_member

    def update(self, instance, validated_data):
        image = validated_data.pop("image", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if image:
            Image.objects.filter(team_member=instance).delete()
            Image.objects.create(team_member=instance, image=image)
        return instance


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ["id", "title", "description", "phone", "email", "address"]


class HomeAboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeAbout
        fields = [
            "id",
            "title",
            "description",
            "years_experience",
            "patients_served",
            "satisfaction_rate",
        ]


class MissionStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionStatement
        fields = ["id", "statement"]


class HomeAboutAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeAboutAchievement
        fields = ["id", "title", "description", "icon"]

from rest_framework import serializers
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "is_staff", "is_superuser", "date_joined"]
        read_only_fields = ["date_joined"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image", "blog", "event", "team_member", "about"]
        read_only_fields = ["blog", "event", "team_member", "about"]


class BlogSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ["id", "title", "slug", "content", "created_at", "published", "images"]
        read_only_fields = ["created_at"]


class BlogCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = BlogComment
        fields = ["id", "user", "blog", "comment", "created_at"]
        read_only_fields = ["user", "created_at"]


class EventSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    description = serializers.CharField(allow_blank=True)

    class Meta:
        model = Event
        fields = ["id", "title", "description", "location", "date", "images"]


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
        fields = ["id", "user", "blood_group", "location", "contact", "date_required"]
        read_only_fields = ["user"]


class BloodDonationInterestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = BloodDonationInterest
        fields = ["id", "user", "blood_group", "available_date", "contact_info"]
        read_only_fields = ["user"]


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

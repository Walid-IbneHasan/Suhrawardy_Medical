from rest_framework import serializers
from core.models import (
    Blog,
    Event,
    BloodInventory,
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
        fields = ["id", "image", "blog", "event"]
        read_only_fields = ["blog", "event"]


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

from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    User,
    Image,
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
)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fields = ["image"]


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ["email", "is_staff"]
    search_fields = ["email"]


@admin.register(Blog)
class BlogAdmin(ModelAdmin):
    list_display = ["title", "slug", "created_at", "published"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ["published"]
    list_editable = ["published"]
    inlines = [ImageInline]


@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = ["title", "date", "location"]
    search_fields = ["title", "description"]
    list_filter = ["date"]
    inlines = [ImageInline]


@admin.register(BloodInventory)
class BloodInventoryAdmin(ModelAdmin):
    list_display = ["group", "available"]
    list_filter = ["group", "available"]
    list_editable = ["available"]


@admin.register(VaccineInventory)
class VaccineInventoryAdmin(ModelAdmin):
    list_display = ["type", "available"]
    list_filter = ["type", "available"]
    list_editable = ["available"]


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ["name"]
    search_fields = ["name", "description"]


@admin.register(Activity)
class ActivityAdmin(ModelAdmin):
    list_display = ["title", "date"]
    search_fields = ["title", "description"]
    list_filter = ["date"]


@admin.register(TopDonor)
class TopDonorAdmin(ModelAdmin):
    list_display = ["name", "blood_group", "donations"]
    search_fields = ["name"]


@admin.register(BlogComment)
class BlogCommentAdmin(ModelAdmin):
    list_display = ["user", "blog", "created_at"]
    search_fields = ["comment"]
    list_filter = ["created_at"]


@admin.register(BloodRequest)
class BloodRequestAdmin(ModelAdmin):
    list_display = ["user", "blood_group", "date_required"]
    search_fields = ["user__email", "blood_group"]
    list_filter = ["blood_group", "date_required"]


@admin.register(BloodDonationInterest)
class BloodDonationInterestAdmin(ModelAdmin):
    list_display = ["user", "blood_group", "available_date"]
    search_fields = ["user__email", "blood_group"]
    list_filter = ["blood_group", "available_date"]

# core/admin.py

from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    About,
    Achievement,
    Mission,
    PDFDocument,
    TeamMember,
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
    BloodDonation,
    BloodDonor,
)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fields = ["image"]


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ["email", "first_name", "last_name", "blood_group", "is_staff"]
    search_fields = ["email", "first_name", "last_name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone",
                    "blood_group",
                    "address",
                    "last_donation_date",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


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
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "blood_group",
        "location",
        "collection_location",
        "reason",
        "contact",
        "date_required",
    )
    list_filter = ("blood_group", "date_required")
    search_fields = (
        "user__email",
        "blood_group",
        "location",
        "collection_location",
        "reason",
    )


@admin.register(BloodDonationInterest)
class BloodDonationInterestAdmin(ModelAdmin):
    list_display = ["user", "blood_group", "available_date"]
    search_fields = ["user__email", "blood_group"]
    list_filter = ["blood_group", "available_date"]


@admin.register(BloodDonation)
class BloodDonationAdmin(ModelAdmin):
    list_display = ["user", "blood_group", "donation_date", "contact_info"]
    search_fields = ["user__email", "blood_group", "contact_info"]
    list_filter = ["blood_group", "donation_date", "created_at"]
    date_hierarchy = "donation_date"
    readonly_fields = ["created_at"]
    fieldsets = (
        (None, {"fields": ("user", "blood_group", "donation_date")}),
        (
            "Additional Information",
            {"fields": ("contact_info", "notes"), "classes": ("collapse",)},
        ),
        ("Timestamps", {"fields": ("created_at",), "classes": ("collapse",)}),
    )


@admin.register(About)
class AboutAdmin(ModelAdmin):
    list_display = ["title", "years_experience", "patients_served", "satisfaction_rate"]
    search_fields = ["title", "description"]
    fields = [
        "title",
        "description",
        "years_experience",
        "patients_served",
        "satisfaction_rate",
        "image",
    ]


@admin.register(Achievement)
class AchievementAdmin(ModelAdmin):
    list_display = ["title", "icon"]
    search_fields = ["title", "description"]
    fields = ["title", "description", "icon"]


@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = ["name", "role", "specialty"]
    search_fields = ["name", "role", "specialty"]
    inlines = [ImageInline]


@admin.register(Mission)
class MissionAdmin(ModelAdmin):
    list_display = ["title", "phone", "email"]
    search_fields = ["title", "description", "phone", "email", "address"]
    fields = ["title", "description", "phone", "email", "address"]


@admin.register(BloodDonor)
class BloodDonorAdmin(ModelAdmin):
    list_display = [
        "name",
        "batch",
        "blood_group",
        "phone",
        "gender",
        "last_donated_date",
        "created_at",
    ]
    search_fields = ["name", "batch", "blood_group", "phone"]
    list_filter = ["blood_group", "gender", "last_donated_date", "created_at"]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at"]
    fieldsets = (
        (None, {"fields": ("name", "batch", "blood_group", "phone", "gender")}),
        ("Donation Information", {"fields": ("last_donated_date", "document")}),
        ("Timestamps", {"fields": ("created_at",), "classes": ("collapse",)}),
    )
    list_editable = ["batch"]
    ordering = ["-created_at"]


@admin.register(PDFDocument)
class PDFDocumentAdmin(ModelAdmin):
    list_display = ["description", "file", "created_at", "updated_at"]
    search_fields = ["description", "file"]
    list_filter = ["created_at", "updated_at"]

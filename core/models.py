from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.text import slugify


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("username", None)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class BloodInventory(models.Model):
    BLOOD_GROUPS = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]
    group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.group} - {'Available' if self.available else 'Not Available'}"


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    blood_group = models.CharField(
        max_length=3, choices=BloodInventory.BLOOD_GROUPS, blank=True
    )
    address = models.TextField(blank=True)
    last_donation_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.email


class Image(models.Model):
    image = models.ImageField(upload_to="images/")
    blog = models.ForeignKey(
        "Blog", on_delete=models.CASCADE, related_name="images", null=True, blank=True
    )
    event = models.ForeignKey(
        "Event", on_delete=models.CASCADE, related_name="images", null=True, blank=True
    )
    team_member = models.ForeignKey(
        "TeamMember",
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True,
    )
    about = models.ForeignKey(
        "About", on_delete=models.CASCADE, null=True, blank=True, related_name="images"
    )

    def __str__(self):
        return f"Image for {self.blog or self.event}"


class Blog(models.Model):
    title = models.CharField(max_length=255)
    # allow blank so serializers don’t require it; still unique in DB
    slug = models.SlugField(unique=True, blank=True, max_length=80)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def _generate_unique_slug(self):
        max_len = self._meta.get_field("slug").max_length or 80
        base = slugify(self.title) or "post"
        base = base[:max_len]
        slug = base
        i = 2
        # ensure uniqueness; trim base if suffix would exceed max_len
        while Blog.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            suffix = f"-{i}"
            slug = f"{base[: max_len - len(suffix)]}{suffix}"
            i += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateTimeField()

    def __str__(self):
        return self.title


class VaccineInventory(models.Model):
    type = models.CharField(max_length=100)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.type} - {'Available' if self.available else 'Not Available'}"


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Activity(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.title


class TopDonor(models.Model):
    name = models.CharField(max_length=255)
    blood_group = models.CharField(max_length=3)
    donations = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class BlogComment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.blog}"


class BloodRequest(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=BloodInventory.BLOOD_GROUPS)
    location = models.CharField(max_length=255)
    contact = models.CharField(max_length=50)
    date_required = models.DateField()

    def __str__(self):
        return f"Request by {self.user} for {self.blood_group}"


class BloodDonationInterest(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=BloodInventory.BLOOD_GROUPS)
    available_date = models.DateField()
    contact_info = models.CharField(max_length=50)

    donation = models.OneToOneField(
        "BloodDonation",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="source_interest",
    )

    def __str__(self):
        return f"Interest by {self.user} for {self.blood_group}"


# core/models.py


class BloodDonation(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=BloodInventory.BLOOD_GROUPS)
    donation_date = models.DateField()
    contact_info = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-donation_date", "-id"]

    def __str__(self):
        return f"Donation by {self.user.email} on {self.donation_date} ({self.blood_group})"


class About(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    years_experience = models.PositiveIntegerField()
    patients_served = models.CharField(max_length=50)
    satisfaction_rate = models.CharField(max_length=50)
    image = models.ImageField(upload_to="about/", blank=True, null=True)

    def __str__(self):
        return self.title


class Achievement(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=50)  # Store icon name (e.g., "Award", "Users")

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Mission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.title


class HomeAbout(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    years_experience = models.PositiveIntegerField(default=0)
    patients_served = models.CharField(max_length=50)
    satisfaction_rate = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Home About"
        verbose_name_plural = "Home About Sections"

    def __str__(self):
        return self.title


class MissionStatement(models.Model):
    statement = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mission Statement"
        verbose_name_plural = "Mission Statements"

    def __str__(self):
        return self.statement[:50]


class HomeAboutAchievement(models.Model):
    ICON_CHOICES = [
        ("Award", "Award"),
        ("Users", "Users"),
        ("Heart", "Heart"),
        ("Activity", "Activity"),
        ("Shield", "Shield"),
        ("Star", "Star"),
        ("CheckCircle", "CheckCircle"),
        ("Trophy", "Trophy"),
        ("UserCheck", "UserCheck"),
        ("HeartPulse", "HeartPulse"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=50, choices=ICON_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Home About Achievement"
        verbose_name_plural = "Home About Achievements"

    def __str__(self):
        return self.title

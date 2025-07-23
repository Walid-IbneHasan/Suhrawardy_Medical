from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


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


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

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
    slug = models.SlugField(unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateTimeField()

    def __str__(self):
        return self.title


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

    def __str__(self):
        return f"Interest by {self.user} for {self.blood_group}"


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

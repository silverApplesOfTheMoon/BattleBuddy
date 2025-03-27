from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Creates and saves a regular user with the given email and password.
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True) # Set user as active by default
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Creates and saves a superuser with the given email and password.
        extra_fields.setdefault("is_staff", True) # Grant admin privileges
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractUser):
    username = None  # Remove username field
    email = models.EmailField(unique=True)  # Use email as the unique identifier
    full_name = models.CharField(max_length=255)
    
    student_type = models.CharField(
        max_length=50,
        choices=[
            ("Future", "Future Student"),
            ("Current", "Current Student"),
            ("Alumni", "Alumni Student"),
            ("None", "Neither"),
        ]
    )

    objects = CustomUserManager() # Use custom user manager

    USERNAME_FIELD = "email" # Use email instead of username for authentication
    REQUIRED_FIELDS = ["full_name", "student_type"] # Required on user creation

    def __str__(self):
        return self.email

# Cohort Quiz Model
class CohortQuiz(models.Model):
    # Stores responses to cohort quiz questions
    q1 = models.CharField(max_length=50)
    q2 = models.CharField(max_length=50)
    q3 = models.CharField(max_length=50)
    q4 = models.CharField(max_length=50)
    q5 = models.CharField(max_length=50)
    q6 = models.CharField(max_length=50)

    def __str__(self):
        return f"Cohort Quiz - {self.id}"

# Edit User Model
class EditUser(models.Model):
    # Link to the user this edit entry applies to
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Editable email field - must be unique
    email = models.EmailField(unique=True)
    # Editable full name of the user
    full_name = models.CharField(max_length=255)
    # Editable student type with predefined choices
    student_type = models.CharField(
        max_length=50,
        choices=[
            ('Future', 'Future Student'),
            ('Current', 'Current Student'),
            ('Alumni', 'Alumni Student'),
            ('None', 'Neither'),
        ]
    )
    # Optional new password field (left blank if not being changed)
    new_password = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.email

# Error Model
class ErrorLog(models.Model):
    request_id = models.CharField(max_length=100, blank=True, null=True)

    # Method to determine if a request ID exists
    def show_request_id(self):
        return bool(self.request_id)

# Forgot Password Model
class ForgotPassword(models.Model):
    # Email of user requesting password reset
    email = models.EmailField()

    def __str__(self):
        return self.email

# Login Model
class Login(models.Model):
    # Email used to login
    email = models.EmailField()
    # User's password
    password = models.CharField(max_length=255)
    # Checkbox for "Remember Me" functionality
    remember_me = models.BooleanField(default=False)

    def __str__(self):
        return self.email

# Register Model
class Register(models.Model):
    # User's full name
    full_name = models.CharField(max_length=255)
    # Unique email for the new user
    email = models.EmailField(unique=True)
    # Initial password
    password = models.CharField(max_length=255)
    # Confirmation password to verify user input
    confirm_password = models.CharField(max_length=255)
    # Student type selected during registration
    student_type = models.CharField(
        max_length=50,
        choices=[
            ('Future', 'Future Student'),
            ('Current', 'Current Student'),
            ('Alumni', 'Alumni Student'),
            ('None', 'Neither'),
        ]
    )

    def __str__(self):
        return self.email

# Reset Password Model
class ResetPassword(models.Model):
    # Token used to verify identity during password reset
    token = models.CharField(max_length=255)
    # Email address of the user resetting the password
    email = models.EmailField()
    # New password to be set
    password = models.CharField(max_length=255)
    # Confirmation of the new password
    confirm_password = models.CharField(max_length=255)

    def __str__(self):
        return f"Reset Password for {self.email}"

# User Info Model
class UserInfo(models.Model):
    # Link to the main user
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Display name of the user
    full_name = models.CharField(max_length=255)
    # Student type metadata
    student_type = models.CharField(
        max_length=50,
        choices=[
            ('Future', 'Future Student'),
            ('Current', 'Current Student'),
            ('Alumni', 'Alumni Student'),
            ('None', 'Neither'),
        ]
    )

    def __str__(self):
        return self.user.email


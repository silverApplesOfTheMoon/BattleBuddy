# Import Django's built-in abstract user model and user manager to create custom user functionality
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission

# Import Django's database models module to define data models
from django.db import models

"""
This file defines all the database models used in the Washington Vets2Tech web platform.
It includes models for:
- Custom User Management (authentication using email)
- Cohort visibility control
- Cohort quiz data storage
- User information management
- Login & Registration data tracking
- Password reset workflow
"""

# Custom User Manager

class CustomUserManager(BaseUserManager):
    """
    Custom manager to handle creation of regular users and superusers.
    This manager uses 'email' instead of the default 'username' field for authentication.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a regular user with the provided email and password.
        :param email: User's email (used as username)
        :param password: User's password
        :param extra_fields: Any additional fields
        """
        # Ensure email is provided, otherwise raise error
        if not email:
            raise ValueError("The Email field must be set")

        # Normalize email format
        email = self.normalize_email(email)
        # Set user account as active by default
        extra_fields.setdefault("is_active", True)
        
        # Create user instance with provided email and extra fields
        user = self.model(email=email, **extra_fields)
        # Hash and set the password securely
        user.set_password(password)
        # Save user to database using default database
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with administrative privileges.
        :param email: Superuser's email
        :param password: Superuser's password
        :param extra_fields: Any additional fields
        """
        # Grant admin privileges
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Call create_user to create and save superuser
        return self.create_user(email, password, **extra_fields)

# Custom User Model

class CustomUser(AbstractUser):
    """
    Custom user model that replaces Django's default User model.
    Uses 'email' instead of 'username' as the unique identifier.
    Includes additional fields like 'full_name' and 'student_type'.
    """
    # Disable username field (not used)
    username = None
    # Email field set to unique identifier
    email = models.EmailField(unique=True)
    # Full name of the user
    full_name = models.CharField(max_length=255)
    
    # Student type to categorize users
    student_type = models.CharField(
        max_length=50,
        choices=[
            ("Future", "Future Student"),
            ("Current", "Current Student"),
            ("Alumni", "Alumni Student"),
            ("None", "Neither"),
        ]
    )

    # Assign custom user manager to handle creation
    objects = CustomUserManager()

    # Set email as primary login field
    USERNAME_FIELD = "email"
    # Required fields when creating a user
    REQUIRED_FIELDS = ["full_name", "student_type"]

    def __str__(self):
        """
        Return email as string representation of the user
        """
        return self.email

# Cohort Visibility Model

class CohortVisibility(models.Model):
    """
    Model to control global visibility (enable/disable) of specific cohorts.
    Enables admin to show or hide cohort options on the website.
    """
    # Unique name of the cohort
    name = models.CharField(max_length=100, unique=True)
    # Boolean flag to enable/disable visibility
    enabled = models.BooleanField(default=True)

    def __str__(self):
        """
        Return cohort name and visibility status as string
        """
        return f"{self.name} - {'Enabled' if self.enabled else 'Disabled'}"

# Cohort Quiz Model

class CohortQuiz(models.Model):
    """
    Model to store user responses to the cohort quiz.
    Contains one field per question.
    """
    # Store answers for 6 quiz questions
    q1 = models.CharField(max_length=50)
    q2 = models.CharField(max_length=50)
    q3 = models.CharField(max_length=50)
    q4 = models.CharField(max_length=50)
    q5 = models.CharField(max_length=50)
    q6 = models.CharField(max_length=50)

    def __str__(self):
        """
        Return string identifying quiz by its ID
        """
        return f"Cohort Quiz - {self.id}"

# Edit User Model

class EditUser(models.Model):
    """
    Model to temporarily store user data for editing purposes.
    Mainly used in Admin Panel when admin modifies user details.
    """
    # Link to the user being edited
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Editable email (must be unique)
    email = models.EmailField(unique=True)
    # Editable full name
    full_name = models.CharField(max_length=255)
    # Editable student type (drop-down)
    student_type = models.CharField(
        max_length=50,
        choices=[
            ('Future', 'Future Student'),
            ('Current', 'Current Student'),
            ('Alumni', 'Alumni Student'),
            ('None', 'Neither'),
        ]
    )
    # Optional field for setting a new password
    new_password = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        """
        Return email as string representation
        """
        return self.email

# Error Log Model

class ErrorLog(models.Model):
    """
    Model to log error request IDs during system errors.
    Helps in debugging and troubleshooting.
    """
    # Optional request ID of the error
    request_id = models.CharField(max_length=100, blank=True, null=True)

    def show_request_id(self):
        """
        Returns True if request ID exists, else False.
        """
        return bool(self.request_id)

# Forgot Password Model

class ForgotPassword(models.Model):
    """
    Stores email addresses of users who requested password reset.
    Used to verify identity and allow password recovery.
    """
    # User email requesting password reset
    email = models.EmailField()

    def __str__(self):
        """
        Return email as string representation
        """
        return self.email

# Login Model

class Login(models.Model):
    """
    Stores login data submitted by users.
    Includes email, password, and 'Remember Me' option.
    """
    # Email used to login
    email = models.EmailField()
    # Password used
    password = models.CharField(max_length=255)
    # 'Remember Me' checkbox status
    remember_me = models.BooleanField(default=False)

    def __str__(self):
        """
        Return email as string
        """
        return self.email

# Register Model

class Register(models.Model):
    """
    Stores user registration data temporarily before account creation.
    """
    # Full name of the user
    full_name = models.CharField(max_length=255)
    # Email used for registration (must be unique)
    email = models.EmailField(unique=True)
    # Password chosen during registration
    password = models.CharField(max_length=255)
    # Confirmation password field
    confirm_password = models.CharField(max_length=255)
    # Student type chosen by user
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
        """
        Return email as string
        """
        return self.email

# Reset Password Model

class ResetPassword(models.Model):
    """
    Model to temporarily store password reset data.
    Contains email, new password, and confirmation password.
    """
    # Token to verify identity
    token = models.CharField(max_length=255)
    # Email of user resetting password
    email = models.EmailField()
    # New password to be set
    password = models.CharField(max_length=255)
    # Confirmation of new password
    confirm_password = models.CharField(max_length=255)

    def __str__(self):
        """
        Return reset password identifier as string
        """
        return f"Reset Password for {self.email}"

# ----------------------- User Info Model -----------------------

class UserInfo(models.Model):
    """
    Model to store additional user information.
    Mainly used for display purposes and metadata.
    """
    # Link to main user model
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Full name of the user
    full_name = models.CharField(max_length=255)
    # Student type of the user
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
        """
        Return user's email as string
        """
        return self.user.email

# Import Django's forms module which provides classes for handling form rendering and validation
from django import forms

# Import Python's random module to shuffle challenge quiz options
import random

# Import built-in Django authentication form classes
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Import CustomUser model from models.py to bind forms to the user model
from .models import CustomUser

# Import translation utility to enable multi-language support
from django.utils.translation import gettext_lazy as _

"""
This file defines all form classes used in the Vets2Tech project.
These forms handle:
- User authentication (login)
- User registration
- Password reset
- Editing user profiles
- Cohort quiz to recommend a cohort
- Challenge test quiz based on cohort
"""

# Login Form

class LoginForm(AuthenticationForm):
    """ 
    Custom Login Form used in the application.
    It overrides the default AuthenticationForm to use email instead of username.
    """
    # Email field to be used as username
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))
    # Password field with input type as password
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        # Fields to be used in the form
        fields = ["username", "password"]

# Registration Form

class RegisterForm(UserCreationForm):
    """ 
    Registration form for new users.
    Includes fields for full name, email, password, and student type.
    """
    # Full name of the user (Required)
    full_name = forms.CharField(max_length=255, required=True, label="Full Name")
    # Email field (Required)
    email = forms.EmailField(required=True, label="Email")
    # Dropdown field for student type
    student_type = forms.ChoiceField(
        choices=[
            ('Future', 'Future Student'),
            ('Current', 'Current Student'),
            ('Alumni', 'Alumni Student'),
            ('None', 'Neither'),
        ],
        required=True,
        label="Student Type"
    )

    class Meta:
        # Bind form to CustomUser model
        model = CustomUser
        # Specify fields to be displayed
        fields = ["full_name", "email", "password1", "password2", "student_type"]

    def clean_email(self):
        """
        Custom validator to check if the email is unique.
        Raises validation error if email is already registered.
        """
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

# Forgot Password Form

class ForgotPasswordForm(forms.Form):
    """
    Simple form to collect user's email address for password reset request.
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

# Reset Password Form

class ResetPasswordForm(forms.Form):
    """
    Form for setting a new password.
    Includes both password and confirm password fields.
    """
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# Edit User Form

class EditUserForm(forms.ModelForm):
    """
    Form for admin to edit user details such as full name, email, and student type.
    """
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    student_type = forms.ChoiceField(choices=[
        ('Future', 'Future Student'),
        ('Current', 'Current Student'),
        ('Alumni', 'Alumni Student'),
        ('None', 'Neither'),
    ], widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        # Bind form to CustomUser model
        model = CustomUser
        # Fields to be displayed in the form
        fields = ['full_name', 'email', 'student_type']

# Cohort Quiz Form

class CohortQuizForm(forms.Form):
    """
    Form used to help users determine their suitable cohort.
    Contains six questions with three choices each (Cloud, Server, Cyber).
    """
    # Dictionary containing questions and corresponding choices
    CHOICES = {
        'q1': [
            ('Cloud', _("I love designing and coding innovative applications.")),
            ('Server', _("I enjoy configuring and managing IT infrastructure.")),
            ('Cyber', _("I like protecting systems and networks from threats.")),
        ],
        'q2': [
            ('Cloud', _("Building user-friendly web applications and software.")),
            ('Server', _("Optimizing system performance and scalability.")),
            ('Cyber', _("Investigating vulnerabilities and safeguarding data.")),
        ],
        'q3': [
            ('Cloud', _("Developing full-stack applications and interactive interfaces.")),
            ('Server', _("Deploying, monitoring, and managing cloud infrastructure.")),
            ('Cyber', _("Conducting penetration tests and implementing security measures.")),
        ],
        'q4': [
            ('Cloud', _("I enjoy creatively coding and prototyping solutions.")),
            ('Server', _("I systematically troubleshoot and optimize systems.")),
            ('Cyber', _("I analyze risks and design defensive strategies.")),
        ],
        'q5': [
            ('Cloud', _("A creative, collaborative team developing new software.")),
            ('Server', _("A dynamic IT department handling complex infrastructure challenges.")),
            ('Cyber', _("A security operations center where threats are monitored and mitigated.")),
        ],
        'q6': [
            ('Cloud', _("Through hands-on coding projects and interactive tutorials.")),
            ('Server', _("By tackling real-world system and network challenges.")),
            ('Cyber', _("Using simulated security scenarios and case studies.")),
        ],
    }

    # Definition of six multiple-choice questions
    q1 = forms.ChoiceField(
        label=_("1. How do you prefer to work?"),
        choices=CHOICES['q1'],
        widget=forms.RadioSelect(attrs={"class": "form-check-input"})
    )
    q2 = forms.ChoiceField(
        label=_("2. What aspect of technology excites you the most?"),
        choices=CHOICES['q2'],
        widget=forms.RadioSelect(attrs={"class": "form-check-input"})
    )
    q3 = forms.ChoiceField(
        label=_("3. What type of projects inspire you?"),
        choices=CHOICES['q3'],
        widget=forms.RadioSelect(attrs={"class": "form-check-input"})
    )
    q4 = forms.ChoiceField(
        label=_("4. How do you approach problem-solving?"),
        choices=CHOICES['q4'],
        widget=forms.RadioSelect(attrs={"class": "form-check-input"})
    )
    q5 = forms.ChoiceField(
        label=_("5. What work environment appeals most to you?"),
        choices=CHOICES['q5'],
        widget=forms.RadioSelect(attrs={"class": "form-check-input"})
    )
    q6 = forms.ChoiceField(
        label=_("6. How do you prefer to learn?"),
        choices=CHOICES['q6'],
        widget=forms.RadioSelect(attrs={"class": "form-check-input"})
    )

#Challenge Test Form

class ChallengeTestForm(forms.Form):
    """
    Dynamic form to quiz users based on their selected cohort.
    Questions and answers are predefined for each cohort.
    """
    # Predefined challenge questions and correct answers
    CHALLENGE_QUESTIONS = {
        "cloud": [
            ("q1", "What is serverless computing?", [("A", "A cloud computing model"), ("B", "A type of database"), ("C", "A security protocol")], "A"),
            ("q2", "Which of these is a popular cloud provider?", [("A", "AWS"), ("B", "React"), ("C", "TensorFlow")], "A"),
        ],
        "cybersecurity": [
            ("q1", "What does a firewall do?", [("A", "Prevents unauthorized access"), ("B", "Stores backup files"), ("C", "Speeds up network traffic")], "A"),
            ("q2", "Which is an example of multi-factor authentication?", [("A", "Password + SMS code"), ("B", "Username only"), ("C", "Public WiFi login")], "A"),
        ],
        "server": [
            ("q1", "What is a virtual machine?", [("A", "An emulation of a computer system"), ("B", "A programming language"), ("C", "A type of network cable")], "A"),
            ("q2", "Which tool is used for containerization?", [("A", "Docker"), ("B", "Photoshop"), ("C", "Microsoft Word")], "A"),
        ]
    }

    def __init__(self, cohort, *args, **kwargs):
        """
        Initialize the challenge quiz form dynamically based on cohort.
        Also randomizes answer choices.
        """
        super().__init__(*args, **kwargs)
        self.correct_answers = {}  # Store correct answers dynamically

        questions = self.CHALLENGE_QUESTIONS.get(cohort, [])  # Retrieve questions based on cohort

        for q_id, question, options, correct_answer in questions:
            # Shuffle options to make quiz less predictable
            random.shuffle(options)

            # Store correct answer
            new_correct_answer = [key for key, value in options if key == correct_answer][0]
            self.correct_answers[q_id] = new_correct_answer

            # Add question to form dynamically
            self.fields[q_id] = forms.ChoiceField(
                label=question,
                choices=options,
                widget=forms.RadioSelect(attrs={"class": "form-check-input"})
            )
            
    def evaluate(self):
        """
        Evaluates the quiz answers submitted by user.
        Returns:
            score (int): Number of correct answers
            total (int): Total number of questions
        """
        score = 0
        total = len(self.correct_answers)

        # Loop over each question and check if user's answer is correct
        for q_id, correct_answer in self.correct_answers.items():
            if self.cleaned_data.get(q_id) == correct_answer:
                score += 1

        # Return the score and total
        return score, total

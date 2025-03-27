from django import forms
import random
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

# Login Form
class LoginForm(AuthenticationForm):
    # Override the default username field to use email
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))
    # Password input field with form control class
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        fields = ["username", "password"]

# Registration Form
class RegisterForm(UserCreationForm):
    # Custom field for full name
    full_name = forms.CharField(max_length=255, required=True, label="Full Name")
    # Override default email handling
    email = forms.EmailField(required=True, label="Email")
    # Student type selection
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
        model = CustomUser
        fields = ["full_name", "email", "password1", "password2", "student_type"]

    # Check if the provided email already exists in the system
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email
    
#  Forgot Password Form
class ForgotPasswordForm(forms.Form):
    # Input field for email during password reset
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

#  Reset Password Form
class ResetPasswordForm(forms.Form):
    # New password field
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # Confirm password field to match above
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

#  Edit User Form
class EditUserForm(forms.ModelForm):
    # Editable name field
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # Drop-down to select student type
    student_type = forms.ChoiceField(choices=[
        ('Future', 'Future Student'),
        ('Current', 'Current Student'),
        ('Alumni', 'Alumni Student'),
        ('None', 'Neither'),
    ], widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'student_type']

#  Cohort Quiz Form
class CohortQuizForm(forms.Form):
    # Questions with multiple choice answers categorized by cohort type
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

    # Define each question field using ChoiceField and RadioSelect widget
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

# Challenge Test Form to quiz students by cohort
class ChallengeTestForm(forms.Form):
    # Predefined challenge questions mapped by cohort
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

    # Initialize the form dynamically based on selected cohort
    def __init__(self, cohort, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.correct_answers = {}

        questions = self.CHALLENGE_QUESTIONS.get(cohort, [])

        for q_id, question, options, correct_answer in questions:
            # Randomize the order of answer choices
            random.shuffle(options)

            # Store the new correct answer dynamically
            new_correct_answer = [key for key, value in options if key == correct_answer][0]
            self.correct_answers[q_id] = new_correct_answer

            # Add question to form fields with RadioSelect widget
            self.fields[q_id] = forms.ChoiceField(
                label=question,
                choices=options,
                widget=forms.RadioSelect(attrs={"class": "form-check-input"})
            )
            
    # Evaluate user's responses and return score
    def evaluate(self):
        score = 0
        total = len(self.correct_answers)

        for q_id, correct_answer in self.correct_answers.items():
            if self.cleaned_data.get(q_id) == correct_answer:
                score += 1

        return score, total

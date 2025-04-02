# Importing Django's built-in HTTP response classes for handling redirects
from django.http import HttpResponseRedirect

# Importing shortcut functions to render templates, redirect, and get objects from DB
from django.shortcuts import render, redirect, get_object_or_404

# Importing Django's built-in authentication functions
from django.contrib.auth import authenticate, login, logout

# Importing decorators to restrict view access to authenticated users or specific conditions
from django.contrib.auth.decorators import login_required, user_passes_test

# Importing Django's messaging framework to display success/error messages to users
from django.contrib import messages

# Importing Django's email utility to send emails
from django.core.mail import send_mail

# Importing Django settings to access configuration variables
from django.conf import settings

# Importing database models used in the project
from .models import CohortVisibility, CustomUser, CohortQuiz

# Importing all form classes used in the project
from .forms import (
    ChallengeTestForm, 
    LoginForm, 
    RegisterForm, 
    ForgotPasswordForm, 
    ResetPasswordForm, 
    EditUserForm, 
    CohortQuizForm
)

# Importing Django's translation utilities for multi-language support
from django.utils.translation import activate, get_language, get_language_from_request
from django.utils.translation import gettext as _

#  Home Page View
def home(request):
    """Redirect logged-in users to their respective homepages based on student type."""
    # Check if user is authenticated
    if request.user.is_authenticated:
        student_type = request.user.student_type

        # Redirect based on the type of student the user is
        if student_type == "Current":
            return redirect("current_student_home")
        elif student_type == "Future":
            return redirect("future_student_home")
        elif student_type == "Alumni":
            return redirect("alumni_home")
        
    # If not authenticated, render the public home page
    cohort_visibility = CohortVisibility.objects.all()
    return render(request, "home/index.html", {"cohort_visibility": cohort_visibility})


# User Login View
def login_view(request):
    """
    Handle user login functionality.
    Authenticates user and redirects based on student type.
    """
    if request.method == "POST":
        # Create a LoginForm instance with POST data
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            # Retrieve cleaned data from form
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            try:
                # Try to get the user using the email provided
                user = CustomUser.objects.get(email=email)  # Find user by email
                user = authenticate(request, email=user.email, password=password)

                if user:
                    # Log the user in
                    login(request, user)

                    # Redirect based on student type
                    if user.student_type == "Current":
                        return redirect("current_student_home")
                    elif user.student_type == "Future":
                        return redirect("future_student_home")
                    elif user.student_type == "Alumni":
                        return redirect("alumni_home")
                    else:
                        # Fallback to a default home page if type does not match
                        return redirect("home")  # Default home page

                else:
                    # Add error message if authentication fails
                    messages.error(request, "Invalid email or password.")

            except CustomUser.DoesNotExist:
                # Handle case where user with provided email does not exist
                messages.error(request, "User with this email does not exist.")

        else:
            # Add error message if form data is invalid
            messages.error(request, "Invalid email or password.")

    else:
        # If GET request, instantiate an empty LoginForm
        form = LoginForm()

    return render(request, "account/login.html", {"form": form})

# User Registration View
def register_view(request):
    """
    Handles new user registration.
    Creates user account and assigns admin privileges for specific email.
    """

    if request.method == "POST":
        # Instantiate the registration form with POST data
        form = RegisterForm(request.POST)

        if form.is_valid():

            # Extract form data
            full_name = form.cleaned_data["full_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            student_type = form.cleaned_data["student_type"]

            # Ensure email is unique
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email is already in use.")
                return render(request, "account/register.html", {"form": form})

            # Create user
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                full_name=full_name,
                student_type=student_type,
            )

            # Make admin if email is "adminemail@gmail.com"
            if email.lower() == "adminemail@gmail.com":
                user.is_staff = True
                user.is_superuser = True
                user.save()

            login(request, user)
            return redirect("register_success")  # Redirect to success page

        else:
            messages.error(request, "Registration failed. Please check your details or try again with a different email.")

    else:
        form = RegisterForm()

    return render(request, "account/register.html", {"form": form})

# Forgot Password View
def forgot_password(request):
    """Handles forgot password process."""
    if request.method == "POST":
        # Instantiate ForgotPasswordForm with POST data
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            # Get the user based on the submitted email
            user = CustomUser.objects.filter(email=form.cleaned_data["email"]).first()
            if user:
                # Build a password reset link for the user
                reset_link = request.build_absolute_uri(f"/reset-password/{user.id}/")
                # Send an email with the password reset link
                send_mail(
                    "Reset Password",
                    f"Click here to reset your password: {reset_link}",
                    "secureprog123@gmail.com",
                    [user.email]
                )
        # Redirect to a confirmation page after processing the request
        return redirect("forgot_password_confirmation") 

    else:
        # If GET request, instantiate an empty ForgotPasswordForm
        form = ForgotPasswordForm()
    # Render the forgot password template with the form
    return render(request, "account/forgot_password.html", {"form": form})

# Forgot Password Confirmation View
def forgot_password_confirmation(request):
    """ View for forgot password confirmation message """
    return render(request, "account/forgot_password_confirmation.html")

# Reset Password View
def reset_password(request, user_id):
    """Handles password reset for a given user."""
    # Retrieve the user or return 404 if not found
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        # Instantiate the ResetPasswordForm with POST data
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            # Update the user's password
            user.set_password(form.cleaned_data["password"])
            user.save()
            # Redirect to a confirmation page after resetting the password
            return redirect("reset_password_confirmation")
    else:
        # If GET request, instantiate an empty ResetPasswordForm
        form = ResetPasswordForm()
    # Render the password reset template with the form
    return render(request, "account/reset_password.html", {"form": form})

# Logout View
@login_required
def logout_view(request):
    """Logs out a user and displays the logged out page."""
    # Terminate the user's session
    logout(request)
    # Render a template confirming that the user has been logged out
    return render(request, "account/logged_out.html")   

# Registration Success Page
def register_success(request):
    """Registration success page."""
    # Render the registration success template
    return render(request, "account/register_success.html")


#  Admin Views
def admin_check(user):
    """ Checks if the user is an admin """
    return user.is_superuser


@user_passes_test(admin_check)
def manage_users(request):
    """Displays all users (Admin only)."""
    # Retrieve all user objects from the database
    users = CustomUser.objects.all()
    # Render the admin user management template with the list of users
    return render(request, "admin/manage_users.html", {"users": users})


@user_passes_test(admin_check)
def edit_user(request, user_id):
    """Allows Admin to edit a user's details."""
    # Retrieve the user to edit or return 404 if not found
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        # Instantiate the edit form with POST data and bind it to the user instance
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            # Save the updated user details
            form.save()
            # Redirect back to the user management page
            return redirect("manage_users")
    else:
        # If GET request, instantiate the form with current user data
        form = EditUserForm(instance=user)
    # Render the edit user template with the form and user data
    return render(request, "admin/edit_user.html", {"form": form, "user": user})


@user_passes_test(admin_check)
def delete_user(request, user_id):
    """Allows Admin to delete a user."""
    # Retrieve the user to be deleted or return 404 if not found
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        # Delete the user and redirect back to the management page
        user.delete()
        return redirect("manage_users")
    # Render the delete confirmation template with the user data
    return render(request, "admin/delete_user.html", {"user": user})


#  Quiz Views
def cohort_quiz(request):
    """Handles the Cohort Quiz"""
    if request.method == "POST":
        # Instantiate the CohortQuizForm with submitted data
        form = CohortQuizForm(request.POST)

        if form.is_valid():
            # Count the number of times each option is chosen
            score_cloud = sum(1 for answer in form.cleaned_data.values() if answer == "Cloud")
            score_server = sum(1 for answer in form.cleaned_data.values() if answer == "Server")
            score_cyber = sum(1 for answer in form.cleaned_data.values() if answer == "Cyber")

            # Determine the highest score
            max_score = max(score_cloud, score_server, score_cyber)
            suggestions = []

            # Append cohort suggestions based on the highest score
            if score_cloud == max_score:
                suggestions.append("Cloud Application Development")
            if score_server == max_score:
                suggestions.append("Server & Cloud Applications")
            if score_cyber == max_score:
                suggestions.append("Cybersecurity Administration")

            # Construct result message
            if len(suggestions) == 1:
                suggestion_message = f"Based on your answers, you should consider the {suggestions[0]} cohort."
            elif len(suggestions) == 2:
                suggestion_message = f"Based on your answers, you should consider the {suggestions[0]} and {suggestions[1]} cohorts."
            elif len(suggestions) == 3:
                suggestion_message = f"Based on your answers, you should consider the {suggestions[0]}, {suggestions[1]}, and {suggestions[2]} cohorts."

            # Render the quiz result page with suggestion and score details
            return render(request, "quiz/cohort_quiz_result.html", {
                "suggestion": suggestion_message,
                "score_cloud": score_cloud,
                "score_server": score_server,
                "score_cyber": score_cyber
            })

    else:
        form = CohortQuizForm()

    return render(request, "quiz/cohort_quiz.html", {"form": form})


#  Study Views
def study_description(request, title):
    """ Displays study resources dynamically based on the title """

    # Dictionary of study resources
    resources = {
        # Cloud Application Development
        _("Cloud Development Bootcamp"): {
            "description": _("This immersive bootcamp offers a step-by-step guide to building cloud-native applications. Learn key concepts like microservices architecture, containerization, and continuous deployment, using modern tools such as Docker and Kubernetes."),
            "resource_url": "https://www.codecademy.com/learn",
            "skills": _("Microservices, Docker, Kubernetes, DevOps pipelines"),
        },
        _("Developing on AWS"): {
            "description": _("This resource provides an in-depth introduction to designing, building, and deploying applications on Amazon Web Services (AWS). Learn essential AWS services like Lambda, DynamoDB, and API Gateway."),
            "resource_url": "https://aws.amazon.com/getting-started/",
            "skills": _("AWS Lambda, DynamoDB, API Gateway, Serverless architectures"),
        },
        _("Microsoft Learn: App Development"): {
            "description": _("Explore the world of cloud application development with Microsoft's free interactive learning platform. This course covers Azure App Services, Azure Functions, and CI/CD pipelines."),
            "resource_url": "https://learn.microsoft.com/en-us/training/",
            "skills": _("Azure App Services, Azure Functions, CI/CD, Cloud scaling"),
        },
        _("Full-Stack Cloud Development"): {
            "description": _("This specialization, offered by IBM on Coursera, teaches you how to develop full-stack cloud-based applications, covering front-end frameworks, server-side scripting, and database integration."),
            "resource_url": "https://www.coursera.org/specializations/ibm-cloud-application-development-foundations",
            "skills": _("Front-end frameworks, Server-side scripting, Database integration, Continuous delivery"),
        },
        _("Google Cloud Application Development"): {
            "description": _("Google Cloud's comprehensive learning platform offers tutorials, labs, and certifications to help you master cloud app development, including scalable backend systems and serverless functions."),
            "resource_url": "https://cloud.google.com/training",
            "skills": _("Google Cloud, Serverless functions, App Engine, Cloud SQL"),
        },
        _("IBM Application Development"): {
            "description": _("Dive into IBM's developer portal to learn about creating cloud-native applications using IBM Cloud services, including Watson AI and Kubernetes."),
            "resource_url": "https://developer.ibm.com",
            "skills": _("IBM Cloud, Watson AI, Kubernetes, Advanced cloud development"),
        },

        # Cybersecurity
        _("CompTIA Security+"): {
            "description": _("CompTIA Security+ is an industry-recognized certification designed for entry-level professionals. This resource covers risk management, network security, and compliance."),
            "resource_url": "https://www.comptia.org/certifications/security",
            "skills": _("Network security, Risk management, Compliance, Threat prevention"),
        },
        _("Introduction to Cybersecurity"): {
            "description": _("Offered by Cisco Networking Academy, this beginner-friendly course introduces the core concepts of cybersecurity, including types of attacks, threat detection, and data protection strategies."),
            "resource_url": "https://www.netacad.com/courses/cybersecurity",
            "skills": _("Threat detection, Data protection, Basic cyber attacks, Cisco tools"),
        },
        _("Certified Ethical Hacker"): {
            "description": _("The CEH certification from EC-Council is a globally respected credential that teaches ethical hacking techniques and methodologies to identify vulnerabilities and strengthen systems against cyberattacks."),
            "resource_url": "https://www.eccouncil.org/programs/certified-ethical-hacker-ceh/",
            "skills": _("Penetration testing, Vulnerability analysis, Network scanning, Ethical hacking"),
        },
        _("Google Cybersecurity Training"): {
            "description": _("This free training program from Google offers hands-on exercises and certification preparation for those interested in practical cybersecurity applications."),
            "resource_url": "https://grow.google/certificates/",
            "skills": _("Google security tools, System hardening, Network fundamentals, Cyber labs"),
        },
        _("Stanford Advanced Cybersecurity"): {
            "description": _("Offered by Stanford University, this advanced program explores cutting-edge practices in threat analysis, risk assessment, and data protection."),
            "resource_url": "https://online.stanford.edu/professional-education",
            "skills": _("Threat analysis, Risk assessment, Data protection, Advanced attack vectors"),
        },
        _("IBM Cybersecurity Analyst"): {
            "description": _("This professional certificate on Coursera provides in-depth knowledge of security intelligence, event management, incident response, and risk analysis."),
            "resource_url": "https://www.coursera.org/professional-certificates/ibm-cybersecurity-analyst",
            "skills": _("SIEM systems, Incident response, Security analytics, IBM security tools"),
        },

        # Server & Cloud Applications
        _("AWS Certified Solutions Architect"): {
            "description": _("This highly regarded certification by AWS equips you with the knowledge and skills to design, deploy, and operate highly available, cost-effective, and secure applications on AWS."),
            "resource_url": "https://aws.amazon.com/certification/certified-solutions-architect-associate/",
            "skills": _("AWS architecture, High availability, Cost optimization, Security best practices"),
        },
        _("Microsoft Azure Fundamentals"): {
            "description": _("Ideal for beginners, this certification offers a thorough introduction to Microsoft Azure services, covering cloud concepts, core Azure services, pricing, and security fundamentals."),
            "resource_url": "https://learn.microsoft.com/en-us/certifications/azure-fundamentals/",
            "skills": _("Azure basics, Cloud concepts, Azure security, Cost management"),
        },
        _("Introduction to Kubernetes"): {
            "description": _("This resource from Kubernetes.io introduces you to container orchestration, helping you manage and deploy containers across clusters effectively."),
            "resource_url": "https://kubernetes.io/docs/tutorials/",
            "skills": _("Container orchestration, Clusters, Pods & services, Deployment best practices"),
        },
        _("Google Cloud Fundamentals"): {
            "description": _("Learn the basics of Google Cloud Platform through interactive lessons and hands-on labs, covering cloud computing fundamentals, managing virtual machines, and leveraging Google Cloud's unique features."),
            "resource_url": "https://cloud.google.com/training",
            "skills": _("Compute Engine, VM management, GCP fundamentals, Scalability"),
        },
        _("IBM Cloud Learn Hub"): {
            "description": _("The IBM Cloud Learn Hub offers resources on app modernization, AI integration, Kubernetes, and hybrid cloud setups."),
            "resource_url": "https://www.ibm.com/cloud/learn",
            "skills": _("IBM Cloud, App modernization, Hybrid cloud, AI integration"),
        },
        _("Cloud Academy"): {
            "description": _("Cloud Academy offers interactive quizzes, hands-on labs, and comprehensive courses to help you become a cloud expert across AWS, Azure, Google Cloud, and Kubernetes."),
            "resource_url": "https://cloudacademy.com",
            "skills": _("AWS, Azure, Google Cloud, Kubernetes, Continuous learning"),
        },
    }

    # Retrieve resource details based on the title
    resource = resources.get(_(title), None)

    if not resource:
        return render(request, "study/not_found.html", {"title": _(title)})

    # Prepare the context with resource details for rendering
    context = {
        "title": _(title),
        "description": resource["description"],
        "resource_url": resource["resource_url"],
        "skills": resource["skills"],
    }

    # Render the study description page with the resource context
    return render(request, "study/description.html", context)


#  Static Page Views
def about_us(request):
    """Displays About Us page."""
    return render(request, "home/about_us.html")


def faq(request):
    """Displays Frequently Asked Questions (FAQ) page."""
    return render(request, "home/faq.html")

def privacy(request):
    """Displays Privacy Policy page."""
    return render(request, 'home/privacy.html')


def server_cloud(request):
    """Displays Server & Cloud Applications cohort page."""
    return render(request, "home/server_cloud.html")


def cloud_app_development(request):
    """Displays Cloud Application Development cohort page."""
    return render(request, "home/cloud_app_development.html")


def cybersecurity(request):
    """Displays Cybersecurity Administration cohort page."""
    return render(request, "home/cybersecurity.html")


@login_required
def current_student_home(request):
    """Displays homepage for current students."""
    cohort_visibility = CohortVisibility.objects.all()
    return render(request, "home/current_student_home.html", {"cohort_visibility": cohort_visibility})


@login_required
def future_student_home(request):
    """Displays homepage for future students."""
    cohort_visibility = CohortVisibility.objects.all()
    return render(request, "home/future_student_home.html", {"cohort_visibility": cohort_visibility})


@login_required
def alumni_home(request):
    """Displays homepage for alumni."""
    cohort_visibility = CohortVisibility.objects.all()
    return render(request, "home/alumni_home.html", {"cohort_visibility": cohort_visibility})

# Challenge Test View
def challenge_test(request, cohort):
    """
    Handles challenge test quiz based on selected cohort.
    Evaluates user's performance and shows results.
    """
    form = ChallengeTestForm(cohort, request.POST or None)
    result = None

    if request.method == "POST" and form.is_valid():
        # Evaluate the test to get the score and total
        score, total = form.evaluate()
        # Prepare the result message with the score details
        result = f"You scored {score} out of {total}!"
    # Render the challenge test page with form, cohort information, and result
    return render(request, "quiz/challenge_test.html", {"form": form, "cohort": cohort, "result": result})

@user_passes_test(admin_check)
def manage_cohorts(request):
    """
    Admin view to enable/disable cohort visibility.
    Allows admin to toggle whether cohorts are visible to users.
    """
    # Auto-create cohorts if missing
    default_cohorts = [
        "Server & Cloud Applications",
        "Cloud Application Development",
        "Cybersecurity Administration"
    ]
    
    for name in default_cohorts:
        CohortVisibility.objects.get_or_create(name=name)

    # Handle POST request (toggle)
    if request.method == "POST":
        cohort_id = request.POST.get("cohort_id")
        cohort = get_object_or_404(CohortVisibility, id=cohort_id)
        cohort.enabled = not cohort.enabled
        cohort.save()
        return redirect("manage_cohorts")

    # Render the manage cohort page
    cohorts = CohortVisibility.objects.all()
    return render(request, "admin/manage_cohorts.html", {"cohorts": cohorts})

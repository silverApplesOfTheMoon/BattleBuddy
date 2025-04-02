# Import Django's path function to define URL patterns
from django.urls import path
# Import all views from the current app
from . import views
# Import i18n_patterns to support language translation URLs
from django.conf.urls.i18n import i18n_patterns
# Import set_language view to handle language change requests
from django.views.i18n import set_language

# Define all URL patterns for the web application
urlpatterns = [
    # Home page - Redirects users to the appropriate home view based on authentication status
    path("", views.home, name="home"),
    
    # User login view
    path("login/", views.login_view, name="login"),
    # User registration view
    path("register/", views.register_view, name="register"),
    # Registration success page
    path('register-success/', views.register_success, name='register_success'),
    # User logout view
    path("logout/", views.logout_view, name="logout"),
    # Current student home view
    path('current-student-home/', views.current_student_home, name='current_student_home'),
    # Future student home view
    path('future-student-home/', views.future_student_home, name='future_student_home'),
    # Alumni home view
    path('alumni-home/', views.alumni_home, name='alumni_home'),
    # Forgot password page
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    # Password reset page with dynamic user_id parameter
    path("reset-password/<int:user_id>/", views.reset_password, name="reset_password"),
    # Forgot password confirmation message
    path("forgot-password-confirmation/", views.forgot_password_confirmation, name="forgot_password_confirmation"),

    # Admin user management page
    path("manage-users/", views.manage_users, name="manage_users"),
    # Edit user details page, accepts user_id as parameter
    path("edit-user/<int:user_id>/", views.edit_user, name="edit_user"),
    # Delete user page, accepts user_id as parameter
    path("delete-user/<int:user_id>/", views.delete_user, name="delete_user"),

    # Cohort quiz page for students
    path("cohort-quiz/", views.cohort_quiz, name="cohort_quiz"),

    # Study description page with dynamic title parameter
    path("study/<str:title>/", views.study_description, name="study_description"),

    # About Us static page
    path("about-us/", views.about_us, name="about_us"),
    # FAQ static page
    path("faq/", views.faq, name="faq"),
    # Privacy Policy static page
    path('privacy/', views.privacy, name='privacy'),
    # Server and Cloud cohort page
    path("server-cloud/", views.server_cloud, name="server_cloud"),
    # Cloud Application Development cohort page
    path("cloud-app-development/", views.cloud_app_development, name="cloud_app_development"),
    # Cybersecurity cohort page
    path("cybersecurity/", views.cybersecurity, name="cybersecurity"),
    # Current student home view (duplicate - can be removed)
    path("current-student-home/", views.current_student_home, name="current_student_home"),
    # Future student home view (duplicate - can be removed)
    path("future-student-home/", views.future_student_home, name="future_student_home"),
    # Alumni home view (duplicate - can be removed)
    path("alumni-home/", views.alumni_home, name="alumni_home"),

    # URL endpoint for setting user's preferred language
    path('i18n/setlang/', set_language, name='set_language'),

    # Challenge test page with dynamic cohort parameter
    path('challenge-test/<str:cohort>/', views.challenge_test, name="challenge_test"),
    
    # Admin control page for enabling/disabling cohort visibility globally
    path("manage-cohorts/", views.manage_cohorts, name="manage_cohorts"),
]

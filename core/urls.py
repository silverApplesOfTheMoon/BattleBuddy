from django.urls import path
from . import views
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

urlpatterns = [
    path("", views.home, name="home"),
    
    # Authentication
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path('register-success/', views.register_success, name='register_success'),
    path("logout/", views.logout_view, name="logout"),
    path('current-student-home/', views.current_student_home, name='current_student_home'),
    path('future-student-home/', views.future_student_home, name='future_student_home'),
    path('alumni-home/', views.alumni_home, name='alumni_home'),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/<int:user_id>/", views.reset_password, name="reset_password"),
    path("forgot-password-confirmation/", views.forgot_password_confirmation, name="forgot_password_confirmation"),


    # Admin
    path("manage-users/", views.manage_users, name="manage_users"),
    path("edit-user/<int:user_id>/", views.edit_user, name="edit_user"),
    path("delete-user/<int:user_id>/", views.delete_user, name="delete_user"),

    # Quiz
    path("cohort-quiz/", views.cohort_quiz, name="cohort_quiz"),

    # Study
    path("study/<str:title>/", views.study_description, name="study_description"),

    # Static Pages
    path("about-us/", views.about_us, name="about_us"),
    path("faq/", views.faq, name="faq"),
    path('privacy/', views.privacy, name='privacy'),
    path("server-cloud/", views.server_cloud, name="server_cloud"),
    path("cloud-app-development/", views.cloud_app_development, name="cloud_app_development"),
    path("cybersecurity/", views.cybersecurity, name="cybersecurity"),
    path("current-student-home/", views.current_student_home, name="current_student_home"),
    path("future-student-home/", views.future_student_home, name="future_student_home"),
    path("alumni-home/", views.alumni_home, name="alumni_home"),

    path('i18n/setlang/', set_language, name='set_language'),

    path('challenge-test/<str:cohort>/', views.challenge_test, name="challenge_test"),
]

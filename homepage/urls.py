from django.urls import path
from .views import (
    homepage,
    login_view,
    logout_view,
    signup_view,
    all_exams,
    exam_sections,
    section_questions,
    start_test,
    evaluate_test,
    show_result,
    test_history,
    leaderboard,
    upload_csv,
)

app_name = "homepage"


urlpatterns = [
    path("", homepage, name="home"),
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),
    path("exams/", all_exams, name="exams"),
    path("exams/<int:exam_id>/sections/", exam_sections, name="sections"),
    path("sections/<int:section_id>/questions/", section_questions, name="questions"),
    path("sections/<int:section_id>/start/", start_test, name="start_test"),
    path("sections/<int:section_id>/submit/", evaluate_test, name="evaluate_test"),
    path("sections/<int:section_id>/result/", show_result, name="show_result"),
    path("test-history/", test_history, name="test_history"),
    path("section/<int:section_id>/leaderboard/", leaderboard, name="leaderboard"),
    path("upload-csv/", upload_csv, name="upload_csv"),
]

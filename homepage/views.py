from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Max


import csv
from django.contrib import messages

# from django.shortcuts import render, redirect
from .models import Exam, Section, Question
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage


def homepage(request):
    return render(request, "homepage.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("homepage:home")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already exists"})
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        return redirect("homepage:login")
    return render(request, "signup.html")


def logout_view(request):
    logout(request)
    return redirect("homepage:login")


from django.shortcuts import render, get_object_or_404
from .models import Exam, Section, Question


def all_exams(request):
    exams = Exam.objects.all()
    return render(request, "homepage/exams.html", {"exams": exams})


def exam_sections(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    sections = exam.sections.all()
    return render(
        request, "homepage/sections.html", {"exam": exam, "sections": sections}
    )


def section_questions(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    questions = section.questions.all()
    return render(
        request, "homepage/questions.html", {"section": section, "questions": questions}
    )


from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Section, Question


@login_required
def start_test(request, section_id):
    section = Section.objects.get(id=section_id)
    questions = section.questions.all()

    return render(
        request,
        "homepage/start_test.html",
        {
            "section": section,
            "questions": questions,
            "total_time": len(questions) * 60,  # seconds (1 min per question)
        },
    )


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import Section, Question, Result


@login_required
def evaluate_test(request, section_id):
    if request.method == "POST":
        section = get_object_or_404(Section, id=section_id)
        questions = section.questions.all()

        correct = 0
        wrong = 0
        attempted = 0

        for q in questions:
            submitted = request.POST.get(f"q{q.id}")
            if submitted:
                attempted += 1
                if submitted == q.correct:
                    correct += 1
                else:
                    wrong += 1

        total_questions = questions.count()
        score = round((correct / total_questions) * 100, 2)

        # Save result to DB
        Result.objects.create(
            user=request.user,
            section=section,
            total_questions=total_questions,
            attempted=attempted,
            correct=correct,
            wrong=wrong,
            score=score,
        )

        return redirect("homepage:show_result", section_id=section.id)

    return redirect("homepage:home")


def show_result(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    result = Result.objects.filter(user=request.user, section=section).latest(
        "created_at"
    )
    return render(request, "homepage/show_result.html", {"result": result})


def test_history(request):
    results = Result.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "homepage/test_history.html", {"results": results})


@login_required
def leaderboard(request, section_id):
    section = get_object_or_404(Section, id=section_id)

    # Get top scores for that section (best score per user)
    top_results = (
        Result.objects.filter(section=section)
        .values("user__username")
        .annotate(best_score=Max("score"))
        .order_by("-best_score")[:10]
    )

    return render(
        request,
        "homepage/leaderboard.html",
        {"section": section, "top_results": top_results},
    )


def upload_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        file = request.FILES["csv_file"]
        if not file.name.endswith(".csv"):
            messages.error(request, "This file is not a CSV.")
            return redirect("homepage:upload_csv")

        # Save file to temp
        file_path = default_storage.save("tmp/questions.csv", file)

        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                exam_name = row["exam"].strip()
                section_name = row["section"].strip()
                question_text = row["question"].strip()

                # Create or get exam
                exam, _ = Exam.objects.get_or_create(name=exam_name)

                # Create or get section
                section, _ = Section.objects.get_or_create(
                    title=section_name, exam=exam
                )

                # Create question
                Question.objects.create(
                    section=section,
                    text=question_text,
                    option_a=row["option_a"],
                    option_b=row["option_b"],
                    option_c=row["option_c"],
                    option_d=row["option_d"],
                    correct=row["correct"].strip().upper(),
                )

            messages.success(request, "Questions uploaded successfully!")
            return redirect("homepage:upload_csv")

    return render(request, "homepage/upload_csv.html")

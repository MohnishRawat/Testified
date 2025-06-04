from django.db import models
from django.contrib.auth.models import User


class Exam(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Section(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="sections")
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.exam.name} – {self.title}"


class Question(models.Model):
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="questions"
    )
    text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct = models.CharField(
        max_length=1, choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")]
    )

    def __str__(self):
        return self.text[:50]


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    total_questions = models.IntegerField()
    attempted = models.IntegerField()
    correct = models.IntegerField()
    wrong = models.IntegerField()
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.section.title} - {self.score}"

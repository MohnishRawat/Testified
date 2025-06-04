import csv
from django.core.management.base import BaseCommand
from homepage.models import Exam, Section, Question


class Command(BaseCommand):
    help = "Import exams, sections, and questions from CSV file"

    def handle(self, *args, **kwargs):
        with open("exam_data.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                exam, _ = Exam.objects.get_or_create(title=row["exam_title"])
                section, _ = Section.objects.get_or_create(
                    exam=exam, title=row["section_title"]
                )
                Question.objects.create(
                    section=section, text=row["question_text"], answer=row["answer"]
                )

        self.stdout.write(self.style.SUCCESS("Data imported successfully!"))

from django.urls import path

from .views import (students_view, tutors_view)

app_name = "home"
urlpatterns = [
    path("students/", view=students_view, name="students"),
    path("tutors/", view=tutors_view, name="tutors"),
]

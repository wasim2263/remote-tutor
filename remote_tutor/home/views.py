from django.shortcuts import render

# Create your views here.
from django.views import View

from remote_tutor.home.forms import FindTutorForm
from remote_tutor.tuition.models import Tuition
from remote_tutor.tutor.models import Tutor, CLASS_LEVELS


class StudentsView(View):
    def get(self, request):
        find_tutor_form = FindTutorForm(request.GET)
        if find_tutor_form.is_valid():
            tutors = find_tutor_form.get_tutor_list()
        else:
            tutors = Tutor.objects.filter(user__isnull=False).select_related('preference').prefetch_related(
                'user__profile')

        tuition = Tuition.objects.filter(tutor=None)
        context = {
            'tutors': tutors,
            'find_tutor_form': find_tutor_form,
            'class_levels': dict(CLASS_LEVELS),
            'tuition': tuition
        }

        return render(request, 'home/students.html', context=context)


students_view = StudentsView.as_view()


class TutorsView(View):
    def get(self, request):
        find_tutor_form = FindTutorForm(request.GET)
        if find_tutor_form.is_valid():
            tutors = find_tutor_form.get_tutor_list()
        else:
            tutors = Tutor.objects.filter(user__isnull=False).select_related('preference').prefetch_related(
                'user__profile')

        tuition = Tuition.objects.filter(tutor=None)
        context = {
            'tutors': tutors,
            'find_tutor_form': find_tutor_form,
            'class_levels': dict(CLASS_LEVELS),
            'tuition': tuition
        }

        return render(request, 'home/tutors.html', context=context)


tutors_view = TutorsView.as_view()

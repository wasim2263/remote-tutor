from django import forms
from django_select2.forms import Select2Widget, Select2MultipleWidget

from remote_tutor.tutor.models import School, College, University, Department, Tutor, Subject, CLASS_LEVELS


class FindTutorForm(forms.Form):
    school = forms.ModelChoiceField(queryset=School.objects.all(), widget=Select2Widget, required=False)
    college = forms.ModelChoiceField(queryset=College.objects.all(), widget=Select2Widget, required=False)
    university = forms.ModelChoiceField(queryset=University.objects.all(), widget=Select2Widget, required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=Select2Widget, required=False)
    subject = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), widget=Select2MultipleWidget,
                                             required=False)
    class_level = forms.MultipleChoiceField(choices=CLASS_LEVELS, widget=Select2MultipleWidget, required=False)

    def get_tutor_list(self):
        school = self.cleaned_data['school']
        college = self.cleaned_data['college']
        university = self.cleaned_data['university']
        department = self.cleaned_data['department']
        subject = self.cleaned_data['subject']
        class_level = self.cleaned_data['class_level']
        tutor = Tutor.objects.filter(user__isnull=False).select_related('preference').prefetch_related('user__profile').distinct()
        if school:
            tutor = tutor.filter(user__profile__school=school)

        if college:
            tutor = tutor.filter(user__profile__college=college)

        if university:
            tutor = tutor.filter(user__profile__university=university)

        if department:
            tutor = tutor.filter(user__profile__department=department)

        if subject:
            tutor = tutor.filter(preference__subject__in=subject)
        if class_level:
            tutor = tutor.filter(preference__class_level__contains=class_level)

        return tutor

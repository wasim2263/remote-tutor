from django import forms as django_forms
from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django_select2.forms import Select2MultipleWidget, Select2Widget

from remote_tutor.tutor.models import Tutor, Preference, CLASS_LEVELS, School

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):
    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class TutorForm(django_forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['school', 'college', 'university', 'department', 'current_occupation', 'current_institute', ]
        widgets = {
            "school": Select2Widget,
            "college": Select2Widget,
            "university": Select2Widget,
            "department": Select2Widget,
            "current_occupation": Select2Widget,
        }


class TutorPreferenceForm(django_forms.ModelForm):
    class_level = django_forms.MultipleChoiceField(
        required=True,
        widget=Select2MultipleWidget,
        choices=CLASS_LEVELS
    )

    class Meta:
        model = Preference
        fields = ['tuition_type', 'class_level', 'subject', 'salary']
        widgets = {
            "subject": Select2MultipleWidget
        }

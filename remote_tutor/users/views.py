from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DetailView, RedirectView, UpdateView
from remote_tutor.tutor.models import Tutor, Subject
from remote_tutor.users.forms import TutorForm, TutorPreferenceForm

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = 'users/user_profile.html'


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["full_name", "phone_no", "gender"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class UserDetailView(DetailView):
    template_name = 'users/user_profile.html'
    context_object_name = 'user'
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:profile',
                       kwargs={'username': self.request.user.username})


class UserTutorView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            tutor = request.user.tutor
        except User.tutor.RelatedObjectDoesNotExist:
            tutor = None
        tutor_form = TutorForm(instance=tutor)
        context = {
            'tutor_form': tutor_form
        }
        return render(request, "users/user_tutor.html", context=context)

    def post(self, request):
        try:
            old_tutor = request.user.tutor
        except User.tutor.RelatedObjectDoesNotExist:
            old_tutor = None
        tutor_form = TutorForm(request.POST, instance=old_tutor)
        if tutor_form.is_valid():
            tutor = tutor_form.save(commit=False)
            tutor.user = request.user
            tutor.save()
            if old_tutor:
                return redirect("users:tutor")
            else:
                return redirect("users:tutor_preference")

        context = {
            'tutor_form': tutor_form
        }
        return render(request, "users/user_tutor.html", context=context)


user_tutor_view = UserTutorView.as_view()


class UserTutorPreference(LoginRequiredMixin, View):

    def get(self, request):
        try:
            tutor_preference = request.user.tutor.preference
        except User.tutor.RelatedObjectDoesNotExist:
            messages.info(request, _("Fill up this form to become a tutor."))
            return redirect("users:tutor")
        except Tutor.preference.RelatedObjectDoesNotExist:
            tutor_preference = None
        tutor_preference_form = TutorPreferenceForm(instance=tutor_preference)
        context = {
            'tutor_preference_form': tutor_preference_form
        }
        return render(request, "users/user_tutor_preference.html", context=context)

    def post(self, request):
        try:
            old_tutor_preference = request.user.tutor.preference
        except User.tutor.RelatedObjectDoesNotExist:
            messages.info(request, _("Fill up this form to become a tutor."))
            return redirect("users:tutor")
        except Tutor.preference.RelatedObjectDoesNotExist:
            old_tutor_preference = None
        tutor_preference_form = TutorPreferenceForm(request.POST, instance=old_tutor_preference)
        if tutor_preference_form.is_valid():
            tutor_preference = tutor_preference_form.save(commit=False)
            tutor_preference.tutor = request.user.tutor
            tutor_preference.save()
            new_subjects = tutor_preference_form.cleaned_data['subject']
            for subject in new_subjects:
                tutor_preference.subject.add(subject)
            old_subjects = Subject.objects.filter(preference=tutor_preference)
            for subject in old_subjects:
                if subject not in new_subjects:
                    tutor_preference.subject.remove(subject)

            return redirect('users:tutor_preference')
        context = {
            'tutor_preference_form': tutor_preference_form
        }
        return render(request, "users/user_tutor_preference.html", context=context)


user_tutor_preference_view = UserTutorPreference.as_view()


class UserStudentView(LoginRequiredMixin, View):
    pass


user_student_view = UserStudentView.as_view()

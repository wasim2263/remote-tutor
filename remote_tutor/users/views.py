from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DetailView, RedirectView, UpdateView

from remote_tutor.tuition.models import Tuition
from remote_tutor.tutor.models import Tutor, Subject
from remote_tutor.users.forms import TutorForm, TutorPreferenceForm, ProfileForm, StudentForm, TuitionForm
from remote_tutor.users.models import Profile

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
    @staticmethod
    def get_profile_and_tutor(request):
        try:
            user_profile = request.user.profile
        except User.profile.RelatedObjectDoesNotExist:
            user_profile = None

        if user_profile:
            try:
                tutor = user_profile.tutor
            except Profile.tutor.RelatedObjectDoesNotExist:
                tutor = None
        else:
            tutor = None

        return user_profile, tutor

    def get(self, request):

        user_profile, tutor = self.get_profile_and_tutor(request)
        tutor_form = TutorForm(instance=tutor)
        user_profile_form = ProfileForm(instance=user_profile)
        context = {
            'user_profile_form': user_profile_form,
            'tutor_form': tutor_form
        }
        return render(request, "users/user_tutor.html", context=context)

    def post(self, request):
        old_user_profile, old_tutor = self.get_profile_and_tutor(request)
        user_profile_form = ProfileForm(request.POST, instance=old_user_profile)
        tutor_form = TutorForm(request.POST, instance=old_tutor)
        if user_profile_form.is_valid() and tutor_form.is_valid():

            user_profile = user_profile_form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            tutor = tutor_form.save(commit=False)
            tutor.user_profile = user_profile
            tutor.save()
            if old_tutor:
                return redirect("users:tutor")
            else:
                return redirect("users:tutor_preference")
        context = {
            'user_profile_form': user_profile_form,
            'tutor_form': tutor_form
        }
        return render(request, "users/user_tutor.html", context=context)


user_tutor_view = UserTutorView.as_view()


class UserTutorPreference(LoginRequiredMixin, View):
    @staticmethod
    def get_tutor_preference(request):
        try:
            tutor_preference = request.user.profile.tutor.preference
        except User.profile.RelatedObjectDoesNotExist:
            messages.info(request, _("Fill up this form to become a tutor."))
            return redirect("users:tutor")
        except Profile.tutor.RelatedObjectDoesNotExist:
            messages.info(request, _("Fill up this form to become a tutor."))
            return redirect("users:tutor")
        except Tutor.preference.RelatedObjectDoesNotExist:
            tutor_preference = None

        return tutor_preference

    def get(self, request):
        tutor_preference = self.get_tutor_preference(request)
        tutor_preference_form = TutorPreferenceForm(instance=tutor_preference)
        context = {
            'tutor_preference_form': tutor_preference_form
        }
        return render(request, "users/user_tutor_preference.html", context=context)

    def post(self, request):
        old_tutor_preference = self.get_tutor_preference(request)
        tutor_preference_form = TutorPreferenceForm(request.POST, instance=old_tutor_preference)
        if tutor_preference_form.is_valid():
            tutor_preference = tutor_preference_form.save(commit=False)
            tutor_preference.tutor = request.user.profile.tutor
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
    @staticmethod
    def get_profile_and_student(request):
        try:
            user_profile = request.user.profile
        except User.profile.RelatedObjectDoesNotExist:
            user_profile = None

        if user_profile:
            try:
                student = user_profile.student
            except Profile.student.RelatedObjectDoesNotExist:
                student = None
        else:
            student = None

        return user_profile, student

    def get(self, request):

        user_profile, student = self.get_profile_and_student(request)
        student_form = StudentForm(instance=student)
        user_profile_form = ProfileForm(instance=user_profile)
        context = {
            'user_profile_form': user_profile_form,
            'student_form': student_form
        }
        return render(request, "users/user_student.html", context=context)

    def post(self, request):
        old_user_profile, old_student = self.get_profile_and_student(request)
        user_profile_form = ProfileForm(request.POST, instance=old_user_profile)
        student_form = StudentForm(request.POST, instance=old_student)
        if user_profile_form.is_valid() and student_form.is_valid():

            user_profile = user_profile_form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            student = student_form.save(commit=False)
            student.user_profile = user_profile
            student.save()
            if student:
                return redirect("users:student")

        context = {
            'user_profile_form': user_profile_form,
            'student_form': student_form
        }
        return render(request, "users/user_student.html", context=context)


user_student_view = UserStudentView.as_view()


class UserTuitionListView(LoginRequiredMixin, View):
    def get(self, request):
        tuition_list = Tuition.objects.filter(tutor=request.user.profile.tutor)
        context = {
            'tuition_list': tuition_list,
        }
        return render(request, "users/user_tuition_list.html", context=context)


user_tuition_list_view = UserTuitionListView.as_view()


class UserCreateTuition(LoginRequiredMixin, View):
    def get(self, request, tuition_id):
        # get old coupon data for edit view
        if tuition_id is not None:
            tuition = get_object_or_404(Tuition, pk=tuition_id, student__user_profile=request.user.profile)
        else:
            tuition = None
        tuition_form = TuitionForm(instance=tuition)
        context = {'tuition_form': tuition_form,
                   'tuition_id': tuition_id
                   }

        return render(request, "users/user_tuition.html", context=context)

    def post(self, request, tuition_id):
        """

        :param request:
        :param tuition_id:
        :return:
        """
        # changing success message for add and edit template
        if tuition_id is None:
            old_tuition = None
            message = _("New tuition added successfully!")
        else:
            old_tuition = get_object_or_404(Tuition, pk=tuition_id, student__user_profile=request.user.profile)
            message = _("Tuition updated successfully!")

        tuition_form = TuitionForm(request.POST, instance=old_tuition)

        if tuition_form.is_valid():
            tuition = tuition_form.save(commit=False)
            tuition.student = request.user.profile.student
            tuition.save()
            new_subjects = tuition_form.cleaned_data['subject']
            for subject in new_subjects:
                tuition.subject.add(subject)
            old_subjects = Subject.objects.filter(tuition=tuition)
            for subject in old_subjects:
                if subject not in new_subjects:
                    tuition.subject.remove(subject)

            messages.success(request, message)
            # redirect to edit page
            return redirect("users:edit_tuition", tuition_id=tuition.pk)

        context = {'tuition_form': tuition_form,
                   'tuition_id': tuition_id
                   }

        return render(request, 'users/user_tuition.html', context=context)


user_create_tuition_view = UserCreateTuition.as_view()
#
#
# class UserTuitionView(LoginRequiredMixin, View):
#     @staticmethod
#     def get_profile_and_student(request):
#         try:
#             user_profile = request.user.profile
#         except User.profile.RelatedObjectDoesNotExist:
#             user_profile = None
#
#         if user_profile:
#             try:
#                 student = user_profile.student
#             except Profile.student.RelatedObjectDoesNotExist:
#                 student = None
#         else:
#             student = None
#
#         return user_profile, student
#
#     def get(self, request):
#
#         user_profile, student = self.get_profile_and_student(request)
#         student_form = StudentForm(instance=student)
#         user_profile_form = ProfileForm(instance=user_profile)
#         context = {
#             'user_profile_form': user_profile_form,
#             'student_form': student_form
#         }
#         return render(request, "users/user_student.html", context=context)
#
#     def post(self, request):
#         old_user_profile, old_student = self.get_profile_and_student(request)
#         user_profile_form = ProfileForm(request.POST, instance=old_user_profile)
#         student_form = StudentForm(request.POST, instance=old_student)
#         if user_profile_form.is_valid() and student_form.is_valid():
#
#             user_profile = user_profile_form.save(commit=False)
#             user_profile.user = request.user
#             user_profile.save()
#
#             student = student_form.save(commit=False)
#             student.user_profile = user_profile
#             student.save()
#             if student:
#                 return redirect("users:student")
#
#         context = {
#             'user_profile_form': user_profile_form,
#             'student_form': student_form
#         }
#         return render(request, "users/user_student.html", context=context)
#
#
# user_student_view = UserStudentView.as_view()

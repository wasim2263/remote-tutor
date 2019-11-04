from django.urls import path

from .views import (user_redirect_view, user_update_view, user_detail_view, user_tutor_view,
                    user_tutor_preference_view, user_student_view, user_tuition_list_view,
                    user_create_tuition_view)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("~tutor/edit/", view=user_tutor_view, name="tutor"),
    path("~student/edit/", view=user_student_view, name="student"),
    path("~tutor/preference/", view=user_tutor_preference_view, name="tutor_preference"),
    path("~tuition/list/", view=user_tuition_list_view, name="tuition_list"),
    path("~tuition/create/", view=user_create_tuition_view, kwargs={'tuition_id': None}, name="create_tuition"),
    path("~tuition/<tuition_id>/edit/", view=user_create_tuition_view, name="edit_tuition"),
]

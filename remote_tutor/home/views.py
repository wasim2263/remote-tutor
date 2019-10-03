from django.shortcuts import render

# Create your views here.
from django.views import View

from remote_tutor.tutor.models import Tutor


class HomeView(View):
    def get(self, request):
        tutors = Tutor.objects.filter().select_related('preference', 'user', 'school', 'college', 'university',
                                                       'department')
        context = {
            'tutors': tutors
        }
        return render(request, 'home/home.html', context=context)


home_view = HomeView.as_view()

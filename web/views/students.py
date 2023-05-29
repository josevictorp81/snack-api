from django.views.generic import ListView
# from braces.views import SuperuserRequiredMixin

from core.models import Child


class StudentListView(ListView):
    template_name = 'student_list.html'
    context_object_name = 'student_list'
    model = Child
    paginate_by = 25

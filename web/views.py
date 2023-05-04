from django.views.generic import TemplateView

class OrderListView(TemplateView):
    template_name = 'order_list.html'

class StudentListView(TemplateView):
    template_name = 'student_list.html'

class SnackListView(TemplateView):
    template_name = 'snack_list.html'

class ClassListView(TemplateView):
    template_name = 'class_list.html'

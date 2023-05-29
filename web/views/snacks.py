from django.views.generic import ListView
# from braces.views import SuperuserRequiredMixin

from core.models import Snack


class SnackListView(ListView):
    context_object_name = 'snack_list'
    template_name = 'snack_list.html'
    model = Snack
    paginate_by = 25

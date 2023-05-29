from django.views.generic import ListView
# from braces.views import SuperuserRequiredMixin

from core.models import Order


class OrderListView(ListView):
    model = Order
    context_object_name = 'order_list'
    template_name = 'order_list.html'
    paginate_by = 15

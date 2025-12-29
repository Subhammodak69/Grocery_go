from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from E_mart.constants.decorators import delivery_worker_required
from E_mart.services import delivery_service


@method_decorator(delivery_worker_required,name='dispatch')
class DeliveriesListView(View):
    def get(self, request):
        worker = delivery_service.get_delivery_worker_obj_by_user_id(request.user)
        deliveries = delivery_service.get_deliveries_by_deliveryPerson(worker)
        return render(request, 'delivery/deliveries.html',{'deliveries':deliveries})
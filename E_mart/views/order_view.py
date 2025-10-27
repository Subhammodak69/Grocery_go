from django.views import View
from django.shortcuts import render
from E_mart.services import product_service
from django.utils.decorators import method_decorator
from E_mart.constants.decorators import enduser_required
from django.views.decorators.csrf import csrf_exempt

@method_decorator(enduser_required, name= 'dispatch')
class ProductOrderSummary(View):
    def get(self, request):
        product_details_id = request.GET.get('product_details_id')
        quantity = request.GET.get('quantity')
        product_data = product_service.product_all_data_by_details_id(product_details_id)
        product_data.update({
            'quantity':quantity
        })
        summary_data = {
            'discount':'',
            'total':''
        }
        print(product_data)
        return render(request, 'enduser/singly_order_summary.html', {'data': product_data,'summary_data':summary_data})
from .models import Customer

def get_customer_by_external_id(external_id):
    try:
        return Customer.objects.get(external_id=external_id)
    except Customer.DoesNotExist:
        return None

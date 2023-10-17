from django.test import TestCase
from rest_framework.test import APIClient
from .models import Customer
from .services import create_customer, get_customer_balance

class CustomerTestCase(TestCase):
    def setUp(self):

        pass

    def test_create_customer(self):
        data = {
            "external_id": "test_customer",
            "status": 1,
            "score": 100.0,
        }
        create_customer(data)
        customer = Customer.objects.get(external_id="test_customer")
        self.assertEqual(customer.external_id, "test_customer")
        self.assertEqual(customer.status, 1)
        self.assertEqual(customer.score, 100.0)

    def test_get_customer_balance(self):
        customer_data = {
            "external_id": "test_customer",
            "status": 1,
            "score": 200.0,
        }
        create_customer(customer_data)

        balance = get_customer_balance("test_customer")
        self.assertEqual(balance["external_id"], "test_customer")
        self.assertEqual(balance["score"], 200.0)
        self.assertEqual(balance["available_amount"], 200.0)
        self.assertEqual(balance["total_debt"], 0)

    def test_customer_viewset_create(self):
        client = APIClient()
        data = {
            "external_id": "test_customer_viewset",
            "status": 1,
            "score": 300.0,
        }
        response = client.post('/api/v1/customer/', data, format='json')
        self.assertEqual(response.status_code, 201)
        customer = Customer.objects.get(external_id="test_customer_viewset")
        self.assertEqual(customer.external_id, "test_customer_viewset")
        self.assertEqual(customer.status, 1)
        self.assertEqual(customer.score, 300.0)

    def test_customer_viewset_get_balance(self):
        client = APIClient()
        customer_data = {
            "external_id": "test_customer_viewset_balance",
            "status": 1,
            "score": 400.0,
        }
        create_customer(customer_data)
        response = client.get('/api/v1/customer/test_customer_viewset_balance/balance/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["external_id"], "test_customer_viewset_balance")
        self.assertEqual(response.data["score"], 400.0)
        self.assertEqual(response.data["available_amount"], 400.0)
        self.assertEqual(response.data["total_debt"], 0)

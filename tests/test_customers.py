from app import create_app
from app.models import db, Customer
import unittest


class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
        })

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Create customer for login + tests
            customer = Customer(
                first_name="Test",
                last_name="User",
                email="test@test.com",
                password="password"
            )
            db.session.add(customer)
            db.session.commit()
            self.customer_id = customer.id

            # Login to get token
            login = self.client.post("/customers/login", json={
                "email": "test@test.com",
                "password": "password"
            })

            print(login.get_json())   # 👈 ADD THIS LINE
            self.token = login.get_json()["auth_token"]



        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_get_customers(self):
        response = self.client.get("/customers/", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_create_customer(self):
        response = self.client.post("/customers/", json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@test.com",
            "password": "password"
        })
        self.assertEqual(response.status_code, 201)

    def test_get_customer_not_found(self):
        response = self.client.get("/customers/999", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_update_customer(self):
        response = self.client.put(
            f"/customers/{self.customer_id}",
            json={
                "first_name": "Updated",
                "last_name": "Name",
                "email": "updated@test.com"
            },
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data["first_name"], "Updated")
        self.assertEqual(data["last_name"], "Name")
        self.assertEqual(data["email"], "updated@test.com")

    def test_delete_customer(self):
        response = self.client.delete(
            f"/customers/{self.customer_id}",
            headers=self.headers
        )
        self.assertEqual(response.status_code, 204)

    def test_login_customer(self):
        response = self.client.post("/customers/login", json={
            "email": "test@test.com",
            "password": "password"
        })
        self.assertEqual(response.status_code, 200)

    def test_login_customer_bad_password(self):
        response = self.client.post("/customers/login", json={
            "email": "test@test.com",
            "password": "wrong"
        })
        self.assertEqual(response.status_code, 401)

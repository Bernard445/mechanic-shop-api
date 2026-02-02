from app import create_app
from app.models import db, Vehicle, Customer
import unittest


class TestVehicle(unittest.TestCase):

    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
        })

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            customer = Customer(
                first_name="Test",
                last_name="User",
                email="test@test.com",
                password="password"
            )
            db.session.add(customer)
            db.session.commit()

            login = self.client.post("/customers/login", json={
                "email": "test@test.com",
                "password": "password"
            })
            self.token = login.get_json()["auth_token"]

            vehicle = Vehicle(
                vin="TESTVIN123",
                make="Toyota",
                model="Camry",
                year=2020,
                customer_id=customer.id
            )
            db.session.add(vehicle)
            db.session.commit()

            self.vehicle_id = vehicle.id
            self.customer_id = customer.id

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_get_vehicles(self):
        response = self.client.get(
            "/vehicles/",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 200)

    def test_create_vehicle(self):
        response = self.client.post(
            "/vehicles/",
            json={
                "vin": "VIN456",
                "make": "Honda",
                "model": "Civic",
                "year": 2021,
                "customer_id": self.customer_id
            },
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 201)

    def test_update_vehicle(self):
        response = self.client.put(
            f"/vehicles/{self.vehicle_id}",
            json={
                "make": "Updated",
                "model": "Car",
                "year": 2022
            },
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_vehicle(self):
        response = self.client.delete(
            f"/vehicles/{self.vehicle_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 204)

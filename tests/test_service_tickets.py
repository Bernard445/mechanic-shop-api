from app import create_app
from app.models import db, ServiceTicket, Customer, Vehicle
import unittest


class TestServiceTicket(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Create customer
            customer = Customer(
                first_name="Ticket",
                last_name="Guy",
                email="ticket@test.com",
                password="password"
            )
            db.session.add(customer)
            db.session.commit()

            # Login to get token
            login = self.client.post("/customers/login", json={
                "email": "ticket@test.com",
                "password": "password"
            })
            self.token = login.get_json()["auth_token"]


            # Create vehicle
            vehicle = Vehicle(
                make="Ford",
                model="Focus",
                year=2019,
                customer_id=customer.id
            )
            db.session.add(vehicle)
            db.session.commit()
            self.vehicle_id = vehicle.id

            # Create ticket
            ticket = ServiceTicket(
                description="Oil change",
                cost=100,
                vehicle_id=self.vehicle_id
            )
            db.session.add(ticket)
            db.session.commit()
            self.ticket_id = ticket.id

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_get_tickets(self):
        response = self.client.get(
            "/service-tickets/",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 200)

    def test_create_ticket(self):
        response = self.client.post(
            "/service-tickets/",
            json={
                "description": "Brakes",
                "cost": 200,
                "vehicle_id": self.vehicle_id
            },
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 201)

    def test_ticket_not_found(self):
        response = self.client.get(
            "/service-tickets/999",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 404)

    def test_edit_ticket(self):
        response = self.client.put(
            f"/service-tickets/{self.ticket_id}/edit",
            json={
                "add_ids": [],
                "remove_ids": []
            },
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_ticket_not_found(self):
        response = self.client.put(
            "/service-tickets/999/edit",
            json={
                "add_ids": [],
                "remove_ids": []
            },
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 404)

from app import create_app
from app.models import db, Mechanic, Customer
import unittest


class TestMechanic(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Create a customer (for login)
            customer = Customer(
                first_name="Test",
                last_name="User",
                email="test@test.com",
                password="password"
            )
            db.session.add(customer)
            db.session.commit()

        # Login to get token (outside context)
        login = self.client.post("/customers/login", json={
            "email": "test@test.com",
            "password": "password"
        })
        self.token = login.get_json()["auth_token"]


        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

        with self.app.app_context():
            # Create a mechanic
            mech = Mechanic(name="Bob")
            db.session.add(mech)
            db.session.commit()
            self.mechanic_id = mech.id

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_get_mechanics(self):
        response = self.client.get("/mechanics/", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_create_mechanic(self):
        response = self.client.post(
            "/mechanics/",
            json={"name": "Alice"},
            headers=self.headers
        )
        self.assertEqual(response.status_code, 201)

    def test_update_mechanic(self):
        response = self.client.put(
            f"/mechanics/{self.mechanic_id}",
            json={"name": "Updated Bob"},
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_mechanic(self):
        response = self.client.delete(
            f"/mechanics/{self.mechanic_id}",
            headers=self.headers
        )
        self.assertEqual(response.status_code, 204)

    def test_most_worked_mechanics(self):
        response = self.client.get(
            "/mechanics/most-worked",
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)

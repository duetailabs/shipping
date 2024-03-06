import unittest

from data_model import Package
from connect_connector import SessionMaker

from main import app

class TestPackage(unittest.TestCase):

    def setUp(self):
        self.session_maker = SessionMaker()

    def tearDown(self):
        self.session_maker.close()

    def test_get_package(self):
        """Test the `get_package()` function."""

        package = Package(
        product_id=11, # Ensure that the product_id different from the sample data
        height=10,
        width=10,
        depth=10,
        weight=10,
        special_handling_instructions="Fragile",
        )

        session = self.session_maker

        session.add(package)
        session.commit()

        response = app.test_client().get("/packages/11")

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.json,
            {
                "height": 10,
                "width": 10,
                "depth": 10,
                "weight": 10,
                "special_handling_instructions": "Fragile",
            },
        )

if __name__ == "__main__":
    unittest.main()

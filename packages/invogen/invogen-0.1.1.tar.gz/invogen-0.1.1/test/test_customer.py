"""Unit tests for the invogen.customer module."""
import unittest
from invogen.customer import Customer


class TestCustomer(unittest.TestCase):
    """Tests for the Customer class"""

    def setUp(self):
        self.customer = Customer()

    def test_customer_account_name(self):
        """Test Customer.account_name can set and get."""
        self.customer.account_name = "account name"
        self.assertEqual("account name", self.customer.account_name)

    def test_customer_name(self):
        """Test Customer.name can set and get."""
        self.customer.name = "name"
        self.assertEqual("name", self.customer.name)

    def test_customer_address(self):
        """Test Customer.address can set and get."""
        self.customer.address = ["Address 1", "Address 2"]
        self.assertEqual(["Address 1", "Address 2"], self.customer.address)

    def test_default_customer_number_is_zero(self):
        """Test the Customer.number is 0 if not set."""
        self.assertEqual(0, self.customer.number)

    def test_customer_number(self):
        """Test Customer.number can set and get."""
        self.customer.number = 13
        self.assertEqual(13, self.customer.number)

    def test_customer_number_is_not_int(self):
        """Test TypeError raised if Customer.number is not int."""
        with self.assertRaises(TypeError):
            self.customer.number = "13"

    def test_customer_info(self):
        """Test Customer.info returns correct dict"""
        customer = Customer("account name",
                            "name",
                            ["Address 1", "Address 2"],
                            13,)
        expected_info = {
            "account_name": "account name",
            "name": "name",
            "address": ["Address 1", "Address 2"],
            "number": 13
        }
        self.assertEqual(expected_info, customer.info)

    def test_customer_string(self):
        """Test string method works."""
        customer = Customer("Test", "Foobar ltd")
        self.assertEqual("Foobar ltd (Test)", str(customer))

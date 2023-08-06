"""Unit tests for the invogen.accounts module."""
import unittest
from invogen.accounts import User, Customer


class TestUser(unittest.TestCase):
    """Tests for the User class"""

    def setUp(self):
        self.user = User()

    def test_user_name(self):
        """Test User.name can set and get."""
        self.user.name = "username"
        self.assertEqual("username", self.user. name)

    def test_user_email(self):
        """Test User.email can set and get."""
        self.user.email = "username@example.com"
        self.assertEqual("username@example.com", self.user.email)

    def test_user_address(self):
        """Test User.address can set and get."""
        self.user.address = ["Address 1", "Address 2"]
        self.assertEqual(["Address 1", "Address 2"], self.user.address)

    def test_user_phone_number(self):
        """Test User.phone can set and get."""
        self.user.phone = "01234567890"
        self.assertEqual("01234567890", self.user.phone)

    def test_user_account_number(self):
        """Test User.account_number can set and get."""
        self.user.account_number = "012345"
        self.assertEqual("012345", self.user.account_number)

    def test_user_sort_code(self):
        """Test User.sort_code can set and get."""
        self.user.sort_code = "012345"
        self.assertEqual("012345", self.user.sort_code)

    def test_user_sort_code_accepts_formatted_input(self):
        """Test User.sort_code accepts a formatted code."""
        self.user.sort_code = "01-23-45"
        self.assertEqual("012345", self.user.sort_code)

    def test_user_info(self):
        """Test Customer.info returns correct dict"""
        user = User(
            name="username",
            email="name@example.com",
            address=["Address 1", "Address 2"],
            phone="01234 567890",
            account_number="123456",
            sort_code="123456",
        )
        expected_info = {
            "name": "username",
            "email": "name@example.com",
            "address": ["Address 1", "Address 2"],
            "phone": "01234 567890",
            "account_number": "123456",
            "sort_code": "123456",
        }
        self.assertEqual(expected_info, user.info)

    def test_user_string(self):
        """Test string method works."""
        user = User(name="Test")
        self.assertEqual("Test's account", str(user))

    def test_user_repr(self):
        """Test repr method works."""
        user = User(name="Test")
        self.assertEqual("<User Test>", repr(user))


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
        customer = Customer(
            account_name="account name",
            name="name",
            email="name@example.com",
            address=["Address 1", "Address 2"],
            phone="01234 567890",
            number=13,
        )
        expected_info = {
            "account_name": "account name",
            "email": "name@example.com",
            "address": ["Address 1", "Address 2"],
            "phone": "01234 567890",
            "name": "name",
            "number": 13,
        }
        self.assertEqual(expected_info, customer.info)

    def test_customer_string(self):
        """Test string method works."""
        customer = Customer(account_name="Test", name="Foobar ltd")
        self.assertEqual("Foobar ltd (Test)", str(customer))

    def test_customer_repr(self):
        """Test repr method works."""
        customer = Customer(account_name="Test", name="Foobar ltd")
        self.assertEqual("<Customer Foobar ltd (Test)>", repr(customer))

"""Unit tests for the invogen.invoice module."""
import unittest
from decimal import Decimal
from invogen.invoice import Invoice, InvoiceEntry
from invogen.accounts import Customer, User


class TestInvoice(unittest.TestCase):
    """Tests for the Invoice class"""

    def setUp(self):
        self.invoice = Invoice()

    def test_invoice_user(self):
        """Test Invoice.user can set and get."""
        user = User("test")
        invoice = Invoice(user=user)
        self.assertEqual(user, invoice.user)

    def test_invoice_customer(self):
        """Test Invoice.customer can set and get."""
        customer = Customer(name="test")
        invoice = Invoice(customer=customer)
        self.assertEqual(customer, invoice.customer)
    
    def test_invoice_increments_customer_number(self):
        """Test that the customer account number increments."""
        customer = Customer(number=3)
        invoice = Invoice(customer=customer)
        self.assertEqual(4, invoice.customer.number)

    def test_invoice_entries(self):
        """Test Invoice.add_entry works and entries can get."""
        entry_1 = InvoiceEntry("id 1")
        entry_2 = InvoiceEntry("id 2")
        self.invoice.add_entry(entry_1)
        self.invoice.add_entry(entry_2)
        self.assertEqual([entry_1, entry_2], self.invoice.entries)

    def test_invoice_init_entries(self):
        """Test Invoice can init with entries."""
        entry_1 = InvoiceEntry("id 1")
        entry_2 = InvoiceEntry("id 2")
        invoice = Invoice(entries=[entry_1, entry_2])
        self.assertEqual([entry_1, entry_2], invoice.entries)

    def test_invoice_shipping(self):
        """Test Invoice.shipping can set and get."""
        self.invoice.shipping = 5
        self.assertEqual(5, self.invoice.shipping)

    def test_invoice_shipping_is_decimal(self):
        """Test Invoice.shipping is a Decimal."""
        self.invoice.shipping = 5
        self.assertIsInstance(self.invoice.shipping, Decimal)

    def test_invoice_discount(self):
        """Test Invoice.discount can set and get."""
        self.invoice.discount = 9
        self.assertEqual(9, self.invoice.discount)

    def test_invoice_discount_is_decimal(self):
        """Test Invoice.discount is a Decimal."""
        self.invoice.discount = 9
        self.assertIsInstance(self.invoice.discount, Decimal)

    def test_get_sub_total_of_invoice(self):
        """Test Invoice.sub_total can get."""
        self.invoice.add_entry(InvoiceEntry(rate=3, quantity=4))
        self.invoice.add_entry(InvoiceEntry(rate=5, quantity=6))
        self.assertEqual(42, self.invoice.sub_total)

    def test_sub_total_is_decimal(self):
        """Test Invoice.sub_total is a Decimal."""
        self.invoice.add_entry(InvoiceEntry(rate=3, quantity=4))
        self.assertIsInstance(self.invoice.sub_total, Decimal)

    def test_get_total_of_invoice(self):
        """Test Invoice.total can get."""
        self.invoice.add_entry(InvoiceEntry(rate=3, quantity=4))
        self.invoice.add_entry(InvoiceEntry(rate=5, quantity=6))
        self.invoice.shipping = 5
        self.assertEqual(47, self.invoice.total)

    def test_total_is_decimal(self):
        """Test Invoice.total is a Decimal."""
        self.invoice.add_entry(InvoiceEntry(rate=3, quantity=4))
        self.assertIsInstance(self.invoice.total, Decimal)

    def test_invoice_str(self):
        """Test string method works."""
        invoice = Invoice(customer=Customer(account_name="Test",
                                            name="Foobar ltd"))
        invoice.add_entry(InvoiceEntry("123", "Some stuff", 3, 4))
        invoice.add_entry(InvoiceEntry("124", "Some other stuff", 3, 5))
        expected_str = "\n".join([
            "Invoice for Foobar ltd (Test)",
            "|   ID   |     Description      |   Rate   | Quantity |  Amount  |",
            "+--------+----------------------+----------+----------+----------+",
            "| 123    | Some stuff           |     3.00 |     4.00 |    12.00 |",
            "| 124    | Some other stuff     |     3.00 |     5.00 |    15.00 |",
            "+--------+----------------------+----------+----------+----------+",
            "                                             Sub-total:    27.00",
            "                                              Shipping:     0.00",
            "                                              Discount:     0.00",
            "                                           +---------------------+",
            "                                                 Total:    27.00"
        ])
        self.assertEqual(expected_str, str(invoice))

class TestInvoiceEntries(unittest.TestCase):
    """Tests for the InvoiceEntry class"""

    def test_invoice_entry_id(self):
        """Test InvoiceEntry.id_code can get."""
        entry = InvoiceEntry(id_code="entry id")
        self.assertEqual("entry id", entry.id_code)

    def test_invoice_entry_description(self):
        """Test InvoiceEntry.description can get."""
        entry = InvoiceEntry(description="entry description")
        self.assertEqual("entry description", entry.description)

    def test_invoice_entry_rate(self):
        """Test InvoiceEntry.rate can get."""
        entry = InvoiceEntry(rate=1)
        self.assertEqual(1, entry.rate)

    def test_empty_invoice_entry_rate_is_decimal(self):
        """Test InvoiceEntry.rate is a Decimal."""
        entry = InvoiceEntry()
        self.assertIsInstance(entry.rate, Decimal)

    def test_invoice_entry_rate_accepts_str(self):
        """Test InvoiceEntry.rate accepts string input."""
        _ = InvoiceEntry(rate="1")

    def test_invoice_entry_quantity(self):
        """Test InvoiceEntry.quntity can get."""
        entry = InvoiceEntry(quantity=2)
        self.assertEqual(2, entry.quantity)

    def test_empty_invoice_entry_quantity_is_decimal(self):
        """Test InvoiceEntry.quantity is a Decimal."""
        entry = InvoiceEntry()
        self.assertIsInstance(entry.quantity, Decimal)

    def test_invoice_entry_quantity_accepts_str(self):
        """Test InvoiceEntry.quantity accepts string input."""
        _ = InvoiceEntry(quantity="2")

    def test_empty_invoice_entry_amount_is_zero(self):
        """Test InvoiceEntry.amount is 0 for an empty entry."""
        entry = InvoiceEntry()
        self.assertEqual(0, entry.amount)

    def test_invoice_entry_amount(self):
        """Test InvoiceEntry.amount can get."""
        entry = InvoiceEntry(rate=3, quantity=4)
        self.assertEqual(12, entry.amount)

    def test_empty_invoice_entry_amount_is_decimal(self):
        """Test InvoiceEntry.amount is a Decimal for an empty entry."""
        entry = InvoiceEntry()
        self.assertIsInstance(entry.amount, Decimal)

    def test_invoice_entry_amount_is_decimal(self):
        """Test InvoiceEntry.amount is a Decimal."""
        entry = InvoiceEntry(rate=3, quantity=4)
        self.assertIsInstance(entry.amount, Decimal)

    def test_invoice_entry_info(self):
        """Test InvoiceEntry.info returns the correct dict."""
        entry = InvoiceEntry(id_code="entry id",
                             description="entry description",
                             rate=3,
                             quantity=4)
        expected_info = {"id_code": "entry id",
                         "description": "entry description",
                         "rate": Decimal("3.00"),
                         "quantity": Decimal("4"),
                         "amount": Decimal("12.00")}
        self.assertEqual(expected_info, entry.info)

    def test_invoice_entry_str(self):
        """Test string method works."""
        entry = InvoiceEntry(id_code="id123",
                             description="entry description",
                             rate=3,
                             quantity=4)
        expected_str = "\n".join([
            "|   ID   |     Description      |   Rate   | Quantity |  Amount  |",
            "+--------+----------------------+----------+----------+----------+",
            "| id123  | entry description    |     3.00 |     4.00 |    12.00 |"
        ])
        self.assertEqual(expected_str, str(entry))

    def test_invoice_entry_latex(self):
        """Test latex method works."""
        entry = InvoiceEntry(id_code="id123",
                             description="entry description",
                             rate=3,
                             quantity=4)
        expected_latex = "id123 & entry description & 3.00 & 4 & 12.00"
        self.assertEqual(expected_latex, entry.latex())

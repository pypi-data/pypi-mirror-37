"""
    invogen.invoice
    ---------------

    This module implements the invoice and entry objects.

    :copyright: © 2018 Samuel Searles-Bryant.
    :license: MIT, see LICENSE for more details.
"""
from decimal import Decimal, getcontext, ROUND_HALF_UP
import jinja2
import pkg_resources
from subprocess import run, DEVNULL
from os import remove
from invogen.accounts import User, Customer

# Decimal objects will round to 2dp
getcontext().rounding = ROUND_HALF_UP
TWOPLACES = Decimal("0.01")

latex_jinja_env = jinja2.Environment(
	block_start_string=r'\BLOCK{',
	block_end_string=r'}',
	variable_start_string=r'\VAR{',
	variable_end_string=r'}',
	comment_start_string=r'\#{',
	comment_end_string=r'}',
	line_statement_prefix=r'%%',
	line_comment_prefix=r'%#',
	trim_blocks=True,
	autoescape=False,
    loader=jinja2.PackageLoader(__name__, "templates")
)
template_filename = pkg_resources.resource_filename(__name__,
                                                    "templates/default.tex")


class Invoice:
    """An invoice object."""

    def __init__(self, user=User(), customer=Customer(), entries=[]):
        """
        Args:
            user (:obj:`User`, optional):
                The user account for the invoice.
                Defaults to a new instance of User.
            customer (:obj:`Customer`, optional):
                The customer account for the invoice.
                Defaults to a new instance of Customer.
            entries (:obj:`list` of :obj:`InvoiceEntry`, optional):
                The items on the invoice.
                Defaults to an empty list
        """
        self.user = user
        self.customer = customer
        self.entries = list(entries)
        self.shipping = Decimal("0.0")
        self.discount = Decimal("0.0")

    def __str__(self):
        lines = []
        lines.append("Invoice for {}".format(self.customer))

        l_head = "| {:^6} | {:^20} | {:^8} | {:^8} | {:^8} |"
        lines.append(l_head.format("ID",
                                   "Description",
                                   "Rate",
                                   "Quantity",
                                   "Amount"))

        l_fill = "+-{0:-^6}-+-{0:-^20}-+-{0:-^8}-+-{0:-^8}-+-{0:-^8}-+"
        lines.append(l_fill.format(""))

        l_entries = "| " + " | ".join(["{id_code:6}",
                                       "{description:20}",
                                       "{rate:8.2f}",
                                       "{quantity:8.2f}",
                                       "{amount:8.2f}"]) + " |"
        lines.append("\n".join([l_entries.format(**entry.info)
                                for entry in self.entries]))
        lines.append(l_fill.format(""))

        sub_t = "Sub-total: {invoice.sub_total:8.2f}".format(invoice=self)
        shipping = "Shipping: {invoice.shipping:8.2f}".format(invoice=self)
        disc = "Discount: {invoice.shipping:8.2f}".format(invoice=self)
        total = "Total: {invoice.total:8.2f}".format(invoice=self)
        l_totals = "{0:>64}"
        lines += [l_totals.format(line) for line in [sub_t,
                                                     shipping,
                                                     disc,
                                                    ]]
        l_sub_fill = "{:>66}".format("+{:-^21}+".format(""))
        lines.append(l_sub_fill)
        lines.append(l_totals.format(total))

        return "\n".join(lines)

    @property
    def user(self):
        """:obj:`User`: The user assigned to the invoice."""
        return self._user

    @user.setter
    def user(self, new_user):
        self._user = new_user

    @property
    def customer(self):
        """:obj:`Customer`: The customer assigned to the invoice."""
        return self._customer

    @customer.setter
    def customer(self, new_customer):
        new_customer.number += 1
        self._customer = new_customer

    @property
    def entries(self):
        """:obj:`list` of :obj:`InvoiceEntry`: The items on the invoice."""
        return self._entries

    @entries.setter
    def entries(self, new_entries):
        self._entries = new_entries

    @property
    def sub_total(self):
        """:obj:`decimal.Decimal`: The sum of the amounts of all items on the invoice."""
        sub_total = sum([entry.amount for entry in self.entries])
        return sub_total.quantize(TWOPLACES)

    @property
    def shipping(self):
        """:obj:`decimal.Decimal`: The shipping amount of the invoice."""
        return self._shipping.quantize(TWOPLACES)

    @shipping.setter
    def shipping(self, new_shipping):
        self._shipping = Decimal(new_shipping)

    @property
    def discount(self):
        """:obj:`decimal.Decimal`: The discount applied to the invoice."""
        return self._discount.quantize(TWOPLACES)

    @discount.setter
    def discount(self, new_discount):
        self._discount = Decimal(new_discount)

    @property
    def total(self):
        """:obj:`decimal.Decimal`: The total amount of the invoice."""
        total = self.sub_total + self.shipping - self.discount
        return total.quantize(TWOPLACES)

    def add_entry(self, new_entry):
        """Add an entry to the invoice.

        Args:
            new_entry (:obj:`InvoiceEntry`):
                The entry to be added to the invoice.
        """
        self.entries.append(new_entry)

    def pdf(self):
        """Generate a PDF of the invoice using LaTeX."""
        FILENAME = "invogen_temporary_LaTeX_file.tex"
        job_name = "invoice_{}-{:03d}".format(self.customer.account_name,
                                              self.customer.number)
        template = latex_jinja_env.get_template("default.tex")
        output = template.render(invoice=self,
                                 user=self.user,
                                 customer=self.customer)
        with open(FILENAME, "w") as f:
            f.write(output)
        run(["latexmk", "-pdf", "-jobname={}".format(job_name), FILENAME],
            stdout=DEVNULL, stderr=DEVNULL)
        run(["latexmk", "-jobname={}".format(job_name), "-c"],
            stdout=DEVNULL, stderr=DEVNULL)
        remove(FILENAME)


class InvoiceEntry:
    """An entry on an invoice."""

    def __init__(self, id_code="", description="", rate=0, quantity=0):
        """
        Args:
            id_code (:obj:`str`, optional): The ID of the entry.
                Defaults to None.
            description (:obj:`str`, optional): The description of the entry.
                Defaults to None.
            rate (:obj:`int`, :obj:`str`, or :obj:`Decimal`, optional):
                The rate of the entry (cost per item).
                Defaults to None.
            quantity (:obj:`int`, :obj:`str`, or :obj:`Decimal`, optional):
                The quantity of the entry.
                Defaults to None.
        """

        self._id_code = id_code
        self._description = description
        self._rate = Decimal(rate)
        self._quantity = Decimal(quantity)

    def __str__(self):
        lines = []
        l_head = "| {:^6} | {:^20} | {:^8} | {:^8} | {:^8} |"
        lines.append(l_head.format("ID",
                                   "Description",
                                   "Rate",
                                   "Quantity",
                                   "Amount"))

        l_fill = "+-{0:-^6}-+-{0:-^20}-+-{0:-^8}-+-{0:-^8}-+-{0:-^8}-+"
        lines.append(l_fill.format(""))
        l_entry = "| " + " | ".join(["{id_code:6}",
                                     "{description:20}",
                                     "{rate:8.2f}",
                                     "{quantity:8.2f}",
                                     "{amount:8.2f}"]) + " |"
        lines.append(l_entry.format(**self.info))
        return "\n".join(lines)

    @property
    def id_code(self):
        """str: The ID code of the entry."""
        return self._id_code

    @property
    def description(self):
        """str: The description of the entry."""
        return self._description

    @property
    def rate(self):
        """:obj:`decimal.Decimal`: The rate of the entry (cost per item)."""
        return self._rate.quantize(TWOPLACES)

    @property
    def quantity(self):
        """:obj:`decimal.Decimal`: The quantity of the entry."""
        return self._quantity

    @property
    def amount(self):
        """:obj:`decimal.Decimal`: The total amount of the entry."""
        total = self.rate * self.quantity
        return total.quantize(TWOPLACES)

    @property
    def info(self):
        """dict: The properties of the entry."""
        properties = [str(p) for p in dir(self)
                      if not p.startswith("_") and p != "info" and p != "latex"]
        info = {p: self.__getattribute__(p) for p in properties}
        return info

    def latex(self):
        """str: The entry information as a LaTeX tabular row."""
        return " & ".join([
            self.id_code,
            self.description,
            str(self.rate),
            str(self.quantity),
            str(self.amount),
        ])

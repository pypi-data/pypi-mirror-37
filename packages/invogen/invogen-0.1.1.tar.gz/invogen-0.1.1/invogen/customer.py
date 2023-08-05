"""
    invogen.customer
    ----------------

    This module implements the customer account object.

    :copyright: © 2018 Samuel Searles-Bryant.
    :license: MIT, see LICENSE for more details.
"""

class Customer:
    """A customer account object. Contains customer information."""

    def __init__(self, account_name="", name="", address=[""], number=0):
        """
        Args:
            account_name (:obj:`str`, optional):
                The account code for this customer.
            name (:obj:`str`, optional):
                The full name of the customer.
            address (:obj:`list` of :obj:`str`, optional):
                The customer's address, split into lines.
            number (:obj:`int`, optional):
                The number of invoices previously issued to this customer.
                Defaults to 0.
        """
        self._account_name = account_name
        self._name = name
        self._address = address
        self._number = number

    def __str__(self):
        return "{cust.name} ({cust.account_name})".format(cust=self)

    @property
    def account_name(self):
        """str: The account code for the customer account."""
        return self._account_name

    @account_name.setter
    def account_name(self, new_account_name):
        self._account_name = new_account_name

    @property
    def name(self):
        """str: The full name of the customer."""
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def address(self):
        """str: The address of the customer."""
        return self._address

    @address.setter
    def address(self, new_address):
        self._address = new_address

    @property
    def number(self):
        """int: The number of invoices previously issued to this customer"""
        return self._number

    @number.setter
    def number(self, new_number):
        assert new_number >= 0, "Account invoice number cannot be less than 0"
        self._number = new_number

    @property
    def info(self):
        """dict: The properties of the customer account"""
        properties = [str(p) for p in dir(self)\
                      if not p.startswith("_") and p != "info"
                     ]
        info = {p: self.__getattribute__(p) for p in properties}
        return info

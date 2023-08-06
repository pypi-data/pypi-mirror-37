"""
    invogen.accounts
    ----------------

    This module implements the customer and user account objects.

    :copyright: © 2018 Samuel Searles-Bryant.
    :license: MIT, see LICENSE for more details.
"""

class Account:
    """An account object. Contains account information."""

    def __init__(self, name="", email="", phone="", address=[]):
        """
        Args:
            name (:obj:`str`, optional):
                The account's name.
            email (:obj:`str`, optional):
                The account's email address.
            phone (:obj:`str`, optional):
                The account's phone number (formatted)
            address (:obj:`list` of :obj:`str`, optional):
                The account's address, split into lines.
        """
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

    def __str__(self):
        return "{u.name}'s account".format(u=self)

    def __repr__(self):
        return "<Account {u.name}>".format(u=self)

    @property
    def name(self):
        """str: The name of the account holder."""
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def email(self):
        """str: The email address of the account holder."""
        return self._email

    @email.setter
    def email(self, new_email):
        self._email = new_email

    @property
    def phone(self):
        """str: The phone number of the account holder."""
        return self._phone

    @phone.setter
    def phone(self, new_phone):
        self._phone = new_phone

    @property
    def address(self):
        """:obj:`list` of :obj:`str`: The address of the account holder."""
        return self._address

    @address.setter
    def address(self, new_address):
        self._address = new_address

    @property
    def info(self):
        """dict: The properties of the customer account"""
        properties = [str(p) for p in dir(self)
                      if not p.startswith("_") and p != "info"
                      ]
        info = {p: self.__getattribute__(p) for p in properties}
        return info


class User(Account):
    """A user account object. Contains user information."""

    def __init__(self, name="",
                       email="",
                       phone="",
                       address=[],
                       account_number="",
                       sort_code=""):
        """
        Args:
            name (:obj:`str`, optional):
                The user's name.
            email (:obj:`str`, optional):
                The user's email address.
            phone (:obj:`str`, optional):
                The user's phone number (formatted)
            address (:obj:`list` of :obj:`str`, optional):
                The user's address, split into lines.
            account_number (:obj:`str`, optional):
                The user's bank account number.
            sort_code (:obj:`str`, optional):
                The user's bank account sort-code. 
        """
        super().__init__(name=name, email=email, phone=phone, address=address)
        self.account_number = account_number
        self.sort_code = sort_code

    def __repr__(self):
        return "<User {u.name}>".format(u=self)

    @property
    def account_number(self):
        """str: The bank account number of the user."""
        return self._account_number

    @account_number.setter
    def account_number(self, new_account_number):
        self._account_number = new_account_number

    @property
    def sort_code(self):
        """str: The bank account sort-code of the user."""
        return self._sort_code

    @sort_code.setter
    def sort_code(self, new_code):
        new_code = "".join(c for c in new_code if c.isdigit())
        self._sort_code = new_code
        

class Customer(Account):
    """A customer account object. Contains customer information."""

    def __init__(self, name="",
                       email="",
                       phone="",
                       address=[],
                       account_name="",
                       number=0):
        """
        Args:
            name (:obj:`str`, optional):
                The user's name.
            email (:obj:`str`, optional):
                The user's email address.
            phone (:obj:`str`, optional):
                The user's phone number (formatted)
            address (:obj:`list` of :obj:`str`, optional):
                The user's address, split into lines.
            account_name (:obj:`str`, optional):
                The account code for this customer.
            number (:obj:`int`, optional):
                The number of invoices previously issued to this customer.
                Defaults to 0.
        """
        super().__init__(name=name, email=email, phone=phone, address=address)
        self.account_name = account_name
        self.number = number

    def __str__(self):
        return "{cust.name} ({cust.account_name})".format(cust=self)
    
    def __repr__(self):
        return "<Customer {cust.name} ({cust.account_name})>".format(cust=self)

    @property
    def account_name(self):
        """str: The account code for the customer account."""
        return self._account_name

    @account_name.setter
    def account_name(self, new_account_name):
        self._account_name = new_account_name

    @property
    def number(self):
        """int: The number of invoices previously issued to this customer"""
        return self._number

    @number.setter
    def number(self, new_number):
        assert new_number >= 0, "Account invoice number cannot be less than 0"
        self._number = new_number

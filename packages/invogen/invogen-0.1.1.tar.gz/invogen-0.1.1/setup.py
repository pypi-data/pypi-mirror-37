"""
InvoGen
=======

InvoGen is a package for generating beautiful invoices with Python and LaTeX.

Instructions
------------

InvoGen is easy to use! In the command prompt or in a file type:

.. code:: python

    from invogen import *

    foobar_inc = Customer("test", name="Foobar Inc.")
    invoice = Invoice(foobar_inc)
    invoice.add_entry(InvoiceEntry(
        id_code="Test01",
        description="Some entry item",
        rate=5,
        quantity=1,
    ))
    invoice.shipping = 3
    print(invoice)

You should see a printout of your invoice like this:

.. code::

    Invoice for Foobar Inc. (test)
    |   ID   |     Description      |   Rate   | Quantity |  Amount  |
    +--------+----------------------+----------+----------+----------+
    | Test01 | Some entry item      |     5.00 |     1.00 |     5.00 |
    +--------+----------------------+----------+----------+----------+
                                                 Sub-total:     5.00
                                                  Shipping:     3.00
                                                  Discount:     3.00
                                               +---------------------+
                                                     Total:     8.00

Links
-----

* `Documentation <https://samueljsb.co.uk/InvoGen>`_
* `GitHub <https://github.com/samueljsb/InvoGen>`_
"""
from setuptools import setup

setup(
    name="invogen",
    version="0.1.1",
    description="",
    long_description=__doc__,
    author="Samuel Searles-Bryant",
    author_email="devel@samueljsb.co.uk",
    url="https://github.com/samueljsb/InvoGen",
    license="MIT",
    packages=[
        "invogen",
    ],
    install_requires=[
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",

    ],
)

__author__ = "Samuel Searles-Bryant"

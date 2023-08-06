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

To generate a PDF invoice using LaTeX, use

.. code::

    invoice.pdf()

Links
-----

* `Documentation <https://samueljsb.co.uk/InvoGen>`_
* `GitHub <https://github.com/samueljsb/InvoGen>`_
"""
from setuptools import setup

setup(
    name="invogen",
    version="0.2.0",
    description="",
    long_description=__doc__,
    author="Samuel Searles-Bryant",
    author_email="devel@samueljsb.co.uk",
    url="https://github.com/samueljsb/InvoGen",
    license="MIT",
    packages=[
        "invogen",
    ],
    include_package_data=True,
    install_requires=[
        "Jinja2>=2.10",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    project_urls={
        "Documentation": "https://invogen.readthedocs.io",
        "Bug Reports": "https://github.com/samueljsb/InvoGen/issues",
    },
)

__author__ = "Samuel Searles-Bryant"

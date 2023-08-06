[![PyPI](https://img.shields.io/pypi/v/invogen.svg)](https://pypi.org/project/invogen/)
[![GitHub](https://img.shields.io/github/license/samueljsb/InvoGen.svg)](#license)
[![Travis (.org) branch](https://img.shields.io/travis/samueljsb/InvoGen/master.svg)](https://travis-ci.org/samueljsb/InvoGen)
[![Coverage Status](https://coveralls.io/repos/github/samueljsb/InvoGen/badge.svg?branch=master)](https://coveralls.io/github/samueljsb/InvoGen?branch=master)
[![Build The Docs](https://readthedocs.org/projects/invogen/badge/?version=latest)](https://invogen.readthedocs.io/en/latest/?badge=latest)

InvoGen is a package to generate beautiful invoices with LaTeX.

## Getting Started ##

To install InvoGen, simply run

```bash
pip install invogen
```

If you wish to work on developing InvoGen then you will also need to install the packages used for development with

```bash
pip install -r requirements.txt
```

## Using InvoGen ##

InvoGen is easy to use! In the command prompt or in a file type:

```python
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
```

You should see a printout of your invoice like this:

```
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
```

To generate a PDF invoice using LaTeX, use

```
invoice.pdf()
```

## Documentation ##

Documentation can be found on [Read the Docs](https://invogen.readthedocs.io)

The docs are built with Sphinx and autodoc.
To build the docs as html yourself, use

```bash
make docs
```

or, from the `/docs` folder,

```bash
make html
```

To use Sphinx to generate the docs in some other format (_e.g._ LaTeX, JSON, man, _etc._), from the `/docs` folder use

```bash
make
```
for a list of options.

## Testing ##

The tests are in `/test`.
To run the tests with coverage, use

```bash
make test
```

To run only the tests, use

```bash
python -m unittest discover
```

## Authors ##

* Sam Searles-Bryant - [website](https://samueljsb.co.uk)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

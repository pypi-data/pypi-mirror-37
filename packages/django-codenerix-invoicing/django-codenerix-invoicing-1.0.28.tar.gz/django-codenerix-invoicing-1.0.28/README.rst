==========================
django-codenerix-invoicing
==========================

Codenerix Invoicing is a module that enables `CODENERIX.com <http://www.codenerix.com/>`_  to manage bills.

.. image:: http://www.codenerix.com/wp-content/uploads/2018/05/codenerix.png
    :target: http://www.codenerix.com
    :alt: Try our demo with Codenerix Cloud

****
Demo
****

Coming soon...

**********
Quickstart
**********

1. Install this package::

    For python 2: sudo pip2 install django-codenerix-invoicing
    For python 3: sudo pip3 install django-codenerix-invoicing

2. Add "codenerix_extensions", "codenerix_products", "codenerix_storages" and "codenerix_invoicing" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'codenerix_extensions',
        'codenerix_products',
        'codenerix_storages',
        'codenerix_invoicing',
    ]

3. Add the param in setting::

    CDNX_INVOICING_URL_COMMON = 'invoicing'
    CDNX_INVOICING_URL_PURCHASES = 'purchases'
    CDNX_INVOICING_URL_SALES = 'sales'

    CDNX_INVOICING_LOGICAL_DELETION = True  # Mark registers as 'removed', but it doesn't really delete them.
    
    # Code format
    CDNX_INVOICING_CODE_FORMAT_BUDGET = 'B{year}{day}{month}-{hour}{minute}-{serial}-{pk}'
    CDNX_INVOICING_CODE_FORMAT_WISHLIST = 'W{year}{day}{month}-{hour}{minute}-{serial}-{pk}'
    CDNX_INVOICING_CODE_FORMAT_SHOPPINGCART = 'S{year}{day}{month}-{hour}{minute}-{serial}-{pk}'
    CDNX_INVOICING_CODE_FORMAT_ORDER = 'O{year}{day}{month}-{hour}{minute}-{serial}-{pk}'
    CDNX_INVOICING_CODE_FORMAT_ALBARAN = 'A{year}{day}{month}-{hour}{minute}-{serial}-{pk}'
    CDNX_INVOICING_CODE_FORMAT_TICKET = 'T{year}{day}{month}-{hour}{minute}-{serial}-{pk}'
    CDNX_INVOICING_CODE_FORMAT_TICKETRECTIFICATION = 'TR{year}{day}{month}-{hour}{minute}-{serial}-{pk}'
    CDNX_INVOICING_CODE_FORMAT_INVOICE = 'I{year}{day}{month}-{hour}{minute}-{serial}-{pk}'
    CDNX_INVOICING_CODE_FORMAT_INVOICERECTIFCATION = 'IT{year}{day}{month}-{hour}{minute}-{serial}-{pk}'

4. Since Codenerix Invoicing is a library, you only need to import its parts into your project and use them.

*************
Documentation
*************

Coming soon... do you help us? `Codenerix <http://www.codenerix.com/>`_

*******
Credits
*******

This project has been possible thanks to `Centrologic <http://www.centrologic.com/>`_.

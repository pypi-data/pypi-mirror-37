=======
api-orm
=======

Interact with API endpoints as Python objects and manage resources in an ORMy way

Installation
============

Python version supported: 3.6+

.. code-block::

    pip install api-orm


About
=====

We have written many small clients to different APIs. It usually becomes a
couple of functions like:

.. code-block:: python

    client.get_customers()
    client.new_customer()
    # etc

When writing our client for our accounting API we wanted a more declarative way
of accessing our data. Also the API supported OData which allows for filtering
on all parameters. This made request look more like database access than
simple REST endpoints. So we wanted an interface more like a database ORM.

We use django a lot so we would like something we are used to.

This library is an attempt to extract the ORM parts of our Visma client so that
we can reuse the framework for a bunch of other API clients.

We want an api very alike the Django ORM:

.. code-block:: python

    all_customers = Customer.api.all()
    a = Customer(**customer_data)
    a.save()

    some_customers = Customer.api.filter(name='Dave').exclude(invoice_postal_code__startswith='25')



Before we have to write alot of custom validation but in this framework we use
the awesome serializer library marshmallow to transform python objects to
HTTP-request data and back. This gives us a declarative way of defining our
models and it comes included with validation of schemas and fields.
There are also tools available to generate models from and API specification
which greatly reduces the implementation time.
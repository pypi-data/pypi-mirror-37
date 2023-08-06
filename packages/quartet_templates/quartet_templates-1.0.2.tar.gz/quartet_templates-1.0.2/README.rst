QU4RTET TEMPLATES
=============

.. image:: https://gitlab.com/serial-lab/quartet_templates/badges/master/pipeline.svg
        :target: https://gitlab.com/serial-lab/quartet_templates/commits/master

.. image:: https://gitlab.com/serial-lab/quartet_templates/badges/master/coverage.svg
        :target: https://gitlab.com/serial-lab/quartet_templates/pipelines


The quartet_templates python package is a Django app that
contains database models necessary to create and edit templates
that are used in various way by the application (Number Range Requests with list-based regions, for instance.)


Quickstart
----------

Install QU4RTET TEMPLATES
---------------------

.. code-block:: text

    pip install quartet_templates


Add it to your `INSTALLED_APPS`:

.. code-block:: text

    INSTALLED_APPS = (
        ...
        'quartet_templates',
        ...
    )


Run the migrations in your QU4RTET directory:

.. code-block:: text

     python manage.py migrate quartet_templates


Add quartet_templates URL patterns:

.. code-block:: text


    urlpatterns = [
        ...
        url(r'^templates/', include('quartet_templates.urls')),
        ...
    ]

Running The Unit Tests
----------------------

.. code-block:: text

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ python runtests.py


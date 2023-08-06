===============
django-functest
===============

.. image:: https://travis-ci.org/django-functest/django-functest.png?branch=master
   :target: https://travis-ci.org/django-functest/django-functest

.. image:: https://coveralls.io/repos/django-functest/django-functest/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/django-functest/django-functest?branch=master

.. image:: https://readthedocs.org/projects/django-functest/badge/?version=latest
   :target: https://django-functest.readthedocs.org/en/latest/


Helpers for creating high-level functional tests in Django, with a unified API
for WebTest and Selenium tests.

Documentation
-------------

The full documentation is at https://django-functest.readthedocs.org.

Installation
------------

::

   pip install django-functest

See also the `dependencies documentation
<http://django-functest.readthedocs.io/en/latest/installation.html#dependencies>`_
for important compatibility information.

Features
--------

* A simplified API for writing functional tests in Django (tests that check the
  behaviour of entire views, or sets of views, e.g. a checkout process).

* A unified API that abstracts over both `WebTest
  <http://webtest.pythonpaste.org/en/latest/>`_ and `Selenium
  <https://pypi.python.org/pypi/selenium>`_ - write two tests at once!

* Many of the gotchas and difficulties of using WebTest and Selenium ironed out
  for you.

* Well tested - as well as its own test suite, which is run against Firefox
  and Chrome, it is also used by `Wolf & Badger
  <https://www.wolfandbadger.com/>`_ for tests covering many business critical
  functionalities.

Typical usage
-------------

In your tests.py::

    from django.test import LiveServerTestCase, TestCase
    from django_functest import FuncWebTestMixin, FuncSeleniumMixin, FuncBaseMixin

    class ContactTestBase(FuncBaseMixin):
        # Abstract class, doesn't inherit from TestCase

        def test_contact_form(self):
            self.get_url('contact_form')
            self.fill({'#id_name': 'Joe',
                       '#id_message': 'Hello'})
            self.submit('input[type=submit]')
            self.assertTextPresent("Thanks for your message")

     class ContactWebTest(ContactTestBase, FuncWebTestMixin, TestCase):
         pass

     class ContactSeleniumTest(ContactTestBase, FuncSeleniumMixin, LiveServerTestCase):
         pass

In this way, you can write a single test with a high-level API, and run it in
two ways - using a fast, WSGI-based method which emulates typical HTTP usage of a
browser, and using a full browser that actually executes Javascript (if present)
etc.

Under the hood, the WSGI-based method uses and builds upon `WebTest
<http://webtest.pythonpaste.org/en/latest/>`_ and `django-webtest
<https://pypi.python.org/pypi/django-webtest>`_.

django-functest provides its functionality as mixins, so that you can have your
own base class for tests.

Contributing and tests
----------------------

See CONTRIBUTING.rst for information about running the test suite and
contributing to django-functest.

Credits
-------

This library was built by developers at `Wolf & Badger
<https://www.wolfandbadger.com/>`_, released with the kind permission of that
company.

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage

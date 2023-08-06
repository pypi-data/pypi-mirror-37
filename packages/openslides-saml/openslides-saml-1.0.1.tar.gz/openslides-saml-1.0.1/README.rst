============================
 OpenSlides SAML Plugin
============================

Overview
========

This plugin for OpenSlides provides a login via a SAML single sign on
service.


Requirements
============

* `OpenSlides 2.2|2.3 <http://openslides.org/>`_
* `python3-saml (>= 1.3.0) <https://pypi.python.org/pypi/python3-saml/1.3.0>`_

Note: python3-saml needs thy python package `xmlsec <https://pypi.python.org/pypi/xmlsec/1.3.3>`_ which depends on `libxml2 <http://xmlsoft.org/>`_. Those packages need to be installed on a Debian-like system::

    $ apt-get install libxml2-dev libxmlsec1-dev libxmlsec1-openssl pkg-config

For more information about other operating systems or distributions visit http://pythonhosted.org/xmlsec/install.html.


Install
=======

This is only an example instruction to install the plugin on GNU/Linux. It
can also be installed as any other python package and on other platforms,
e. g. on Windows.

Change to a new directory::

    $ cd
    $ mkdir OpenSlides
    $ cd OpenSlides

Setup and activate a virtual environment and install OpenSlides and the
plugin in it::

    $ python -m venv .venv
    $ source .venv/bin/activate
    $ pip install openslides-saml

Start OpenSlides::

    $ openslides


Configuration
=============

Before the first start this line needs to be added to the ``settings.py``::

    SETTINGS_FILEPATH = __file__

If this line isn't there, the plugin will remind you :).

On startup of OpenSlides the ``saml_settings.json`` is created in the settings folder if
it does not exist. To force creating this file run::

    $ python manage.py create-saml-settings [--dir /<path to custom settings dir>/]

The path has to match with the settings path OpenSlides is started with.

For the first part in the settings file refer to `python3-saml settings documentation
<https://github.com/onelogin/python3-saml#settings>`_. All settings described there are
merged into the ``saml_settings.json``. Also note the ``README`` file in the ``certs``
folder next to the ``saml_settings.json``.

General Settings
----------------
Here you can provide a custom text for the SAML login button. The `changePasswordUrl`
redirects the user to the given URL when click on `Change password` in the OpenSlides user
menu.

Attributes
----------

The identity provider sends attributes to the plugin if a user sucessfully logged in. To
map these attributes to attributes of OpenSlides users, the section ``attributeMapping``
exists. The structure is like this::

    "attributeMapping: {
        "attributeFromIDP": ["attributeOpenSlidesUser", <used for lookup>],
        "anotherAttributeFromIDP": ["anotherAttributeOpenSlidesUser", <used for lookup>]
    }

All available OpenSlides user attributes are:

- ``username``: Has to be unique. Identifies the user.
- ``first_name``: The user's first name.
- ``last_name``: The user's last name.
- ``title``: The title of the user, e.g. "Dr.".
- ``email``: The user's email addreess.
- ``structure_level``: The structure level.
- ``number``: The participant number. This field is not unique.
- ``about_me``: A free text field.
- ``is_active``, ``is_present``, ``is_committee``: Boolean flags.

To get detailed information see the `models.py
<https://github.com/OpenSlides/OpenSlides/blob/master/openslides/users/models.py>`_.

The ``<used for lookup>`` has either to be ``true`` or ``false``. All attributes with this
value being true are used to search for an existing user. If the user is found, the user gets
updated with all changed values and used to log in. If the user is not found, it will be
created with all values given. Try to choose unique attributes (e.g. the username),
attributes you are sure about to be unique (e.g. maybe the number) or use a combination of
attributes.

Requests
--------

The metadata and requests are prepared for saml, e.g. the port number is needed. If not specified all these values are taken from the requests meta information:

- ``https``: Either ``on`` or ``off``.
- ``http_host``: The hostname.
- ``script_name``: The aquivalent to ``PATH_INFO`` in the meta values.
- ``server_port``: The port listen by the server.

These values may be false, because OpenSlides runs on port 8000 behind a webserver
redirecting the traffic from port 80 to port 8000. In the section ``requestSettings`` you
can set these values to overwrite the values get in the meta information.


Development
===========

To contribute to this plugin please create your own fork and work there in a branch
different to ``master``. Clone your fork, create a virtual environment and make a link
into a development checkout from OpenSlides (refer to `this guide
<https://github.com/OpenSlides/OpenSlides/blob/master/DEVELOPMENT.rst>`_)::

    $ ln -s /<path to this plugin>/openslides_saml /<path to os>/

You just need to add ``'openslides_saml'`` to your ``settings.py`` to enable this plugin.

For codestyle currently ``flake8`` and ``isort`` are checking the code. To install them
run a ``pip install -r requirements.txt``. Feel free to add unit or integration testing.

Happy contribution :)


License and authors
===================

This plugin is Free/Libre Open Source Software and distributed under the
MIT License, see LICENSE file. The authors are mentioned in the AUTHORS file.


Changelog
=========

Version 1.0.1 (2018-10-19)
--------------------------
* Support for OpenSlides 2.3


Version 1.0 (2018-06-22)
------------------------
* Initial release. Please read the README for every setting and
  possibility for customization.
* Support for OpenSlides 2.2

==========
pyKeyring
==========

.. |Build Status| image:: https://img.shields.io/travis/gabrielperes97/pyKeyring.svg   
    :alt: Travis (.org)   
    :target: https://travis-ci.org/gabrielperes97/pyKeyring

.. |pypi version| image:: https://img.shields.io/pypi/v/pyKeyring.svg
   :target: https://pypi.python.org/pypi/pykeyring/

.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/pyKeyring.svg
   :alt: PyPI - Python Version
   :target: https://pypi.python.org/pypi/pykeyring/

.. |GitHub license| image:: https://img.shields.io/github/license/gabrielperes97/pyKeyring.svg
   :target: https://github.com/gabrielperes97/pyKeyring/blob/master/LICENSE

|Build Status| |pypi version| |PyPI pyversions| |GitHub license|

A simple and secure tool to store passwords

Introdution 
***********

pyKeyring is a tool to store encrypted passwords in a simple database file. 

Installation
*************

Using pip
=========

You need Python 3 installed on your system.

The latest release can be installed from `pypi <https://pypi.org/project/pyKeyring/>`_ via pip:

.. code-block:: console

    foo@bar:~# pip install pykeyring

Manual Installation
====================

Manual installation allows you to run the latest development version from this repository.

pyKeyring depends on `TinyDB <https://github.com/msiemens/tinydb/>`_ and `Criptography <https://cryptography.io/en/latest/>`_ to run.

You can install pyKeyring with all dependecies by running:

.. code-block:: console

    foo@bar:~# python setup.py install

Usage
***********

pyKeyring is very simple to use.

Create a database
==================
.. code-block:: console

    foo@bar:~$ keyring.py -f /path/to/keyring.db create
    
The default database file is named keyring.db. If you don't use the -f argument, pyKeyring will use this name. 
You can use the -F argument to specify the storage format, BSON (default) or JSON.

Insert a password
==================
.. code-block:: console

    foo@bar:~$ keyring.py add password_label

The password_label is used to label your password :)

Get a password
==============
.. code-block:: console

    foo@bar:~$ keyring.py get password_label


If you don't want to print the password in the terminal you can use the argument -c to copy the password to clipboard.

.. code-block:: console

    foo@bar:~$ keyring.py get -c password_label

Update a password
=================
.. code-block:: console

    foo@bar:~$ keyring.py update password_label


Remove a password
==================
.. code-block:: console

    foo@bar:~$ keyring.py remove password_label

Generate a random password
===========================
.. code-block:: console

    foo@bar:~$ keyring.py generate

If you want to save this with a label you only need to use the -s (--save) argument.

.. code-block:: console

    foo@bar:~$ keyring.py generate -s label

You can limit the characteres used to generate the password using the arguments:

- `-l length, --length length`
    The length for the generated password [default=12]

- `-u, --no-uppercase`    
    Don't use uppercase chars in the password

-  `-ll, --no-lowercase`
    Don't use lowercase chars in the password

-  `-d, --no-digits`
    Don't use digits in the password

-  `-p, --no-punctuation`  
    Don't use punctuation chars in the password

-  `-e except_chars, --except-chars except_chars`
    Don't use these chars in the password

To generate an 8 digits password you can use:

.. code-block:: console

    foo@bar:~$ keyring.py generate -u -ll -p -l 8

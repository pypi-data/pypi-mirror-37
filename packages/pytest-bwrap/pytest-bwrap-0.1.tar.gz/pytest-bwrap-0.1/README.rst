Sandboxed Tests
===============

This `pytest`_ plugin allows running each test in its own `bubblewrap`_
sandbox.

This means each test runs in its own isolated environment, no test has any
side-effects on any other.

Basic Usage
-----------

Just install the plugin::

    $ pip install pytest-bwrap

Then run your tests as usual, with a single added option::

    $ py.test --bwrap

Each test will be run in its own sandbox.

Sandbox details
---------------

The sandbox will have its own filesystem, layed out as follows:

* network access is blocked by default; (see "Options")

* the following are mounted read-only from the host system:

  * ``/etc/hosts`` and ``/etc/resolv.conf``
  * ``/usr`` (and the accompanying ``/bin``, ``/lib``, ``/sbin``, with proper
    handling of ``/usr``-merge)

* the following are mounted from the host system:

  * ``/dev``
  * ``/proc``
  * the current directory (that is, the root of the project you are testing)
  * the active virtualenv, if running in one

* ``/tmp`` is a new ``tmpfs``;

Options
-------

Network Access
~~~~~~~~~~~~~~

Tests can optionally be granted network access, by decorating them with
``pytest_bwrap.decorators.network_enabled()``.

Additional Read-only Directories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is sometimes useful to have read-only directories, for example when
verifying error handling in the tested functions.

This can be achieved in one of two ways:

* decorating the test function with
  ``pytest_bwrap.decorators.read_only('/path/to/ro-dir')``;
* setting the ``extra-ro-dirs`` option in the `pytest configuration`_;

Example
-------

A full example of how to use this plugin for testing is included.

In particular, it shows how to use the decorators as well as the pytest
configuration.

You should be able to switch to that directory, then run the tests::

    $ pip install -r requirements.txt
    $ py.test --bwrap

All the tests should pass.

License
-------

This project is offered under the terms of the
`GNU Lesser General Public License, either version 3 or any later version`_,
see the `COPYING`_ file for details.


.. _bubblewrap: https://github.com/projectatomic/bubblewrap
.. _COPYING: COPYING
.. _GNU Lesser General Public License, either version 3 or any later version: http://www.gnu.org/licenses/lgpl.html
.. _pytest: https://docs.pytest.org
.. _pytest configuration: https://docs.pytest.org/en/latest/customize.html

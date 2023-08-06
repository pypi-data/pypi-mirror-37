=========
Antaresia
=========

Overview
========
TODO

Features
========
- Type checking (using mypy);
- Statement and Expression based configurations;
- Can be used as CLI or Python module;
- Basic security checks.

Security Features
=================
- Most imports are disallowed by default;
- Access to private attributes and variables is disallowed;
- Allow setting a timeout to process the configuration.

How to use
==========
For simple configuration files you simple need to execute:

.. code-block::

    antaresia myconfig.ppy

This will output your configuration as json.

Allowed Imports
---------------
By default, the only import that is allowed is ``typing``. But you can allow other imports with:

.. code-block::

    antaresia -i my.module myconfig.ppy

If you set allowed imports you also need to explicitly allow ``typing`` if you want to use it.

Antaresia provides some useful functions in ``antaresia.config_functions`` but they are not allowed
by default, since some of them can read files from the filesystem.

Timeout
-------
To give set a time limit to process a configuration use the ``--timeout\-t`` flag.
For example, to give up after 1 second, use:

.. code-block::

    antaresia -t 1 myconfig.ppy

TODO: How to use with IDEs

TODO: How to use as module
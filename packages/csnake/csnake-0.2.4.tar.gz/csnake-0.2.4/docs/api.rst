Developer Interface (API)
=========================

.. module:: csnake

.. role:: ccode(code)
    :language: c

.. role:: pycode(code)
    :language: python


Csnake has no user interface or CLI functionality.
It's a code-only package and is meant to be used by developers in their own
scripts and programs.
The API intended for external use is documented in this file.

File-level code container
-------------------------

This class is intended to be your main way of interacting with csnake.
It's a container allows for easy inclusion of various aspects of C language
constructs (i.e. a function's prototype, a variable's initialization, ...).

Those constructs must previously be declared (instantiated using the
:ref:`provided classes <C language constructs>`).

Calling the appropriate methods (i.e.
:meth:`CodeWriter.add_variable_initialization`) adds the code to the container
sequentially.

.. autoclass:: CodeWriter
    :members:
    :inherited-members:
    :show-inheritance:


C language constructs
---------------------

These classes describe C language constructs such as *functions*, *variables*,
*structs*, ...

They can be used on their own (by instantiating them and using their
:func:`str` or other functions such as *generate_declaration*,
*generate_definition*,... ) or via :class:`CodeWriter`.


.. autoclass:: Enum
   :members:
   :inherited-members:
   :show-inheritance:

.. autoclass:: Function
   :members:
   :inherited-members:
   :show-inheritance:

.. autoclass:: Struct
   :members:
   :inherited-members:
   :show-inheritance:

.. autoclass:: Variable
   :members:
   :inherited-members:
   :show-inheritance:

Variable initialization values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
These classes help You modify the literals you're using to initialize your
variables.

.. autoclass:: VariableValue
   :members:
   :inherited-members:
   :show-inheritance:

.. autoclass:: AddressOf
   :members:
   :inherited-members:
   :show-inheritance:

.. autoclass:: Arrow
   :members:
   :inherited-members:
   :show-inheritance:

.. autoclass:: Dereference
   :members:
   :inherited-members:
   :show-inheritance:

.. autoclass:: Dot
   :members:
   :inherited-members:
   :show-inheritance:

.. autoclass:: GenericModifier
   :members:
   :inherited-members:
   :show-inheritance:

.. autoclass:: OffsetOf
   :members:
   :inherited-members:
   :show-inheritance:

.. autoclass:: Subscript
   :members:
   :inherited-members:
   :show-inheritance:

.. autoclass:: TextModifier
   :members:
   :inherited-members:
   :show-inheritance:

.. autoclass:: Typecast
   :members:
   :inherited-members:
   :show-inheritance:

.. autoclass:: FormattedLiteral
   :members:
   :inherited-members:
   :show-inheritance:

Variable value literal formatters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can specify formatters which are used to modify the way literals are
printed by encasing your :class:`Variable`'s value with
a :class:`FormattedLiteral` with the some formatters given by keyword arguments
(see :class:`FormattedLiteral` for details).

These are some format functions used by default by csnake:

.. autofunction:: simple_bool_formatter

.. autofunction:: simple_str_formatter



Variable type declaration helpers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These classes help you declare complex types for use as :class:`Variable`'s
type.

.. autoclass:: FuncPtr
   :members:
   :inherited-members:
   :show-inheritance:


Extra variable value conversion modules
---------------------------------------
These submodules contain functions to convert more complicated types (like PIL
Images, for instance) to types that can be used as initializers.

Module pil_converter
^^^^^^^^^^^^^^^^^^^^

.. automodule:: csnake.pil_converter
   :members:
   :inherited-members:
   :show-inheritance:

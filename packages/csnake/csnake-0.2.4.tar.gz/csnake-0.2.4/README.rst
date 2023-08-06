######
csnake
######

.. image:: https://gitlab.com/andrejr/csnake/badges/master/pipeline.svg
   :alt: pipeline status
   :target: https://gitlab.com/andrejr/csnake/pipelines
.. image:: https://gitlab.com/andrejr/csnake/badges/master/coverage.svg
   :alt: coverage report
   :target: https://andrejr.gitlab.io/csnake/coverage/index.html

Csnake is a Python 3 package that helps you generate C code from Python.

Csnake provides you with a consistent and opinionated API that helps you
structure your C-generating Python code.
It does so by providing classes and functions for generating every C language
construct.

Probably the most important feature is the ability to initialize a value to
``struct`` and *array* initializers from Python dicts and lists (actually,
``Map``\s and ``Collection``\s), nested to an arbitrary level.

Here's a taste:

.. code-block:: python

   from csnake import CodeWriter, Variable, FormattedLiteral
   import numpy as np

   var = Variable(
       "test",
       primitive="struct whatever",
       value={
           "field1": [{'x': num, 'y': 10-num} for num in range(2)],
           "field2": {'test': range(3), 'field': np.arange(6).reshape(2,3)},
           "field3": FormattedLiteral([30, 31, 32], int_formatter=hex),
           "field4": 8,
       },
   )
   cw = CodeWriter()
   cw.add_variable_initialization(var)
   print(cw)


This yields:

.. code-block:: c

    struct whatever test = {
        .field1 = {
            {
                .x = 0,
                .y = 10
            },{
                .x = 1,
                .y = 9
            }
        },
        .field2 = {
            .test = {0, 1, 2},
            .field = {
                {0, 1, 2},
                {3, 4, 5}
            }

        },
        .field3 = {0x1e, 0x1f, 0x20},
        .field4 = 8
    };

As shown, ``numpy`` arrays are supported as values (so are ``sympy`` arrays),
and values can be formatted by arbitrary functions (here we're using ``hex`` to
output ints as hex literals for member `field3`).

Motivation
==========

Csnake's varable generation was motivated by a common embedded development
task: inputting data into C code.

Csnake should be of help when generating C code for representing data like
bitmaps, fonts, statemachines, lookup tables - as arrays and structs.
It can also be used for loop unrolling, templating, ...

Csnake  can be easily incorporated into a build system (Make, CMake,
Scons,...), and also goes along great with
`Ned Batcher's cog <https://nedbatchelder.com/code/cog/>`_.

Documentation
=============

Documentation (Sphinx) can be viewed on
`GitLab pages for this package <https://andrejr.gitlab.io/csnake/>`_.

Examples
========

Csnake is used on several of my yet-to-be-released open source embedded
projects. I'll be adding those (and other) examples along the way.

Credits
=======

Csnake is a major re-implementation (and improvement) of
`C-Snake <https://github.com/SchrodingersGat/C-Snake>`_
by
`Oliver <https://github.com/SchrodingersGat>`_
(original idea) and Andrej (variable initialization idea and implementation,
author of this package).

It's provided under the MIT license.

Changelog
=========

The changelog can be found within the documentation, 
`here <https://andrejr.gitlab.io/csnake/changes.html>`_.

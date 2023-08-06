BGPack
======

.. |bgpack| replace:: **bgpack**


|bgpack| is a Python package originally designed to work with genome position files.
The goal is to serve as a replacement for `tabix <http://www.htslib.org/doc/tabix.html>`_
for some files where we need data for each genomic position and the number of distinct values is
not huge (e.g. `CADD <http://cadd.gs.washington.edu/>`_).

|bgpack| is not restricted to genome position files. It can work with any file that is indexed
with an index that moves in steps of 1.
Basically, |bgpack| creates a set of distinct values and associates each with a unique key.
The keys are stored in a file.

Consider using |bgpack| if (accomplish all):

- for each position (index) you have one or more values, but *always the same amount of data*
- you have/need data for most of the positions. If you have many missing positions |bgpack| will store values also for them
  so you might use a lot of space in disk that you will never use
- values are repeated along the file. If you have as many distinct values as indexes |bgpack| will not give
  any advantage

.. contents:: Table of Contents


How it works
------------

|bgpack| works by receiving a ``parser``. The parser should be an iterator that returns
the index and the value(s) associated with that index. **Indexes** must be *integers*
and the parser has to return them in *incremental* order.

All distinct values returned by the parser are stored and |bgpack| generates a *key* for each of them.
Then the parser is iterated a second time and for each index the key(s) associated with the value(s)
is stored in a file ``.bgpck``. Along with it, the metadata information is saved in a pickle file (``.pkl``).

Options
*******

|bgpack| supports two types of packing:

- **read**: intended for fast reading, but make take more disk space.
- **size**: intended to optimize disk usage, but takes a bit more time to read the data

You can indicate you choice when you create the packed file.



How to use
----------

|bgpack| can be used from the command line or from Python.


Command line interface
**********************

The command line interface allows a easy, but restricted, use of |bgpack| capabilities.
You can create a packed file or read from one.

The creation of packed files is restricted to ``csv`` files.
You need to indicate the column of the index (``--position``)
the separator between the columns (tab by default) and
optionally wich columns you want to use as data and
which format do they have.

E.g.

.. code:: bash

   bgpack pack myfile.csv.gz --position 0 --sep , -c 1 -c 2.i -c 3.f2


Reading is simple, indicate the file and the start and end indexes


E.g.

.. code:: bash

   bgpack read myfile.pkl --from 1 --to 7


Python
******

Using |bgpack| from Python gives you more control and in addition it allows
the use of your own parsers, either making them from scratch or extending
existing ones (they can be found in the ``parser`` module).

If you want to make your own parser, just create an iterator that
returns the index in first place and the data afterwards.

A simple examples of a parser:

.. code:: python

       def parser():
           for i in range(12):
                yield i, i*5  # i is the position, i*5 the data


Then you can create the packed file using the ``create`` function from the
``packer`` module, and get the reader with the ``load`` function of the ``reader`` module.

The reader is a **context manager**, so you can use it with the ``with`` statement. E.g.:

.. code:: python

   reader = load(...)
   with reader as r:
        for pos, value in r.get(1, 7):
            ...


Further optimization
---------------------

As mentioned, |bgpack| can work with one or multiple data values
(provided for each index the amount is equal).
Thus, you can use a parser like:


.. code:: python

       def parser():
           for i in range(12):
               yield i, i*5, i*5

Then, for each each you will receive two values.
However, in this case, values of each index are completely linked.
In this case, it might be worth to provide the values a tuple
(for |bgpack| it will be as a single value) so you |bgpack| will save disk space.

.. code:: python

       def parser():
           for i in range(12):
               yield i, (i*5, i*5)

The drawback is that |bgpack| will also return them as a tuple.
In case it is not an issue to get them as a tuple, consider using the
``optimize`` function in the ``parser`` module to get some hints
of how to group your date to maximize disk usage.
Please, note that the advice is for the **size** option of the packer.

License
-------

`LICENSE <LICENSE.txt>`_.

|License| |Build Status|

Introduction
============

This project provides a Python 2.7/3.x library for common tasks
especially when writing shell-like scripts. Some of the functionality
overlaps with the standard library but the API is slightly modified.

The goal of this project is to leverage the straightforward, clean
syntax of Python while avoiding some of the boilerplate code that might
be necessary when using the standard library.

Status
======

Currently, this project is in the **development release** stage. While
this project is suitable for use, please note that there may be
incompatibilities in new releases.

Release notes are maintained in the project
`changelog <https://github.com/jeffrimko/Auxly/blob/master/CHANGELOG.adoc>`__.

Requirements
============

Auxly should run on any Python 2.7/3.x interpreter without additional
dependencies.

Installation
============

Auxly can be installed with pip using the following command:
``pip install auxly``

Additionally, Auxly can be installed from source by running:
``python setup.py install``

Usage
=====

Auxly provides various convenience functions for common tasks. Functions
that overlap with the standard library are designed to do what you would
reasonably expect
(`POLA <https://en.wikipedia.org/wiki/Principle_of_least_astonishment>`__)
and, when necessary, fail without throwing exceptions.

Auxly provides the following modules:

-  ``auxly`` - `Top Level <#top-level>`__

-  ``auxly.filesys`` - `File System <#file-system>`__

-  ``auxly.shell`` - `Shell <#shell>`__

-  ``auxly.stringy`` - `Stringy <#stringy>`__

-  ``auxly.listy`` - `Listy <#listy>`__

The following are basic examples of Auxly (all examples can be found
`here <https://github.com/jeffrimko/Auxly/tree/master/examples>`__):

-  `examples/delete\_1.py <https://github.com/jeffrimko/Auxly/blob/master/examples/delete_1.py>`__
   - Deletes all PYC files in the project.

Refer to the unit tests
`here <https://github.com/jeffrimko/Auxly/tree/master/tests>`__ for
additional examples.

Top Level
---------

Start by importing Auxly into your Python script:

.. code:: python

    import auxly

Auxly will attempt to open files and URLs using the default application:

.. code:: python

    auxly.open("myfile.txt")
    auxly.open("https://www.github.com/")

Auxly can tell you if the script is running as an admin:

.. code:: python

    auxly.isadmin()

Also in the top level is the ``auxly.throw()`` convenience function that
allows exceptions to be thrown if desired.

File System
-----------

The ``auxly.filesys`` module provides various convenience functions for
working with the file system.

Start by importing the file system module into your Python script:

.. code:: python

    import auxly.filesys as fs

Checking or changing the current working directory (CWD) is easy:

.. code:: python

    print(fs.cwd())  # Get the CWD.
    fs.cwd("foo")  # Set the CWD to `foo`.
    with fs.Cwd(fs.homedir()):  # Temporarily set CWD.
        pass  # do stuff here...

Copying or moving files is a snap:

.. code:: python

    fs.copy("foo.txt", fs.homedir())  # Simple file move.
    fs.move("bar", fs.homedir())  # Entire directory copied.

Note that copy/move functions return a boolean. Miss your exceptions?
Try the following:

.. code:: python

    fs.copy("foo.txt", "bar") or auxly.throw()  # Throws/raises exception on failure.

Check if a file or directory is empty:

.. code:: python

    fs.isempty("foo.txt")  # Works on files...
    fs.isempty("bar")  # ...or directories!

Need to make some directories:

.. code:: python

    fs.makedirs("bar/baz")

Delete files or directories:

.. code:: python

    fs.delete("bar")  # Returns true if successful.

There are ``File`` and ``Path`` objects too:

.. code:: python

    f = File("foo.txt")
    f.write("hello")
    f.append(" world")
    f.read()  # "hello world"

    p = File.path  # Path object
    p.isfile()  # True
    p.isdir()  # False
    p.isempty()  # False

Shell
-----

The ``auxly.shell`` module provides various convenience functions for
working with the system shell.

Start by importing the shell module into your Python script:

.. code:: python

    import auxly.shell as sh

Calling command line utilities is easy:

.. code:: python

    sh.call("ls")

Not sure if a utility is available on the shell? Try the following:

.. code:: python

    sh.has("ls")
    # True

Call a utility while hiding the output:

.. code:: python

    sh.silent("ls")

Need to iterate over the stdout of a command? Just use:

.. code:: python

    for line in sh.iterout("cat myfile.txt"):
        print(line)

Or get the stdout as a string:

.. code:: python

    sh.strout("ls")

Stringy
-------

The ``auxly.stringy`` module provides various convenience functions for
working with strings.

Start by importing the stringy module into your Python script:

.. code:: python

    import auxly.stringy as stringy

Substituting within a string is easy:

.. code:: python

    stringy.subat("bit", 2, "n")
    # bin

Need a random string? Try this:

.. code:: python

    stringy.randomize()
    # bnmzwx

Listy
=====

The ``auxly.listy`` module provides various convenience functions for
working with lists.

Start by importing the listy module into your Python script:

.. code:: python

    import auxly.listy as listy

Need to split a list into chunks? Not a problem:

.. code:: python

    list(chunk([1,2,3,4,5,6,7,8], 3))
    # [[1, 2, 3], [4, 5, 6], [7, 8]]

Need to smooth a chunky list? Worry not:

.. code:: python

    list(smooth([1,[2,[3,[4]]]]))
    # [1, 2, 3, 4]

Documentation
=============

The full documentation for this project can be found `here on Read the
Docs <http://auxly.readthedocs.io>`__.

Similar
=======

The following projects are similar and may be worth checking out:

-  `Reusables <https://github.com/cdgriffith/Reusables>`__

.. |License| image:: http://img.shields.io/:license-mit-blue.svg
.. |Build Status| image:: https://travis-ci.org/jeffrimko/Auxly.svg?branch=master


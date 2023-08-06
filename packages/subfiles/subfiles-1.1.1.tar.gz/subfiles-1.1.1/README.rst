.. image:: https://raw.githubusercontent.com/mindey/subfiles/master/misc/subfiles.png
    :alt: Subfiles Illustration
    :width: 100%
    :align: center
    
**Make files parsible!**

Say you're editing a wiki using default ``.txt`` files, but you are using some specific syntax, e.g., ``markdown``, or ``zimwiki``, or some other... How can another program know what schema you use in your ``.txt`` files, or your ``.json`` files, ``.xls`` files, any kind of other files? For all what we know, your pogram that you generated your files with might have a specific **version of program**, and the different versions of the program might use **specific schemas** (file formats) for these simple files (records stored in our disks). How do we make sure that the future generation can automatically know what schema was used, and what software can be used to automatically and 100% correctly parse them, or convert them to other types? One way would be to add ``Content-Type`` and ``Softare Version`` to each file. However, what if you want to do that without changing the files or their content? What if these are binary files? Well, the solution proposed here is that you just place ``.ftypes`` file into the directory where your files are, and describe, what these type of files are. for example::

    [*.txt]
    <description goes here>
    
    [*.json]
    <description goes here>

That's the main principle of ``.ftypes`` file. Our files are records in some databases, and if we want to organize them, we have to describe what record types they are...

Now, let's say you have multiple ``.txt`` files in a project, with different kind of internal format. Well, you can describe that in ``.ftypes`` too, if you give them a different subtype name e.g.::
    
    [*.kind1.txt]
    <description goes here>
    
    [*.kind2.txt]
    <description goes here>

We're introducing something like a second level of file extension here, like a namespacing in file extensions, and ``.ftypes`` is all about utilizing this to encode meaningful meta information, such as the file schema, and the ``subfiles`` package here is just a helper program to find and list all the existing file extensions, sub-extensions, etc. in current directory and all its subdirectories.

So what?
--------

So, now, I simply put the file ``.ftypes`` file in my folder where I keep my ``zimwiki``, and this way say, that my ``.txt`` files have a specific format in that folder, and happily use ZimWiki, knowing that later these files will be automatically convertable to whatever othe format that becomes popular.


Purpose
-------

Introduce command ``ftypes`` to extract ftypes of files in a directory, so as to have a list of file **sub**-extensions appearing in directory. 

Usage
-----

Set up::

    $ pip install subfiles

In any project, or directory, run to preview what files with subextensions are::

    $ ftypes -l [level]

This will output files grouped by different file sub-extensions in the project. The default ``[level]=2``. You can output standard extensions by choosing ``[level]=1``.

To preview what the ``.ftypes`` file would be generated, type::

    $ ftypes -s [level]

Again, the default is ``[level]=2``, and if you want to start defining the meaning for the 2nd level subextensions, just do::

    $ ftypes -s > .ftypes

Then, edit the generated ``.ftypes`` file to suit your needs, in the following format:

The basic format of the .subfiles is a wildcard map of file extensions within a ``[]``, an optional short description after double underscores ``__``, more information after it, and a new-line separator between the diffrent file format descriptions, that is:

.. code::

   [*.my_type.csv]
   __: SHORT DESCRIPTION
   MORE INFORMATION

   [*.my_other_type.json]
   __: SHORT DESCRIPTION
   MORE INFORMATION

Coded this way, it is easy to read with a config parser.

.. code::

   # Python3
   import configparser
   config = configparser.ConfigParser()
   config.optionxform=str
   config.read('.ftypes')
   # Sections
   config.sections()
   # Keys
   for key in config['*.my_type.csv']: print(key)
   # Values
   config['*.my_type.csv']['__']

.. code::

   # Python2
   import ConfigParser
   config = ConfigParser.RawConfigParser()
   config.optionxform=str
   config.readfp(open('.ftypes'))
   config.get('*.my_type.csv', '__')

However, this does not have to be limited to config format, as the 'more information' part could be almost any text.

Usage to Encode Schemas
-----------------------
One very useful case for ``.ftypes``, is encoding the information about the data schemas stored in files with sub-extensions. For this use-case, we might even agree to use a special kind of subtype, which is ``.schema.ftypes``:

.. code::

   [*.graph.json]
   __: https://www.wikidata.org/wiki/Q182598
   cat: https://www.wikidata.org/wiki/Q146
   dog: https://www.wikidata.org/wiki/Q144
   love: https://www.wikidata.org/wiki/Q316
   
   [*.products.csv]
   __: https://www.wikidata.org/wiki/Q278425
   url: https://www.wikidata.org/wiki/Q42253
   currency: https://www.wikidata.org/wiki/Q8142
   price: https://www.wikidata.org/wiki/Q160151
   name: https://www.wikidata.org/wiki/Q1786779

In the schema ftypes we could agree to have the links to concepts, the instance of which the thing in the file of this subextension is.

Custom Schemas
--------------

It may be that you are not entirely satisfied with the schema provided by http://schema.org, e.g., or want to define your own schemas in terms of concepts from custom or other ontologies, you could simply include them as a file subtype in your project. You can do it with a ``.ftypes``.


Why?
----

The idea here is that our file extensions don't have to end with one dot, and we can create multi-level namespaces for file extensions for all kind of uses based on dot notation. There are many potential uses. For example, you might want to use secondary level extensions represent and map files with schemas of data instances that they contain.

So, the idea here is to introduce a ``.ftypes`` dot file to contain any metadata that data developer assumes for files with subextensions to carry beyond what the traditional file extension represents to help any other programs or humans to understand the files in any project.

The ``ftypes`` command is simply a helper to extract **ftypes of files** in a directory, so as to have a list of file "subextensions" appearing in directory for any purpose. A subextension is an extension of second or greater level (e.g., ``'hello.world.txt'`` has top level extension ``.txt``, and second level subextension ``.world``).

Development reminder
====================

To publish new version on PyPI::

    $ python setup.py sdist bdist_wheel
    $ twine upload dist/*

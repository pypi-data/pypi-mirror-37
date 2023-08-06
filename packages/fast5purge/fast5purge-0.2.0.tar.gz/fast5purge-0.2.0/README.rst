fast5purge
==========

Purge a fast5 file or directory of fast5 files from potentially
sensitive information: the information in data in following locations
will be erased: - UniqueGlobalKey/context\_tags/filename -
UniqueGlobalKey/context\_tags/user\_filename\_input -
UniqueGlobalKey/tracking\_id/sample\_id -
UniqueGlobalKey/tracking\_id/ip\_address

WARNING
-------

| Currently modifies fast5 file IN PLACE. You cannot get your original
  data data back if you do not have a copy.
| I hope to fix this sooner or later, pull requests are very much
  welcome

INSTALLATION
------------

``pip install fast5purge``

USAGE
-----

::

    fast5purge [-h] [-d DIR] [-f FILE] [-r]

    Remove sensible content from a fast5 file or directory

    optional arguments:
      -h, --help            show this help message and exit
      -d DIR, --dir DIR     directory in which fast5 files have to be purged
      -f FILE, --file FILE  single fast5 file to purge
      -r, --recursive       recursively go through directory

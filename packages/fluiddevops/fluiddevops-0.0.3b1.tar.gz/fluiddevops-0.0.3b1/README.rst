===========
FluidDevOps
===========

|release| |coverage|

.. |release| image:: https://img.shields.io/pypi/v/fluiddevops.svg
   :target: https://pypi.python.org/pypi/fluiddevops/
   :alt: Latest version

.. |coverage| image:: https://codecov.io/bb/fluiddyn/fluiddevops/branch/default/graph/badge.svg
  :target: https://codecov.io/bb/fluiddyn/fluiddevops

FluidDevOps is a small package which provides some console scripts to
make DevOps easier.

See directory ``docker`` for more on running Docker containers.

Installation
------------

::

    python setup.py develop

Features
--------

- ``fluidmirror`` or ``fm``  to easily setup
  mercurial and git mirroring for a group of packages and periodically check
  for updates::

    usage: fluidmirror [-h] [-c CFG]
                       {init,list,clone,set-remote,pull,push,sync,run} ...

    A tool to handle multiple repositories. Works on a specific / all configured
    repositories (default)

- ``fluidicat`` to display the output of a command or contents of a file
  intermittently::

    usage: fluidicat [-h] [-e EVERY] [-w WAIT] [FILE [FILE ...]]

    Intermittent cat command. Watch stdin or catenate a set of filesand output to
    stdout for every N lines

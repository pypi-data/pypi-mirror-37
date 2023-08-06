mete0r.recipe.whoami
====================

Usage
-----

A sample buildout.

::

   [buildout]
   parts = whoami.txt
   
   [whoami]
   recipe = mete0r.recipe.whoami
   
   [whoami.txt]
   recipe = collective.recipe.template
   output = ${buildout:directory}/whoami.txt
   input=inline:
         user=${whoami:user}
         user-id=${whoami:user-id}
         group=${whoami:group}
         group-id=${whoami:group-id}
         real-user=${whoami:real-user}
         real-user-id=${whoami:real-user-id}
         real-group=${whoami:real-group}
         real-group-id=${whoami:real-group-id}




Development environment
-----------------------

To setup development environment::

   virtualenv -p python2.7 .
   bin/pip install -U setuptools pip pip-tools
   make
   make test

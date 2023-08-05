penv
====


Framework for ease project management tools building.


Principal rule is like autoenv_ from Kenneth Reitz but with more
fun. It basically allows you to create plugins (in Python) that are
activated/deactivated then entring/leaving project directory
(directory that contains ".penv")

.. _autoenv: https://github.com/kennethreitz/autoenv


Installation::

   $> pip install penv

   # And put following to your .bashrc
   # eval "`penv --startup-script`"


Usage::

   # overriden "cd" function generation
   $> penv --startup-script

   # You can simply check generated output by invoking the command.
   # To put it into effect please put the following into your .bashrc:
   #
   # eval "`penv --startup-script`"


So... what it does?
-------------------

Well why not just ask program itself?::

   # Case 1) - no ".penv"
   $> cd /tmp
   $> penv scan
   # Scanning: /tmp | OLDPWD=/tmp
   # Scanning: / | OLDPWD=/tmp
   #
   # ^^^^ haven't found anything but, as you can see, it doesn't
   # stop when it fails immediatelly - it searches for ".penv"
   # in parent directory, too.

   # Case 2) with ".penv" directory
   $> cd /tmp
   $> penv scan
   # Scanning: /tmp | OLDPWD=/tmp
   #     new env found (/tmp/.penv) and it shouldn't be skipped, so generating activation scripts
   #     ##############################
   #     Following places will be checked for plugins existance:
   #        /home/<user>/.penv/.plugins
   #        /tmp/.penv/.plugins
   #        /tmp/.penv-plugins
   #     ##############################

   # <GENERATE BASH CONTENT GOES HERE>

   #     generation script done.


Basically it searches for ".penv" directory whereever you go
with "cd" command (assuming you've installed it in .bashrc) and
activates whatever plugins are generating.


Ok, so why it's cool?
---------------------

#) It's very simple: basically it's just providing hooks for "cd"
   and "cd .." commands. Allows you to activate environment or your
   own specific tools and deactivate them when your leaving project
   directory.

#) Pluginable nature allows you to customize environment for each
   project and reuse plugins.


TODO
----

   - docs for plugins
   - some tests wouldn't hurt


Authors
-------

* Jakub Janoszek (kuba.janoszek@gmail.com)

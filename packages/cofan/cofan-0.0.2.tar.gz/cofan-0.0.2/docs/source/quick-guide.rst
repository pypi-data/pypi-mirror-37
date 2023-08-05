===========
Quick Guide
===========

---------------------
Serve local directory
---------------------

This is a typical usage example::
    
    from cofan import *
    import pathlib

    #assume we want to share files from `~/Videos` directory

    #lets make an http file browser and share our videos

    #first, we specify the icons used in the file browser
    #you can omit the theme. it defaults to `humanity`. This theme is supplied
    #with `cofan`.
    icons = Iconer(theme='humanity')

    #now we create a Filer and specify the path we want to serve
    vid = Filer(pathlib.Path.home() / 'Videos', iconer=icons)

    #now we need to give prefixes to our website
    #we create a patterner
    patterns = Patterner()

    #then we add the iconer and filer with their prefixes

    #first, we need to add our iconer
    #we should have told the iconer about its prefix but we did not. by default
    #it assumes `__icons__`
    #make sure to add a trailing slash
    patterns.add('__icons__/', icons)

    #now we add our filer as the root url
    patterns.add('', vid)

    #now we create our handler like in http.server. we give it our patterner
    handler = BaseHandler(patterns)

    #and create our server like in http.server
    srv = CofanServer(('localhost', 8000), handler)

    #and serve forever
    srv.serve_forever()

    #now try to open your browser on http://localhost:8000/

-----------------------
As a main python script
-----------------------

This module can also be run as a main python script to serve files from a
directory.

commandline syntax::

    python -m cofan.py [-a <addr>] [<root>]

options:

    * -a <addr>, --addr <addr>: specify the address and port to bind to. <addr>
    should be in the form `<ip>:<port>` where `<ip>` is the ip address and
    `<port>` is the tcp port. defaults to `localhost:8000`.

args:

    * root: The root directory to serve. Defaults to the current directory.

----------------
Further readings
----------------
In :doc:`serving-a-local-dir` you can a the more detailed cofan tutorial.
In :doc:`reference` you will find the library reference.


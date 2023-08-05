=========================
Serving a Local Directory
=========================

In this tutorial, we will look at different `cofan` features. We will start by
serving files from a local directory but then we will do more complicated things
like serving from a zip file and serving a website.

This tutorial is a practical tutorial. From this lesson we will write an example
program and explain how it is written. Our program will start simple then will
evolve with each lesson.

In this lesson, we will serve local files.

-------------
The beginning
-------------

First, you obviously need to install `cofan`. To start using the library, you
obviously need to import it::

    from cofan import *

---------------
The Filer class
---------------

`Filer` is the class used to serve local files. Before serving files, we need to
make a `Filer` instance and tell it what directory to serve. Here, we will serve
our videos. Our videos directory is '/home/user/Videos/'. Our program will
become::
    
    from cofan import *
    
    video = Filer('/home/user/Videos/')

We did not start our server yet. We only made our program know what files to
serve. There are still a few steps before we start serving.

-----------------
Handling requests
-----------------

We need something to handle our requests. If you have used `http.server`
standard python library, cofan uses similar way with a little difference.

We need to create a `BaseHandler` object that will serve requests and we need
to tell the handler that it should send incoming requests to our filer. We do
this by putting our filer as an argument to the handler constructor::
    
    handler = BaseHandler(video)

We need a few little steps to start serving files.

-------------------
Starting the server
-------------------

Similar to `http.server`, we need to create a server instance and give it the
address we want to serve at and the handler to send requests to. In `cofan`, you
can use the `Server` class. You can also use `http.server.Server` class if you
want but unlike `http.server.Server`, cofan `Server` class can serve multiple
requests at the same time.

Now we will create the server and tell it to serve at localhost:8000 and give it
our handler::

    server = cofan.Server(('localhost', 8000), handler)

And finally, we start serving forever::

    server.serve_forever()

Our final program now becomes::

    from cofan import *
    
    video = Filer('/home/user/Videos/')
    
    handler = BaseHandler(video)
    
    server = cofan.Server(('localhost', 8000), handler)
    
    server.serve_forever()

Now try to open `localhost:8000` in your web browser and you will see all your
files and folders inside `Videos`. However, there are no icons yet. In fact,
everything looks ugly so far. No worries as we will fix that soon.

----
Next
----

In next lessons, we will show file and directory icons in our website.

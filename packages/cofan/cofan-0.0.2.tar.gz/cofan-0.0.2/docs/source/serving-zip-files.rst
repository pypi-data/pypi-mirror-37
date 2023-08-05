=================
Serving Zip Files
=================

In the previous lesson, we made a home page that lists our music page video
page. In this lesson, we will add a little more thing. We will serve files but
not from a directory. We will serve files from within a zip file.

-----
Ziper
-----

The `Zipper` provider is very similar to the `Filer`. But instead of taking a
directory or file to serve, it takes a zip file. When a request comes to the
`Ziper`, it searches its zip file for the requested path. If found, it
uncompresses the file and sends it to the client.

Assume we want to serve the zip file in `/home/user/myarchive.zip`. The first
thing to do is create a `Ziper` and tell it where our zip file is. We also need
to tell it what iconer to use. We will use the same iconer we used for the video
filer and the music filer::

    ziper = Ziper('/home/user/myarchive.zip', iconer=iconer)

Second, we give our ziper a prefix and add it to the `pattener` just like what
we did to the other providers::

    patterner.add('zip/', ziper)

Our program now becomes::

    from cofan import *
    
    patterner = Patterner()
    iconer = Iconer()
    video = Filer('/home/user/Videos/', iconer=iconer)
    music = Filer('/home/user/Music/', iconer=iconer)
    #this is our lister
    lister = PatternLister(patterner, root='icons.zip')
    ziper = Ziper('/home/user/myarchive.zip', iconer=iconer)
    
    #add pages prefixes
    patterner.add('__icons__/', iconer)
    patterner.add('video/', video)
    patterner.add('music/', music)
    patterner.add('zip/', ziper)
    
    #remember: the home page prefix is always added last
    patterner.add('', lister)
    
    #make the handler use our patterner as its provider
    handler = BaseHandler(patterner)
    
    server = cofan.Server(('localhost', 8000), handler)

    server.serve_forever()

Now open your browser to `localhost:8000`. You will see that our `ziper` is
added to the home page because we added it to the `patterner`. Because we did
not put an icon for it in the `lister` icons zip file, you will find the `ziper`
has no icon. You can add an icon for it if you want.

If you click on the iconer link, you will see that the `ziper` behaves just like
our `filer`. You can browse the files in the zip archive and download any of
them.

------------------------
Serving a static website
------------------------

There are times when you want to serve a collection of html files as a website.
Usually, static html files website is just a directory or a zip file with html
files inside it. The home html file is called `index.html`.

When a `Filer` or a `Ziper` receives a request that points to a directory and
that directory contains a file named `index.html`, the `Filer` or `Ziper` will
not list the directory content. Instead, it will consider the directory to be a
static html website and will redirect the request to the `index.html` file.

I will leave the practice to test this for you to do.

----
Next
----

We have gone through the main features of `cofan`. In the next lesson, we will
go through a quick overview of other `cofan` features.

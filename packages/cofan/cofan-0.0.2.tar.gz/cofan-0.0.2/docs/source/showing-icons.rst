=============
Showing Icons
=============

In the previous lesson, we started serving our videos in a file browser-like
webpage. However, there were no icons in our page. In this lesson, we will add
icons to the page.

-----------------
Content providers
-----------------

Before we make our icons, let's take sometime learning what content providers
are in `cofan`.

`cofan` works with the concept of content providers. A provider is an object
that takes the requested URL and gives back an HTTP response code the content to
be sent to the client. An example of a content provider is the `Filer` object we
created in the previous lesson.

In cofan, we make a handler object and give it a single provider. Whenever the
handler gets a request, it asks the provider for the content. In the previous
lesson, we made a handler and told it to use our `Filer` object as its provider.
We could have used a different provider if we needed and that is what we are
going to do in this lesson.

----------------
The Iconer class
----------------

`Iconer` is a class used to serve icons. We create an `Iconer` object and tell
our filer to use it to get the icons.

To use icons, first we need to create an `Iconer` object and tell our filer to
use it::

    iconer = Iconer()
    video = Filer('/home/user/Videos/', iconer=iconer)

If you run the program now, you will notice nothing have changed. We still see
an ugly page with no icons.

The iconer is another content provider. It is like the filer but instead of
listing directory content, it serves an icon if it is asked to. In our example
above, all requests go to the filer object. No request ever goes to the iconer.

We need to send some requests to the filer and some requests to the iconer. This
is what we will do in the next few sections.

-------------------
The Patterner class
-------------------

We want to arrange our website to serve two things:

    * Our video files.
    * File icons to show them in the file browser web page.

We actually created the two providers for this, the filer and the iconer.
However, we can only add a single provider to the handler.

In such situation, the `Patterner` is our friend. The `Patterner` provider is a
provider that checks the requested url. Based on the url, it forwards the
request to other providers.

In our example, we will make a url plan:

    * If the url starts with `__icons__/` (notice the trailing slash `/`), we
      will forward the request to the iconer. In the next section, we will
      explain why we chose the prefix `__icons__`.
    * Otherwise, we will forward the request to the video filer.

The first step to do this is to create a `Patterner` instance::

    patterner = Patterner()

Then we add our iconer and filer, each with its prefix, to the patterner::

    patterner.add('__icons__/', iconer)
    patterner.add('', video)

Now, whenever the patterner gets a requested url which starts with '__icons__/',
it will forward it to the iconer and will remove the prefix from the url.
If the url does not start with `__icons__/`, it will check the other prefix.
Since the other prefix is an empty string, the check will always succeed
(because all strings start with an empty string).

Finally, instead of telling our handler to send requests to the filer directly,
we tell the handler to forward the request to the patterner. The patterner then
will forward to the other providers::
    
    handler = BaseHandler(patterner)

Our program now becomes::
    
    from cofan import *
    
    patterner = Patterner()
    iconer = Iconer()
    video = Filer('/home/user/Videos/', iconer=iconer)
    
    #add prefixes
    patterner.add('__icons__/', iconer)
    patterner.add('', video)
    
    #make the handler use our patterner as its provider
    handler = BaseHandler(patterner)
    
    server = cofan.Server(('localhost', 8000), handler)

    server.serve_forever()

Now our web site shows icons and looks better. In the next section, we will
learn more about how to customize our iconer.

-------------
Iconer prefix
-------------

Our iconer now works and serves icons. However, how does the `__icons__/` prefix
work? If you make any other prefix, it will not work.

In order to make the iconer work correctly with the filer, the iconer needs to
know what prefix you will give it. The same prefix has to be given to the iconer
and the patterner. Even though we did not tell the iconer what prefix we will
give it, it uses the prefix `__icons__/` by default. We could have changed that
to, for example, `myicons/` if we wanted. We do this by using the `prefix`
argument in the `Iconer` constructor. We just need to make sure that the prefix
we give to the iconer is the same prefix we add to the patterner::

    patterner = Patterner()
    iconer = Iconer()
    video = Filer('/home/user/Videos/', iconer=iconer)
    
    #add prefixes
    patterner.add('myicons/', iconer)
    patterner.add('', videos)

-------------
Iconer images
-------------

Another thing we can customize in our iconer is the icons to show. We can do
that in two ways.

The first way is to specify an icon `theme` name. There are
3 themes that come with `cofan`: `humanity`, `plane` and `zafiro`. If no theme
is  specified, the iconer chooses the default theme which is `humanity`. We can
change the theme using the `theme` argument in the `Iconer` constructor::

    iconer = Iconer(theme='plane', prefix='myicons/')

Now our icons have changed to use the `plane` theme.

The second way to use icons is to specify a path to a zip file that contains
icons using the `root` argument. For example::

    iconer = Iconer(root='/home/user/icons.zip', prefix='myicons/')

In order to use a zip file as an icon theme, it should contain image files in
its toplevel directory. The images can be in any format and with any extension
as long as the names follow the following rules:

    1- The icon for a specific file extension should be name by extension name.
        For example, `mp3` files icon can be names `mp3.png`, `mp3.jpg` or
        `mp3.<any extension>`.
    #- The icon for a general file mimetype should be named with the general
        mimetype. For example, an icon for video files generally can be named
        `video.png`, `video.jpg` or `video.<any extension>`. If you do not know
        what a mimetype is, search for it and read about what it is.
    #- The word `directory`. The icon with this name will be used as the icon for
        directories. For example, an icon for direcotries can be named
        `direcotry.png`, `direcotry.jpg` or `direcotry.<any extension>`.
    #- The word `generic`. The icon with this name will be used as a fallback
        icon for file types that have no icons in the zip file based on rules 1
        and 2 above. For example, a fallback icon can be named `generic.png`,
        `generic.jpg` or `generic.<any extension>`.

------------------
Our program so far
------------------

Below is our program so far. I have ignored the modifications we did in the last
two sections::

    from cofan import *

    patterner = Patterner()
    iconer = Iconer()
    video = Filer('/home/user/Videos/', iconer=iconer)
    
    #add prefixes
    patterner.add('__icons__/', iconer)
    patterner.add('', video)
    
    #make the handler use our patterner as its provider
    handler = BaseHandler(patterner)
    
    server = cofan.Server(('localhost', 8000), handler)

    server.serve_forever()

----
Next
----

In the next lesson, we will learn how to serve more than one local directory.

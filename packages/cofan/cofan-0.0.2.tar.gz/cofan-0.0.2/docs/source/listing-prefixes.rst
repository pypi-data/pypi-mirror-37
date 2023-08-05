================
Listing Prefixes
================

In the previous lesson, we made a music page in addition to the video page.
However, there is nothing in the home page of our website. In this lesson, we
will make a home page for our website which will contain a link to our video
page and another link for our music page.

--------------
Pattern lister
--------------

We need the `PatternLister` provider for this job. The `PatternLister` is used
to create a page with a list of all the prefixes in a `Patterner` object so that
users can click on an item and open the corresponding page. This will help us to
create our home page.

First, we need to create a `PatternLister` object and tell it to list prefixes
from our patterner::

    lister = PatternLister(patterner)

In our example, There are three prefixes in the `pattener`: `video/`, `music/`
and `__icons__/`. Our `lister` now knows them.

Remember that the `pattener` is the first provider that handles a request and it
will forward it to other providers. In order to forward requests to our
`lister`, we need to add it to the `pattener`::

    patterner.add('', lister)

Now our `lister` is added to the `pattener` and it has the home page prefix
(that is empty string). Now open your browser to `localhost:8000`.

Wait a second!! We have the ugly no icon page again.. Furthermore, it only
lists two prefixes: `video/` and `music/`. What about `__icons__`?!

For the ugly page without icons, it is OK because that is what we will fix in
the next section.

For the `__icons__/` prefix, it is not listed because the `PatterLister` by
default hides any prefix that starts and ends with two underscores. `__icons__/`
does start and ends with two underscores and that is why it is not listed. We
can change that if we wanted. However, we should leave the icons prefix unlisted
because this prefix is only used for icons and is not intended to be opened by
users directly.

----------------------
Icons for our prefixes
----------------------

Now we want to get rid of the no-icon ugliness. To do that, we first need to
make a zip file which contains icons for each prefix. So lets make a zip file
that contains the following:

    * An image named `video.png`.
    * An image named `music.png`.

The image names must be the same as the prefix after removing all trailing
slashes. The file format we used above is `png`. You could use any other format
if you like as long as the file name without extension is the same as the
prefix.

Second, we need to tell our `lister` to get the icons from this zip file. Save
the zip file in the same directory as our python file and name it `icons.zip`.
Now, we modify our `PatternLister` object creation to the following::

    lister = PatternLister(patterner, root='icons.zip')

Now our lister shows the icons we have put in the zip file.
    
Now our latest program is::
    
    from cofan import *
    
    from cofan import *
    
    patterner = Patterner()
    iconer = Iconer()
    video = Filer('/home/user/Videos/', iconer=iconer)
    music = Filer('/home/user/Music/', iconer=iconer)
    #this is our lister
    lister = PatternLister(patterner, root='icons.zip')
    
    #add pages prefixes
    patterner.add('__icons__/', iconer)
    patterner.add('video/', video)
    patterner.add('music/', music)
    
    #remember: the home page prefix is always added last
    patterner.add('', lister)
    
    #make the handler use our patterner as its provider
    handler = BaseHandler(patterner)
    
    server = cofan.Server(('localhost', 8000), handler)

    server.serve_forever()

-------------------------
Adding title to our pages
-------------------------

If you open the `lister` page, you will notice that the title shown in our
`lister` for each page is the same as the page prefix but without a trailing
slash. That is, our `video/` page is called `video` in the `lister`. The
`music/` page is called `music` in the `lister`. May be you want to change that.
For example, you want to start the title with a capital letter like `Music`. Or
may be your users are Russian and you want the title to be `Музыка`. You can do
that by giving the title as an argument to `Patterner.add()`::

    patterner.add('music/', music, 'Музыка')

Now we have changed the title for the `music/` page to be `Музыка`. You can
change it to anything else.

----
Next
----

In the next lesson, we will serve files which are compressed in a zip file.

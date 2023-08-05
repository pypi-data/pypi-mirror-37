============================
Serving Multiple Directories
============================

In the previous lesson, we added icons to our web site. However, we were only
serving our videos. In this lesson, we will serve the content of our music
folder too.

-------------
Another Filer
-------------

The first step to serve our music is to create another `Filer`. This is easy
for us because we did it in :doc: `serve-local-dir` lesson. The only difference
here is the directory we are serving.

music = Filer('/home/user/Music/', iconer=iconer)

Notice that we have used the same iconer to get the icons. This way, both the
video filer and the music filer will use the same icon theme.

---------------
Another pattern
---------------

Remember that we use the `Patterner` to forward requests to one of multiple
providers based on the url prefix. our `music` is just another provider. Before
we add it to the `patterner`, let make a few modifications to our previous
program. We will make another url prefix plan:

    * `video/` will be the prefix for the video filer.
    * `music/` will be the prefix for the music filer.
    * `__icons__/` will be the prefix for the iconer.

Notice that we changed the prefix for the video filer. Before, it was an empty
string. Now, it is `video/`. Let's add the providers to our `pattener` now::

    patterner.add('__icons__/', iconer)
    patterner.add('video/', video)
    patterner.add('music/', music)
    
We are done. Our program now becomes::
    
    from cofan import *
    
    patterner = Patterner()
    iconer = Iconer()
    video = Filer('/home/user/Videos/', iconer=iconer)
    music = Filer('/home/user/Music/', iconer=iconer)
    
    #add prefixes
    patterner.add('__icons__/', iconer)
    patterner.add('video/', video)
    patterner.add('music/', music)
    
    #make the handler use our patterner as its provider
    handler = BaseHandler(patterner)
    
    server = cofan.Server(('localhost', 8000), handler)

    server.serve_forever()

Notice that we do not have any provider for the home page url so if we type in
the browser address bar `localhost:8000`, we get a `NOT FOUND` error. We need to
type `localhost:8000/video/` or `localhost:8000/music/` to open an existing
page. That is not so convenient. All websites have a home page right? We are
going to fix this in the next lesson.

--------------------------
A last word about prefixes
--------------------------

The prefixes we use in our patterner class can be any regular expression. as
mentioned in a previous lesson, any trailing slash is required except for the
root url. The pattern `video` will make the patterner function improperly. Use
`video/` with a trailing slash instead.

Whenever a request is recieved, the patterner will do the following:

    * It removes the root address and the root address trailing slash.
      In our example, when the requested address is
      `localhost:8000/video/example.mp4`, the patterner will remove
      `localhost:8000/`. The url now becomes `video/example.mp4`.
    * Match each pattern with the beginning of the url. In our example, the url
      from the previous step is `video/example.mp4`. The patterner will look
      for the prefix that the url starts with. The prefix in this case
      will be `video/`.
    * Remove the prefix from the url. Now the url becomes only `example.mp4`.
    * Forwards the request and the new url to the corresponding provider.

Now the video filer will get a request with the url `example.mp4` only and will
search for this file in its root directory.

----
Next
----

In the next lesson, we will make a home page for our website. Our home page will
have links to our video page and music page.

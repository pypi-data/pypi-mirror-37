==============
Other Features
==============

We have highlighted the main features of `cofan`. In this lesson, we will have a
quick look on the other classes in the library.

--------
Statuser
--------

The `Statuser` provider is used to respond to requests with a constant status
code. Below is an example of how to create a `Statuser` object which always
replies with `404 Not Found` status code::

    not_found = Statuser(http.HTTPStatus.NOT_FOUND)

-----------
IPPatterner
-----------

The `IPPatterner` provider is used to respond differently based on the ip client
address. It is similar to the `Patterner` but it matches the beginning of the
client ip address instead of the url. The prefix is a regular expression string.
Below is an example of how to create an `IPPatterner` object which always
forwards requests to a filer only if the IP address of the client is in the
local network (that is 192.168.1.xxx)::

    filer = Filer('/home/user/Videos/')
    ippatterner = IPPatterner()
    #add a pattern
    ippatterner.add('192[.]168[.]1[.]', filer)

If the client address does not start with any added regular expression, the
client gets a `401 UNAUTHORIZED` response.

------
JFiler
------

The `JFiler` provider is the same as the `Filer` provider except it serves
directory content as a JSON object and it does not redirect to `index.html` even
if it is in a requested directory. Obviously it does not take any iconer. Below
is an example of creating a `JFiler`::

    jfiler = JFiler('/home/user/Videos/')

----
Next
----

This is everything in the `cofan` tutorial. You can have a look at `cofan`
reference at any time if you need detailed information.

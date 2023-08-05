********************
collective.lazysizes
********************

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

This package integrates `lazysizes <https://afarkas.github.io/lazysizes/>`_, a lightweight lazy loader, into Plone.

`lazysizes`_ is a fast, SEO-friendly and self-initializing lazyloader for images (including responsive images picture/srcset), iframes, scripts/widgets and much more.
It also prioritizes resources by differentiating between crucial in view and near view elements to make perceived performance even faster.

By using this package you can expect reductions of up to 80% in load time, 75% in page size and 50% in number of requests.

Mostly Harmless
===============

.. image:: https://img.shields.io/pypi/v/collective.lazysizes.svg
   :target: https://pypi.python.org/pypi/collective.lazysizes

.. image:: https://img.shields.io/travis/collective/collective.lazysizes/master.svg
    :target: https://travis-ci.org/collective/collective.lazysizes

.. image:: https://img.shields.io/coveralls/collective/collective.lazysizes/master.svg
    :target: https://coveralls.io/r/collective/collective.lazysizes

These are some sites using ``collective.lazysizes``:

* `CartaCapital <http://www.cartacapital.com.br/>`_ (BR)
* `Conversa Afiada <http://www.conversaafiada.com.br/>`_ (BR)
* `Portal Brasil 2016 <http://www.brasil2016.gov.br/>`_ (BR)

As long as `we have tested <https://github.com/aFarkas/lazysizes/issues/239>`_, `lazysizes`_ seems not to interfere with image indexing made by crawlers like Googlebot.

Got an idea? Found a bug? Let us know by `opening a support ticket <https://github.com/collective/collective.lazysizes/issues>`_.

Don't Panic
===========

Installation
------------

To enable this package in a buildout-based installation:

#. Edit your buildout.cfg and add add the following to it::

    [buildout]
    ...
    eggs =
        collective.lazysizes

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``collective.lazysizes`` and click the 'Activate' button.

How does it work
----------------

This package adds a transformer to the transform chain to integrate `lazysizes`_ into Plone.

The transformer looks for all the ``<img>``, ``<iframe>`` and ``<blockquote>`` tags inside the content and does the following:

* appends a ``lazyload`` class
* if the tag is an ``<img>``, transforms the ``src`` attribute into a ``data-src`` and uses a gray square in its place to maintain valid HTML code (this placeholder is loaded using the data URI scheme to avoid a new request to the server)
* if the tag is an ``<iframe>``, transforms the ``src`` attribute into a ``data-src``
* if the tag is a ``<blockquote>`` `containing a tweet <https://dev.twitter.com/web/embedded-tweets>`_, it adds a ``data-twitter`` attribute and removes the ``<script>`` tag associated with the Twitter widget to avoid a useless request

These transforms are applied to anonymous users only.

Look Ma! No Resource Registries
-------------------------------

This add-on uses a very opinionated approach on how to handle static resources in Plone.
We just deprecated resource registries in favor of a simpler approach: a viewlet in ``plone.htmlhead``.
This simplifies maintainance among multiple Plone versions and avoids bundling of unrelated resources.

Development
-----------

We use `webpack <https://webpack.js.org/>`_ to process static resources on this package.
Webpack processes SCSS and JS files, minifies the resulting CSS and JS, and optimizes all images.
The final JS file is also a UMD package, which provides compatibility with most popular script loaders.

To contribute, you should start the instance in one shell and start webpack watcher on another with the following command:

.. code-block:: bash

    $ bin/watch-lazysizes

Then go to ``webpack/app`` folder and edit SCSS and JS files;
Webpack watcher will automatically create the final resources in the right place.

There are also other commands added to handle more complex scenarios.
The following command will set the buildout node installation in the system PATH, this way you can use webpack as described on its documentation.

.. code-block:: bash

    $ bin/env-lazysizes

The following command generates JS and CSS without the minify step (it can be used to check the code being generated in a human readable way).

.. code-block:: bash

    $ bin/debug-lazysizes

The following command rebuilds static files and exit (insted of keep watching the changes):

.. code-block:: bash

    $ bin/build-lazysizes

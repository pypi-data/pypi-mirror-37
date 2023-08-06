
==============================
django-middleware-public-pages
==============================

Use this App to redirect the requests to 'public' alternative of the same view if the user is not logged in.
For example, if there are two views registered:
 - page_private (name=page1)
 - page_public (name=page1_pub)
If the user is not authenticated, the middleMiddleware will look for a url-name with the same name and the suffix '_pub' and redirect the request.
If the user is authenticated or the 'public' URL is not found, the Middleware has no effect.


Quick start
-----------

1. Install the app:


1. Add it to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django-middleware-public-pages',
    ]

2. Add the middleware at the end of the list in settings::

    MIDDLEWARE_CLASSES = (
       ...
       "django-middleware-public-pages",
    )

3. Configure two views, one for authenticated user e.g. page_private and another 
   for anonymous or public (page_public)::

    urlpatterns += [
       url("^page_private/$", views.Page1View.as_view(), name="page1"),
       url("^page_public/$",  views.Page2View.as_view(), name="page1_pub"),
       ...
    ]

The middleware will automaticaly redirect "/page_private" to "/page_public" if the user is not
authenticated.
Attention: important is the name of the view and not the url-path.

Project page - https://gitlab.com/rristow/django-middleware-public-pages.git

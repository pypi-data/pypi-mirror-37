Blender ID OAuth Client
=======================

This OAuth Client allows your Django application to authenticate
against Blender ID, the authentication service of Blender Foundation.


Quick start
-----------

- Add `'blender_id_oauth_client'` to your `INSTALLED_APPS` setting like this::

    INSTALLED_APPS = [
        ...
        'blender_id_oauth_client',
    ]

- Add `BLENDER_ID` configuration::

    BLENDER_ID = {
        # MUST end in a slash:
        'BASE_URL': 'http://id.local:8000/',
        'OAUTH_CLIENT': 'TEST-CLIENT-ID',
        'OAUTH_SECRET': 'TEST-SECRET'
    }

- Configure the correct URLs for logging in and out::

    LOGIN_URL = '/oauth/login'
    LOGOUT_URL = '/oauth/logout'
    LOGIN_REDIRECT_URL = '/redir-target-after-login'

    # Set to empty string to remain on Blender ID after logging out:
    LOGOUT_REDIRECT_URL = '/redir-target-after-logout'

- Include the URLconf in your project urls.py like this::

    path('oauth/', include('blender_id_oauth_client.urls')),

- Run `python manage.py migrate` to create the polls models.

- Start the development server and visit http://127.0.0.1:8000/oauth/login
  to create a local user by authenticating against Blender ID.

- Run `python manage.py makesuperuser your@email` to make yourself a
  superuser.

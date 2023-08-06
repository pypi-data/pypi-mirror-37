##################
django-allauth-ens
##################

This package is meant to ease the management of authentication of django-apps
at the ENS.

On top of django-allauth_, which provides easy ways to configure the
authentication of django-apps, this package provides:

* social authentication using Clipper (*cas.eleves*);

* ready-to-use templates in replacement of allauth' ones;

* helpers to use *allauth*'s login and logout views instead of those
  provided by third-parties (Django admin, wagtail, *etc*).


**Contents**

.. contents:: :local:


************
Installation
************

First, `install django-allauth`_.

Then, install *django-allauth-ens*:

.. code-block:: bash

  $ pip install django-allauth-ens

And edit your settings file:

.. code-block:: python

  INSTALLED_APPS = [
      # …

      # Above allauth to replace its templates.
      'allauth_ens',

      # Added when you installed allauth.
      'allauth',
      'allauth.account',
      'allauth.socialaccount',

      # Required to use CAS-based providers (e.g. Clipper).
      'allauth_cas',

      # …
  ]


*************
Configuration
*************

See also the `allauth configuration`_ and `advanced usage`_ docs pages.

``ACCOUNT_HOME_URL``
  *Optional* — A view name or an url path.

  Used as a link from the templates of ``allauth_ens`` to return to your
  application.

  **Examples:** ``'home'``, ``'/home/'``

``ACCOUNT_DETAILS_URL``
  *Optional* — A view name or an url path.

  Used as a link from the templates of ``allauth_ens`` for a logged in user to
  access their profile in your app.

  **Examples:** ``'my-account'``, ``'/my-account/'``

``ALLAUTH_ENS_HIGHLIGHT_CLIPPER``
  *Optional* — Boolean (default: `True`).

  When set to `True`, displays prominently the Clipper option in the login view
  (if you use the `allauth_ens` templates).

  
*****
Views
*****

Capture other login and logout views
====================================

You can use the ``capture_login`` and ``capture_logout`` views to replace the
login and logout views of other applications. They redirect to their similar
*allauth*'s view and forward the query string, so that if a GET parameter
``next`` is given along the initial request, user is redirected to this url on
successful login and logout.

This requires to add urls before the include of the app' urls.

For example, to replace the Django admin login and logout views with allauth's
ones:

.. code-block:: python

  from allauth_ens.views import capture_login, capture_logout

  urlpatterns = [
      # …

      # Add it before include of admin urls.
      url(r'^admin/login/$', capture_login),
      url(r'^admin/logout/$', capture_logout),

      url(r'^admin/$', include(admin.site.urls)),

      # …
  ]


*********
Templates
*********

The templates provided by *allauth* only contains the bare minimum. Hopefully,
this package includes ready-to-use templates. They are automatically used if
you put ``'allauth_ens'`` before ``'allauth'`` in your ``INSTALLED_APPS``,


*********
Providers
*********

*Google, Facebook¸ but also Clipper…*

To interact with an external authentication service, you must add the
corresponding provider application to your ``INSTALLED_APPS``.

*allauth* already includes `several providers`_ (see also `their python path`_).
In addition to that, this package adds the following providers:

Clipper
=======

It uses the CAS server `<https://cas.eleves.ens.fr/>`_.

Installation
  Add ``'allauth_ens.providers.clipper'`` to the ``INSTALLED_APPS``.

Configuration
  Available settings and their default value:

  .. code-block:: python

    SOCIALACCOUNT_PROVIDERS = {
        # …
        'clipper': {
            # These settings control whether a message containing a link to
            # disconnect from the CAS server is added when users log out.
            'MESSAGE_SUGGEST_LOGOUT_ON_LOGOUT': True,
            'MESSAGE_SUGGEST_LOGOUT_ON_LOGOUT_LEVEL': messages.INFO,
        },
    }
    
Auto-signup
  Populated data
    - username: ``<clipper>``
    - email (primary and verified): ``<clipper>@clipper.ens.fr``

********
Adapters
********

Long Term Clipper Adapter
=========================

We provide an easy-to-use SocialAccountAdapter to handle the fact that Clipper
accounts are not eternal, and that there is no guarantee that the clipper
usernames won't be reused later.

This adapter also handles getting basic information about the user from SPI's
LDAP.

**Important:** If you are building on top of *allauth*, take care to preserve
the ``extra_data['ldap']`` of ``SocialAccount`` instances related to *Clipper*
(where ``provider_id`` is ``clipper`` or ``clipper_inactive``).

Configuration
  Set ``SOCIALACCOUNT_ADAPTER='allauth_ens.adapter.LongTermClipperAccountAdapter'``
  in `settings.py`

Auto-signup
  Populated data
    - *username*: ``<clipper>@<entrance year>``
    - *email*: from LDAP's *mailRoutingAddress* field, or ``<clipper>@clipper.ens.fr``
    - *first_name*, *last_name* from LDAP's *cn* field
    - *entrance_year* (as 2-digit string), *department_code*, *department* and *promotion* (department+year) parsed from LDAP's *homeDirectory* field
    - *extra_data* in SocialAccount instance, containing all these field except *promotion* (and available only on first connection)

Account deprecation
  At the beginning of each year (i.e. early November), to prevent clipper
  username conflicts, you should run ``$ python manage.py deprecate_clippers``.
  Every association clipper username <-> user will then be put on hold, and at
  the first subsequent connection, a verification of the account will be made
  (using LDAP), so that a known user keeps his account, but a newcomer won't
  inherit an archicube's.

Customize
  You can customize the SocialAccountAdapter by inheriting
  ``allauth_ens.adapter.LongTermClipperAccountAdapter``. You might want to
  modify ``get_username(clipper, data)`` to change the default username format.
  By default, ``get_username`` raises a ``ValueError`` when the connexion to the
  LDAP failed or did not allow to retrieve the user's entrance year. Overriding
  ``get_username`` (as done in the example website) allows to get rid of that
  behaviour, and for instance attribute a default entrance year.

Initial migration
  If you used allauth without LongTermClipperAccountAdapter, or another CAS
  interface to log in, you need to update the Users to the new username policy,
  and (in the second case) to create the SocialAccount instances to link CAS and
  Users. This can be done easily with ``$ python manage.py install_longterm``.
      
*********
Demo Site
*********

See ``example/README``.


***********
Development
***********

First, you need to clone the repository.

Stylesheets
===========

This project uses `compass`_ to compile SCSS files to CSS.

Using bundler
-------------

Requirements
  * Ensure Ruby is installed (``$ ruby -v``) or `install Ruby`_
  * Ensure bundler is installed (``$ bundle -v``) or install bundler
    (``$ gem install bundler``)
  * Install dependencies: ``$ bundle install``

Compile
  * Watch changes and recompile: ``$ bundle exec compass watch``

Tests
=====

Local environment
-----------------

Requirements
  * fakeldap and mock, install with ``$ pip install mock fakeldap``

Run
  * ``$ ./runtests.py``

All
---

Requirements
  * tox, install with ``$ pip install tox``
  * ``python{2.7,3.4,3.5,3.6}`` must be available on your system path

Run
  * all (django/python with combined coverage + flake8 + isort): ``$ tox``


******
Howtos
******

Assuming you use the following settings (when needed):

.. code-block:: python

  ACCOUNT_ADAPTER = 'shared.allauth_adapter.AccountAdapter'
  SOCIALACCOUNT_ADAPTER = 'shared.allauth_adapter.SocialAccountAdapter'

Signup disabled, except for clipper provider (auto-signup)
==========================================================

In ``shared/allauth_adapter.py``:

.. code-block:: python

  class AccountAdapter(DefaultAccountAdapter):
      def is_open_for_signup(self, request):
          return False

  class SocialAccountAdapter(DefaultSocialAccountAdapter):
      def is_open_for_signup(self, request, sociallogin):
          # sociallogin.account is a SocialAccount instance.
          # See https://github.com/pennersr/django-allauth/blob/master/allauth/socialaccount/models.py

          if sociallogin.account.provider == 'clipper':
              return True

          # It returns AccountAdapter.is_open_for_signup().
          # See https://github.com/pennersr/django-allauth/blob/master/allauth/socialaccount/adapter.py
          return super().is_open_for_signup(request, sociallogin)


.. _django-allauth: https://django-allauth.readthedocs.io/en/latest/overview.html
.. _install django-allauth: https://django-allauth.readthedocs.io/en/latest/installation.html
.. _several providers: https://django-allauth.readthedocs.io/en/latest/providers.html
.. _allauth configuration: https://django-allauth.readthedocs.io/en/latest/configuration.html
.. _advanced usage: https://django-allauth.readthedocs.io/en/latest/advanced.html
.. _their python path: https://django-allauth.readthedocs.io/en/latest/installation.html
.. _compass: https://compass-style.org/
.. _install Ruby: https://www.ruby-lang.org/en/documentation/installation/

=====
Django Classic User Accounts
=====


Detailed documentation is in the "docs" directory.

Quick 
-----------

1. Add "ClassicUserAccounts" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'ClassicUserAccounts',
	'django.contrib.admin',
	'django.contrib.auth',
    ]

2. Add "AUTH_USER_MODEL" in your settings file like this::
	AUTH_USER_MODEL = 'ClassicUserAccounts.User'

3. Add "Middleware" to youe MIDDLEWARE settings like this::
	MIDDLEWARE = [
	   ...
	   'ClassicUserAccounts.middleware.ClassicUserAccountsMiddleWare',
	]

4. Add "SITE_NAME" in your settings file like this::
	SITE_NAME = 'Your site name'

5. Add url in your project.urls file::
	urlpatterns = [
		...
		path('accounts/', include('ClassicUserAccounts.urls')),
	]

6. Run `python manage.py migrate` to create the polls models.

7. Start the development server and visit http://127.0.0.1:8000/admin/
   to manage user profile (you'll need the Admin app enabled).

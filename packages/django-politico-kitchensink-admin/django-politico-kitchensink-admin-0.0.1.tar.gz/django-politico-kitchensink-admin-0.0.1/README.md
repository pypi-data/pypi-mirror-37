![POLITICO](https://rawgithub.com/The-Politico/src/master/images/logo/badge.png)

# django-politico-kitchensink-admin

### Quickstart

1. Install the app.

  ```
  $ pip install django-politico-kitchensink-admin
  ```

2. Add the app to your Django project and configure settings.

  ```python
  INSTALLED_APPS = [
      # ...
      "rest_framework",
      "kitchensink",
  ]

  #########################
  # kitchensink settings

  KITCHENSINK_AUTH_DECORATOR = "django.contrib.admin.views.decorators.staff_member_required" # default
  KITCHENSINK_SECRET_KEY = "a-bad-secret-key"
  KITCHENSINK_API_ENDPOINT = "https://kitchensink.politicoapps.com" # default
  KITCHENSINK_PUBLISH_DOMAIN = "https://www.politico.com" # default
  ```

3. Add the app to your project URLs.

  ```python
  # urls.py
  urlpatterns = [
      # ...
      path("kitchensink/", include("kitchensink.urls")),
  ]
  ```

4. Migrate and run your app!

  ```
  $ python manage.py migrate
  $ python manage.py runserver
  ```

### Developing

##### Running a development server

Developing python files? Move into example directory and run the development server with pipenv.

  ```
  $ cd example
  $ pipenv run python manage.py runserver
  ```

Developing static assets? Move into the pluggable app's staticapp directory and start the node development server, which will automatically proxy Django's development server.

  ```
  $ cd kitchensink/staticapp
  $ gulp
  ```

Want to not worry about it? Use the shortcut make command.

  ```
  $ make dev
  ```

##### Setting up a PostgreSQL database

1. Run the make command to setup a fresh database.

  ```
  $ make database
  ```

2. Add a connection URL to the `.env` file.

  ```
  DATABASE_URL="postgres://localhost:5432/kitchensink"
  ```

3. Run migrations from the example app.

  ```
  $ cd example
  $ pipenv run python manage.py migrate
  ```

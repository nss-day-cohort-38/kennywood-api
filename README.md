# Django REST Kennywood API

## Project Setup

* Clone down the repo and `cd` into it

* Create your OSX/Linux OS virtual environment:

  * `python -m venv KennywoodEnv`
  * `source ./KennywoodEnv/bin/activate`

* Install the app's dependencies:

  * `pip install -r requirements.txt`

* Run migrations (The migrations directory is not in the `.gitignore`, therefore you don't need to generate migrations):

  * `python manage.py migrate`

* Run your server

  * `python manage.py runserver`

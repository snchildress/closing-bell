# Closing Bell

Closing Bell is a vacation schedule management app. It's built on top of the [Django](https://djangoproject.com) [Python](https://python.org) framework.

## Contributing

Clone this repository and branch off `development` using the following branch naming convention:

* `feature/name`
* `task/name`
* `bug/name`

```bash
https://github.com/snchildress/closing-bell
```

Create and activate a virtual environment and turn on DEBUG mode for local development

```bash
virtualenv venv
source venv/bin/activate
export DEBUG=True
```

Migrate your development database, create a superuser, then run the development server

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Once your feature, task, or bug fix is complete, submit a Pull Request to the `development` branch

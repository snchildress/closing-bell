# Closing Bell

Closing Bell is a vacation schedule management app. It's built on top of the [Django](https://djangoproject.com) [Python](https://python.org) framework.

## Contributing

Clone this repository and branch off `development` using the following branch naming convention:

* `feature/name`
* `task/name`
* `bug/name`

```bash
git clone https://github.com/snchildress/closing-bell
git checkout -b feature/name
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

## To Do

The following tasks are intended to clarify the user experience or add additional functionality

### Clarify User Experience

- [ ] Make it clear to admins which user's request page you are viewing
- [ ] Allow users to specify a single date when taking a single day off
- [x] Remove confusing reset buttons
- [ ] Validate that a request's start date is before an end date
- [x] Swap the placement of one's balance and accrued days
- [ ] Provide admins the remaining balance of all users
- [ ] Remove nights and weekends from balance deductions and additions

### Additional Functionality

- [ ] Notify admins when users submit new requests
- [ ] Expose all users' requests by month and year in a single report view

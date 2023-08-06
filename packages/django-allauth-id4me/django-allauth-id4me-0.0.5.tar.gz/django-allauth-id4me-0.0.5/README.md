# django-allauth-id4me
Extension library for django-allauth to support ID4me (https://id4me.org) as social login provider.

## Specification reference
https://gitlab.com/ID4me/documentation/blob/master/id4ME%20Technical%20Specification.adoc
- Version: 1.0
- Revision: 02

## Installation

### Install the package from pip
```shell
pip install django-allauth-id4me
```

### Configure django-allauth if not yet installed
[See documentation](https://django-allauth.readthedocs.io/en/latest/installation.html)

### Configure django project
Add `allauth_id4me` to `INSTALLED_APPS` in your `settings.py`:
```python
INSTALLED_APPS = (
    ...
    # ... include the providers you want to enable:
    'allauth_id4me',
   ...
)
```

### Run migrations in your django project
```bash
python manage.py migrate
```

### Add social client configuration
Start your django project
```bash
python.exe manage.py runserver localhost:8000
```

Open /admin application
[http://localhost:8000/admin/](http://localhost:8000/admin/)

Go to Home › Social Accounts › Social applications and add new application:
- Provider: ID4me
- Name: the name of your application (will appear on login screen)
- Client id: wished client_id, may however not be respected
- Secret key: not used, fill with dummy value 

Open [http://localhost:8000/accounts/login/](http://localhost:8000/accounts/login/) and test the login with ID4me!

## Template customization
To present own ID4me login page it is enough to place new template in ```id4me``` folder inside your ```templates``` 
dictionary named ```login.html```. Minimum required content:
```html
<form id="id4me_login_form" class="id4me_login" method="post" action="{% url 'id4me_login' %}">
    {% csrf_token %}
    {{form.as_p}}
    <button type="submit">Sign In</button>
</form>
```

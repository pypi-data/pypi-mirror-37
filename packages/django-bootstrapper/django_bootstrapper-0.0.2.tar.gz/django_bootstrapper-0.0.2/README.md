# Django Bootstrapper

[![PyPI](https://img.shields.io/pypi/v/django-bootstrapper.svg)](https://pypi.org/project/django-bootstrapper)

This is a simple django project generator, it uses django default command and complete the schema generating a full application ready to use, including base, authentication, and template_base applications.

The main idea behind this projects is to automate some labors when we create projects.

The project folder structure will be:

```bash
project_folder
├── applications
│   ├── authentication (Authentication app from https://github.com/contraslash/authentication-django)
│   ├── base_template (Base template from https://github.com/contraslash/template_cdn_bootstrap)
│   └── __init__.py
├── base (base from https://github.com/contraslash/base-django)
├── manage.py
└── project_name
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

```

The project is git submodule based, and creates submodules for `authentication`, `base_template` and `base`, 
all open source projects  created by contraslash.

Also we recommend to use [Django Crud Generator](https://django-crud-generator.readthedocs.io/en/latest/) to create CRUD
automatically.

Our main goal is to create a project with a structure that we can extend using templates and existing files.
 
If you want to modify and add to your tree any submodule, we recommend to follow [this question](https://stackoverflow.com/questions/1260748/how-do-i-remove-a-submodule) 

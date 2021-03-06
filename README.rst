.. _README:

Django-Annotator-Store
======================

.. sphinx-start-marker-do-not-remove

.. image:: https://travis-ci.org/Princeton-CDH/django-annotator-store.svg?branch=master
   :target: https://travis-ci.org/Princeton-CDH/django-annotator-store
   :alt: Build Status
.. image:: https://codecov.io/gh/Princeton-CDH/django-annotator-store/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Princeton-CDH/django-annotator-store
   :alt: Code Coverage
.. image:: https://landscape.io/github/Princeton-CDH/django-annotator-store/master/landscape.svg?style=flat
   :target: https://landscape.io/github/Princeton-CDH/django-annotator-store/master
   :alt: Code Health
.. image:: https://requires.io/github/Princeton-CDH/django-annotator-store/requirements.svg?branch=master
   :target: https://requires.io/github/Princeton-CDH/django-annotator-store/requirements/?branch=master
   :alt: Requirements Status
.. image:: https://readthedocs.org/projects/django-annotator-store/badge/?version=latest
   :target: http://django-annotator-store.readthedocs.io/en/latest/
   :alt: Documentation Status

**annotator_store** is a `Django <https://www.djangoproject.com/>`_
application meant for use within a Django project as an
`annotator.js <https://github.com/openannotation/annotator>`_ 2.x annotation
store backend, and implements the `Annotator Storage API <http://docs.annotatorjs.org/en/latest/modules/storage.html?highlight=store#storage-api>`_.

**annotator_store** was originally develop as a component of
`Readux <https://github.com/ecds/readux>`_.


License
^^^^^^^

This software is distributed under the Apache 2.0 License.


Installation
------------

Use pip to install::

    pip install annotator_store

You can also install from GitHub.  Use branch or tag name, e.g.
``@develop`` or ``@1.0``, to install a specific tagged release or branch::

    pip install git+https://github.com/Princeton-CDH/django-annotator-store.git@develop#egg=annotator_store


Configuration
-------------

Add `annotator_store` to installed applications and make sure that other
required components are enabled::

    INSTALLED_APPS = (
        ...
      'django.contrib.auth',
      'django.contrib.admin',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.sites',
      'annotator_store',
        ...
    )


Include the annotation storage API urls at the desired base url with the
namespace::

    from annotator_store import views as annotator_views

    urlpatterns = [
        # annotations
        url(r'^annotations/api/', include('annotator_store.urls', namespace='annotation-api')),
        # annotatorjs doesn't handle trailing slash in api prefix url
        url(r'^annotations/api', annotator_views.AnnotationIndex.as_view(), name='annotation-api-prefix'),
    ]

Run migrations to create annotation database tables::

    python manage.py migrate

.. Note::

  If you want per-object permissions on individual annotations (rather than
  the standard django type-based permissions), you must also install
  `django-guardian` and include `guardian` in your
  **INSTALLED_APPS**.  Per-object permissions must be turned on in Django
  settings by setting **ANNOTATION_OBJECT_PERMISSIONS** to True.

Custom Annotation Model
^^^^^^^^^^^^^^^^^^^^^^^

This module is designed to allow the use of a custom Annotation model, in order
to add functionality or relationships to other models within an application.
To take advantage of this feature, you should extend the abstract model
`annotator_store.models.BaseAnnotation` and configure your model in
Django setings, e.g.::

    ANNOTATOR_ANNOTATION_MODEL = 'myapp.LocalAnnotation'

If you want per-object permissions on your annotation model, you should
extend `annotator_store.models.AnnotationWithPermissions` rather than
the base annotation class.

.. NOTE::

  Per-object permissions require that a `permissions plugin`_ be
  included when you initialize your annotator.js Annotator object.
  That code is currently available as a plugin in the `Readux codebase`_

.. _permissions plugin: https://github.com/ecds/readux/blob/master/sitemedia/js/annotator/annotator.permissions.js
.. _Readux codebase: https://github.com/ecds/readux

Development instructions
------------------------

This git repository uses `git flow`_ branching conventions.

.. _git flow: https://github.com/nvie/gitflow

Initial setup and installation:

- recommended: create and activate a python virtualenv::

    virtualenv annotator-store
    source annotator-store/bin/activate

- pip install the package with its python dependencies::

    pip install -e .


Unit Testing
^^^^^^^^^^^^

Unit tests are run with `py.test`_ but use
Django test classes for convenience and compatibility with django test suites.
Running the tests requires a minimal settings file for Django required
configurations.

.. _py.test: http://doc.pytest.org

- Copy sample test settings and add a **SECRET_KEY**::

    cp ci/testsettings.py testsettings.py

- To run the tests, either use the configured setup.py test command::

    python setup.py test

- Or install test requirements and use py.test directly::

    pip install -e '.[test]'
    py.test


Sphinx Documentation
^^^^^^^^^^^^^^^^^^^^

- To work with the sphinx documentation, install `sphinx` directly via pip
  or via::

    pip install -e '.[docs]'

- Documentation can be built in the `docs` directory using::

    make html




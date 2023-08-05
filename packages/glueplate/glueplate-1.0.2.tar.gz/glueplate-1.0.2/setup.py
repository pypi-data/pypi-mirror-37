from setuptools import setup

setup(
    name = "glueplate",
    version = "1.0.2",
    packages = ['glueplate', 'glueplate.config']    ,
    author = "makoto tsuyuki",
    author_email = "mtsuyuki@gmail.com",
    description = "Settings framework for framework or library.",
    license = "MIT",
    keywords = "settings config framework",
    url = "https://github.com/tsuyukimakoto/glueplate",
    test_suite = 'nose.collector',
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    long_description = '''
glueplate
========================================================

config framework

.. image:: https://travis-ci.org/tsuyukimakoto/glueplate.svg?branch=master
    :target: https://travis-ci.org/tsuyukimakoto/glueplate

.. image:: https://codecov.io/gh/tsuyukimakoto/glueplate/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/tsuyukimakoto/glueplate

.. image:: https://pyup.io/repos/github/tsuyukimakoto/glueplate/shield.svg
    :target: https://pyup.io/repos/github/tsuyukimakoto/glueplate/

.. image:: https://pyup.io/repos/github/tsuyukimakoto/glueplate/python-3-shield.svg
    :target: https://pyup.io/repos/github/tsuyukimakoto/glueplate/

.. image:: https://codebeat.co/badges/bb625f2e-572a-410f-9019-08006aac86cf
    :target: https://codebeat.co/projects/github-com-tsuyukimakoto-glueplate-master

What is Config framework?
------------------------------------------------------

Your framework or library might need default settings and you want your user to change them.

Many developer wrote this kind of code, and you are going to. GluePlate is it!

Features
------------------------------------------------------

Easy to write - Merge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You and your user write easiry.

Just import Glue as _ and write like nested dict.

::

    from glueplate import Glue as _


    settings = _(
        GLUE_PLATE_ENVIRONMENT_VARIABLE_KEY = 'BASEPACKAGE_SETTINGS_MODULE',
        from_base = 'comming from base',
        to_be_override = 'I am base.',
    )

glueplate import variable named `settings` from os.environ['GLUE_PLATE_BASE_MODULE'], this is a base settings.

Then glueplate looks settings.GLUE_PLATE_ENVIRONMENT_VARIABLE_KEY and import variable named `settings` from os.environ[settings.GLUE_PLATE_ENVIRONMENT_VARIABLE_KEY], this is a user customized settings. Customized settings needs only user needs override, or addition.

::

    from glueplate import Glue as _


    settings = _(
        from_sub='comming from sub',
        to_be_override = 'I am sub.',
    )

They are merged and easy to use.

::

    from glueplate import config

    assert('I am sub' == config.settings.to_be_override)
    assert('comming from base' == config.settings.from_base)
    assert('comming from sub' == config.settings.from_sub)

Append to list
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You may not want to override by you user, just add user's additional data.

glueplate provide special keyword prefix to append original settings variable.

- GLUE_PLATE_PLUS_BEFORE\_

    User can append list before.
    ::
    
        # base
        settings = _(
            list1 = [1,2,3],
        )

        # user customized
        settings = _(
            GLUE_PLATE_PLUS_BEFORE_list1 = [5,4]
        )

        # config.settings.list1 == [5, 4, 1, 2, 3]

- GLUE_PLATE_PLUS_AFTER\_

    Same as GLUE_PLATE_PLUS_BEFORE\_ but append to backward.
    ::

        # base
        settings = _(
            list1 = [1,2,3],
        )

        # user customized
        settings = _(
            GLUE_PLATE_PLUS_AFTER_list1 = [5,4]
        )

        # config.settings.list1 == [1, 2, 3, 5, 4]

Inherit other glueplate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You might use library using glueplate. Environment variable `GLUE_PLATE_BASE_MODULE` is only one on your process.

Your base settings can indecate library's gluplate settings module.

- GLUE_PLATE_PARENT_MODULES

    Specify library's gluplate settings module names as list.
    ::

        from glueplate import Glue as _


        settings = _(
            GLUE_PLATE_PARENT_MODULES=[
                'parentpackage1.parentpackage1_settings',
                'parentpackage2.parentpackage2_settings'
            ]
        )
'''
)


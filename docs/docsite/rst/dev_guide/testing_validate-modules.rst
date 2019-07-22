:orphan:

.. _testing_validate-modules:

****************
validate-modules
****************

.. contents:: Topics

Python program to help test or validate Ansible modules.

``validate-modules`` is one of the ``ansible-test`` Sanity Tests, see :ref:`testing_sanity` for more information.

Originally developed by Matt Martz (@sivel)


Usage
=====

.. code:: shell

    cd /path/to/ansible/source
    source hacking/env-setup
    ansible-test sanity --test validate-modules

Help
====

.. code:: shell

    usage: validate-modules [-h] [-w] [--exclude EXCLUDE] [--arg-spec]
                            [--base-branch BASE_BRANCH] [--format {json,plain}]
                            [--output OUTPUT]
                            modules [modules ...]

    positional arguments:
      modules               Path to module or module directory

    optional arguments:
      -h, --help            show this help message and exit
      -w, --warnings        Show warnings
      --exclude EXCLUDE     RegEx exclusion pattern
      --arg-spec            Analyze module argument spec
      --base-branch BASE_BRANCH
                            Used in determining if new options were added
      --format {json,plain}
                            Output format. Default: "plain"
      --output OUTPUT       Output location, use "-" for stdout. Default "-"


Extending validate-modules
==========================

The ``validate-modules`` tool has a `schema.py <https://github.com/ansible/ansible/blob/devel/test/sanity/validate-modules/schema.py>`_ that is used to validate the YAML blocks, such as ``DOCUMENTATION`` and ``RETURNS``.


Codes
=====

Errors
------

=========   ===================
  code      sample message
---------   -------------------
  **1xx**   **Locations**
  101       Interpreter line is not ``#!/usr/bin/python``
  102       Interpreter line is not ``#!powershell``
  103       Did not find a call to ``main()`` (or ``removed_module()`` in the case of deprecated & docs only modules)
  104       Call to ``main()`` not the last line (or ``removed_module()`` in the case of deprecated & docs only modules)
  105       GPLv3 license header not found
  106       Import found before documentation variables. All imports must appear below
            ``DOCUMENTATION``/``EXAMPLES``/``RETURN``/``ANSIBLE_METADATA``
  107       Imports should be directly below ``DOCUMENTATION``/``EXAMPLES``/``RETURN``/``ANSIBLE_METADATA``
  108       GPLv3 license header should be the :ref:`short form <copyright>` for new modules
  109       Next to last line is not ``if __name__ == "__main__":``
  ..
---------   -------------------
  **2xx**   **Imports**
  201       Did not find a ``module_utils`` import
  203       ``requests`` import found, should use ``ansible.module_utils.urls`` instead
  204       ``boto`` import found, new modules should use ``boto3``
  205       ``sys.exit()`` call found. Should be ``exit_json``/``fail_json``
  206       ``WANT_JSON`` not found in module
  207       ``REPLACER_WINDOWS`` not found in module
  208       ``module_utils`` imports should import specific components, not ``*``
  209       Only the following ``from __future__`` imports are allowed:
            ``absolute_import``, ``division``, and ``print_function``.
  210       ``subprocess.Popen`` used instead of ``module.run_command``
  211       ``os.call`` used instead of ``module.run_command``
  ..
---------   -------------------
  **3xx**   **Documentation**
  301       No ``DOCUMENTATION`` provided
  302       ``DOCUMENTATION`` is not valid YAML
  303       ``DOCUMENTATION`` fragment missing
  304       Unknown ``DOCUMENTATION`` error
  305       Invalid ``DOCUMENTATION`` schema
  306       Module level ``version_added`` is not a valid version number
  307       Module level ``version_added`` is incorrect
  308       ``version_added`` for new option is not a valid version number
  309       ``version_added`` for new option is incorrect
  310       No ``EXAMPLES`` provided
  311       ``EXAMPLES`` is not valid YAML
  312       No ``RETURN`` documentation provided
  313       ``RETURN`` is not valid YAML
  314       No ``ANSIBLE_METADATA`` provided
  315       ``ANSIBLE_METADATA`` was not provided as a dict, YAML not supported
  316       Invalid ``ANSIBLE_METADATA`` schema
  317       option is marked as required but specifies a default.
            Arguments with a default should not be marked as required
  318       Module marked as deprecated or removed in at least one of the filename, its metadata, or
            in DOCUMENTATION (setting DOCUMENTATION.deprecated for deprecation or removing all
            documentation for removed) but not in all three places.
  319       ``RETURN`` fragments missing  or invalid
  320       ``DOCUMENTATION.options`` must be a dictionary/hash when used
  321       ``Exception`` attempting to import module for ``argument_spec`` introspection
  322       argument is listed in the argument_spec, but not documented in the module
  323       argument is listed in DOCUMENTATION.options, but not accepted by the module
  324       Value for "default" from the argument_spec does not match the documentation
  325       argument_spec defines type different than documentation does
  326       Value for "choices" from the argument_spec does not match the documentation
  327       Default value from the documentation is not compatible with type defined in the argument_spec
  328       Choices value from the documentation is not compatible with type defined in the argument_spec
  329       Default value from the argument_spec is not compatible with type defined in the argument_spec
  330       Choices value from the argument_spec is not compatible with type defined in the argument_spec
  331       argument in argument_spec must be a dictionary/hash when used
  332       ``AnsibleModule`` schema validation error
  333       ``ANSIBLE_METADATA.status`` of deprecated or removed can't include other statuses
  334       ``ANSIBLE_METADATA`` cannot be changed in a point release for a stable branch
  335       argument_spec implies type="str" but documentation defines it as different data type
  336       argument in argument_spec is not a valid python identifier
  337       Type value is defined in ``argument_spec`` but documentation doesn't specify a type
  338       documentation doesn't specify a type but argument in ``argument_spec`` use default type (``str``)
  ..
---------   -------------------
  **4xx**   **Syntax**
  401       Python ``SyntaxError`` while parsing module
  403       Type comparison using ``type()`` found. Use ``isinstance()`` instead
  ..
---------   -------------------
  **5xx**   **Naming**
  501       Official Ansible modules must have a ``.py`` extension for python
            modules or a ``.ps1`` for powershell modules
  502       Ansible module subdirectories must contain an ``__init__.py``
  503       Missing python documentation file
=========   ===================

Warnings
--------

=========   ===================
  code      sample message
---------   -------------------
  **1xx**   **Locations**
  107       Imports should be directly below ``DOCUMENTATION``/``EXAMPLES``/``RETURN``/``ANSIBLE_METADATA`` for legacy modules
  ..
---------   -------------------
  **2xx**   **Imports**
  208       ``module_utils`` imports should import specific components for legacy module, not ``*``
  291       Try/Except ``HAS_`` expression missing
  292       Did not find ``ansible.module_utils.basic`` import
  ..
---------   -------------------
  **3xx**   **Documentation**
  312       No ``RETURN`` documentation provided for legacy module
  391       Unknown pre-existing ``DOCUMENTATION`` error
  392       Pre-existing ``DOCUMENTATION`` fragment missing
=========   ===================


.. _developing_resource_modules:

***********************************
Developing network resource modules
***********************************

.. contents::
  :local:

The resource module builder is an Ansible Playbook that helps developers scaffold and maintain an Ansible network resource module.

The resource module builder has the following capabilities:

- Uses a defined model to scaffold a resource module directory layout and initial class files.
- Scaffolds either an Ansible role or a collection.
- Subsequent uses of the resource module builder will only replace the module arspec and file containing the module docstring.
- Allows you to store complex examples along side the model in the same directory.
- Maintains the model as the source of truth for the module and use resource module builder to update the source files as needed.
- Generates working sample modules for both ``<network_os>_<resource>`` and ``<network_os>_facts``.

Accessing the resource module builder
=====================================

To access the resource module builder:

1. clone the github repository:

  .. code-block:: bash

    git clone https://github.com/ansible-network/resource_module_builder.git

2. Install the requirements:

  .. code-block:: bash

    pip install -r requirements.txt

Creating a model
================

You must create a model for your new resource. The resource module builder uses this model to create:

* The scaffold for a new module
* The argspec for the new module
* The docstring for the new module

The model is then the single source of truth for both the argspec and docstring, keeping them in sync. Use the resource module builder to generate this scaffolding. For any subsequent updates to the module, update the model first and use the resource module builder to update the module argspec and docstring.

For example, the resource model builder includes the ``myos_interfaces.yml`` sample in the :file:`models` directory, as seen below:

.. code-block:: yaml

  ---
  GENERATOR_VERSION: '1.0'
  ANSIBLE_METADATA: |
      {
          'metadata_version': '1.1',
          'status': ['preview'],
          'supported_by': '<support_group>'
      }
  NETWORK_OS: myos
  RESOURCE: interfaces
  COPYRIGHT: Copyright 2019 Red Hat
  LICENSE: gpl-3.0.txt

  DOCUMENTATION: |
    module: myos_interfaces
    version_added: 2.9
    short_description: 'Manages <xxxx> attributes of <network_os> <resource>'
    description: 'Manages <xxxx> attributes of <network_os> <resource>.'
    author: Ansible Network Engineer
   notes:
      - 'Tested against <network_os> <version>'
    options:
      config:
        description: The provided configuration
        type: list
        elements: dict
        suboptions:
          name:
            type: str
            description: The name of the <resource>
          some_string:
            type: str
            description:
            - The some_string_01
            choices:
            - choice_a
            - choice_b
            - choice_c
            default: choice_a
          some_bool:
            description:
            - The some_bool.
            type: bool
          some_int:
            description:
            - The some_int.
            type: int
            version_added: '1.1'
          some_dict:
            type: dict
            description:
            - The some_dict.
            suboptions:
              property_01:
                description:
                - The property_01
                type: str
      state:
        description:
        - The state of the configuration after module completion.
        type: str
        choices:
        - merged
        - replaced
        - overridden
        - deleted
        default: merged
  EXAMPLES:
    - deleted_example_01.txt
    - merged_example_01.txt
    - overridden_example_01.txt
    - replaced_example_01.txt

Notice that you should include examples for each of the states that the resource supports. The resource module builder also includes these in the sample model.

See `Ansible network resource models  <https://github.com/ansible-network/resource_module_models>`_ for more examples.

Using the resource module builder
=================================

To use the resource module builder to create a collection scaffold from your resource model:

.. code-block:: bash

  ansible-playbook -e rm_dest=<destination for modules and module utils> \
                   -e structure=collection \
                   -e collection_org=<collection_org> \
                   -e collection_name=<collection_name> \
                   -e model=<model> \
                   site.yml

Where the parameters are as follows:

- ``rm_dest``: The directory where the resource module builder places the files and directories for the resource module and facts modules.
- ``structure``: The directory layout type (role or collection)

  - ``role``: Generate a role directory layout.
  - ``collection``: Generate a collection directory layout.

- ``collection_org``: The organization of the collection, required when `structure=collection`.
- ``collection_name``: The name of the collection, required when `structure=collection`.
- ``model``: The path to the model file.

To use the resource module builder to create a role scaffold:

.. code-block:: bash

  ansible-playbook -e rm_dest=<destination for modules and module utils> \
                   -e structure=role \
                   -e model=<model> \
                   site.yml

Examples
========

Collection directory layout
---------------------------

This example shows the directory layout for the following:

- ``network_os``: myos
- ``resource``: interfaces

.. code-block:: bash

  ansible-playbook -e rm_dest=~/github/rm_example \
                   -e structure=collection \
                   -e collection_org=cidrblock \
                   -e collection_name=my_collection \
                   -e model=models/myos/interfaces/myos_interfaces.yml \
                   site.yml

.. code-block:: text

  ├── docs
  ├── LICENSE.txt
  ├── playbooks
  ├── plugins
  |   ├── action
  |   ├── filter
  |   ├── inventory
  |   ├── modules
  |   |   ├── __init__.py
  |   |   ├── myos_facts.py
  |   |   └──  myos_interfaces.py
  |   └──  module_utils
  |       ├── __init__.py
  |       └──  network
  |           ├── __init__.py
  |           └──  myos
  |               ├── argspec
  |               |   ├── facts
  |               |   |   ├── facts.py
  |               |   |   └──  __init__.py
  |               |   ├── __init__.py
  |               |   └──  interfaces
  |               |       ├── __init__.py
  |               |       └──  interfaces.py
  |               ├── config
  |               |   ├── __init__.py
  |               |   └──  interfaces
  |               |       ├── __init__.py
  |               |       └──  interfaces.py
  |               ├── facts
  |               |   ├── facts.py
  |               |   ├── __init__.py
  |               |   └──  interfaces
  |               |       ├── __init__.py
  |               |       └──  interfaces.py
  |               ├── __init__.py
  |               └──  utils
  |                   ├── __init__.py
  |                   └──  utils.py
  ├── README.md
  └──  roles


Role directory layout
---------------------

This example displays the role directory layout for the following:

- ``network_os``: myos
- ``resource``: interfaces

.. code-block:: bash

  ansible-playbook -e rm_dest=~/github/rm_example/roles/my_role \
                   -e structure=role \
                   -e model=models/myos/interfaces/myos_interfaces.yml \
                   site.yml


.. code-block:: text

    roles
    └── my_role
        ├── library
        │   ├── __init__.py
        │   ├── myos_facts.py
        │   └── myos_interfaces.py
        ├── LICENSE.txt
        ├── module_utils
        │   ├── __init__.py
        │   └── network
        │       ├── __init__.py
        │       └── myos
        │           ├── argspec
        │           │   ├── facts
        │           │   │   ├── facts.py
        │           │   │   └── __init__.py
        │           │   ├── __init__.py
        │           │   └── interfaces
        │           │       ├── __init__.py
        │           │       └── interfaces.py
        │           ├── config
        │           │   ├── __init__.py
        │           │   └── interfaces
        │           │       ├── __init__.py
        │           │       └── interfaces.py
        │           ├── facts
        │           │   ├── facts.py
        │           │   ├── __init__.py
        │           │   └── interfaces
        │           │       ├── __init__.py
        │           │       └── interfaces.py
        │           ├── __init__.py
        │           └── utils
        │               ├── __init__.py
        │               └── utils.py
        └── README.md


Using the collection
--------------------

This example shows how to use the generated collection in a playbook:

 .. code-block:: yaml

     ----
     - hosts: myos101
       gather_facts: False
       tasks:
       - cidrblock.my_collection.myos_interfaces:
         register: result
       - debug:
           var: result
       - cidrblock.my_collection.myos_facts:
       - debug:
           var: ansible_network_resources


Using the role
--------------

This example shows how to use the generated role in a playbook:

.. code-block:: yaml

    - hosts: myos101
      gather_facts: False
      roles:
      - my_role

    - hosts: myos101
      gather_facts: False
      tasks:
      - myos_interfaces:
        register: result
      - debug:
          var: result
      - myos_facts:
      - debug:
          var: ansible_network_resources


Resource module structure and workflow
======================================

The resource module structure includes the following components:

Module
    * ``library/<ansible_network_os>_<resource>.py``.
    * Imports the ``module_utils`` resource package and calls ``execute_module`` API

    .. code-block:: python

      def main():
          result = <resource_package>(module).execute_module()

Module argspec
    * ``module_utils/<ansible_network_os>/argspec/<resource>/``.
    * Argspec for the resource.

Facts
    * ``module_utils/<ansible_network_os>/facts/<resource>/``.
    * Populate facts for the resource.
    * Entry in ``module_utils/<ansible_network_os>/facts/facts.py`` for ``get_facts`` API to keep ``<ansible_network_os>_facts`` module and facts gathered for the resource module in sync for every subset.
    *  Entry of Resource subset in FACTS_RESOURCE_SUBSETS list in ``module_utils/<ansible_network_os>/facts/facts.py`` to make facts collection work.

Module package in module_utils
    * ``module_utils/<ansible_network_os>/<config>/<resource>/``.
    * Implement ``execute_module`` API that loads the configuration to device and generates the result with ``changed``, ``commands``, ``before`` and ``after`` keys.
    * Call ``get_facts`` API that returns the ``<resource>`` configuration facts or return the difference if the device has onbox diff support.
    * Compare facts gathered and given key-values if diff is not supported.
    * Generate final configuration.

Utils
    * ``module_utils/<ansible_network_os>/utils``.
    * Utilities for the ``<ansible_network_os>`` platform.

Developer notes
===============

The tests rely on a role generated by the resource module builder. After changes to the resource module builder, the role should be regenerated and the tests modified and run as needed. To generate the role after changes:

.. code-block:: bash

  rm -rf rmb_tests/roles/my_role
  ansible-playbook -e rm_dest=./rmb_tests/roles/my_role \
                   -e structure=role \
                   -e model=models/myos/interfaces/myos_interfaces.yml \
                   site.yml


.. _testing_resource_modules:


Unit testing Ansible network resource modules
=============================================


This section walks through an example of how to develop unit tests for Ansible network resource
modules.

See :ref:`testing_units` and :ref:`testing_units_modules` for general documentation on Ansible unit tests for modules.
Please read those pages first to understand unit tests and why and when you should use them.

.. note::

   The structure of the unit tests matches
   the structure of the code base, so the tests that reside in the :file:`test/units/modules/network` directory
   are organized by module groups.

Using mock objects to unit test Ansible network resource modules
----------------------------------------------------------------


Mock objects (from https://docs.python.org/3/library/unittest.mock.html) can be very
useful in building unit tests for special or difficult cases, but they can also
lead to complex and confusing coding situations.  One good use for mocks would be to
simulate an API. The ``mock`` Python package is bundled with Ansible (use
``import units.compat.mock``).

You can mock the device connection and output from the device as follows:

.. code-block:: python

   self.mock_get_config = patch('ansible.module_utils.network.common.network.Config.get_config')
   self.get_config = self.mock_get_config.start()

   self.mock_load_config = patch('ansible.module_utils.network.common.network.Config.load_config')
   self.load_config = self.mock_load_config.start()

   self.mock_get_resource_connection_config = patch('ansible.module_utils.network.common.cfg.base.get_resource_connection')
   self.get_resource_connection_config = self.mock_get_resource_connection_config.start()

   self.mock_get_resource_connection_facts = patch('ansible.module_utils.network.common.facts.facts.get_resource_connection')
   self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

   self.mock_edit_config = patch('ansible.module_utils.network.eos.providers.providers.CliProvider.edit_config')
   self.edit_config = self.mock_edit_config.start()

   self.mock_execute_show_command = patch('ansible.module_utils.network.eos.facts.l2_interfaces.l2_interfaces.L2_interfacesFacts.get_device_data')
   self.execute_show_command = self.mock_execute_show_command.start()

The facts file of the module now includes a new method, ``get_device_data``. Call ``get_device_data`` here to emulate the device output.


Mocking device data
-----------------------

To mock fetching results from devices or provide other complex data structures that
come from external libraries, you can use ``fixtures`` to read in pre-generated data. The text files for this pre-generated data live in ``test/units/modules/network/PLATFORM/fixtures/``. See for example the `eos_l2_interfaces.cfg file <https://github.com/ansible/ansible/blob/devel/test/units/modules/network/eos/fixtures/eos_l2_interfaces_config.cfg>`_.

Load data using the ``load_fixture`` method and set this data as the return value of the
``get_device_data`` method in the facts file:

.. code-block:: python

    def load_fixtures(self, commands=None, transport='cli'):
        def load_from_file(*args, **kwargs):
            return load_fixture('eos_l2_interfaces_config.cfg')
        self.execute_show_command.side_effect = load_from_file

See the unit test file `test_eos_l2_interfaces
<https://github.com/ansible/ansible/blob/devel/test/units/modules/network/eos/test_eos_l2_interfaces.py>`_
for a practical example.


.. seealso::

   :ref:`testing_units`
       Ansible unit tests documentation
   :ref:`testing_units`
       Deep dive into developing unit tests for Ansible modules
   :ref:`testing_running_locally`
       Running tests locally including gathering and reporting coverage data
   :ref:`developing_modules_general`
       Get started developing a module

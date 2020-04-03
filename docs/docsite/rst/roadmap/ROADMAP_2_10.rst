============
Ansible 2.10
============

.. contents::
   :local:

Release Schedule
----------------

Expected
========

PRs must be raised well in advance of the dates below to have a chance of being included in this Ansible release.

.. note:: There is no Alpha phase in 2.10.
.. note:: Dates subject to change.

- 2020-05-30 Beta 1 **Feature freeze**
  No new functionality (including modules/plugins) to any code

- 2020-06-30 Release Candidate 1
- 2020-??-?? Release Candidate 2 if needed
- 2020-07-30 Release

Release Manager
---------------

@sivel

Planned work
============

- Migrate non-base plugins and modules from the ``ansible/ansible`` repository to smaller collection repositories
- Add functionality to ease transition to collections, such as automatic redirects from the 2.9 names to the new FQCN of the plugin
- Create new ``ansible-base`` package representing the ``ansible/ansible`` repository

Additional Resources
====================

The 2.10 release of Ansible will fundamentally change the scope of plugins included in the ``ansible/ansible`` repository, by
moving much of the plugins into smaller collection repositories that will be shipped through https://galaxy.ansible.com/

The following links have more information about this process:

- https://groups.google.com/d/msg/ansible-devel/oKqgCeYTs-M/cHrOgMw8CAAJ
- https://github.com/ansible-collections/overview/blob/master/README.rst

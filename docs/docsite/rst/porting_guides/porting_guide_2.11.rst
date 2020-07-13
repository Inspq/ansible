
.. _porting_2.11_guide:

**************************
Ansible 2.11 Porting Guide
**************************

This section discusses the behavioral changes between Ansible 2.10 and Ansible 2.11.

It is intended to assist in updating your playbooks, plugins and other parts of your Ansible infrastructure so they will work with this version of Ansible.

We suggest you read this page along with `Ansible Changelog for 2.11 <https://github.com/ansible/ansible/blob/devel/changelogs/CHANGELOG-v2.11.rst>`_ to understand what updates you may need to make.

This document is part of a collection on porting. The complete list of porting guides can be found at :ref:`porting guides <porting_guides>`.

.. contents:: Topics


Playbook
========

No notable changes


Command Line
============

No notable changes


Deprecated
==========

No notable changes


Modules
=======

* The ``apt_key`` module has explicitly defined ``file`` as mutually exclusive with ``data``, ``keyserver`` and ``url``. They cannot be used together anymore.


Modules removed
---------------

The following modules no longer exist:

* No notable changes


Deprecation notices
-------------------

No notable changes


Noteworthy module changes
-------------------------

* facts - ``ansible_virtualization_type`` now tries to report a more accurate result than ``xen`` when virtualized and not running on Xen.


Plugins
=======

No notable changes


Porting custom scripts
======================

No notable changes


Networking
==========

No notable changes

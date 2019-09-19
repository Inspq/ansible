.. _slxos_platform_options:

***************************************
SLX-OS Platform Options
***************************************

Extreme SLX-OS Ansible modules only support CLI connections today. ``httpapi`` modules may be added in future.
This page offers details on how to use ``network_cli`` on SLX-OS in Ansible.

.. contents:: Topics

Connections Available
================================================================================

.. table::
    :class: documentation-table

    ====================  ==========================================
    ..                    CLI
    ====================  ==========================================
    Protocol              SSH

    Credentials           uses SSH keys / SSH-agent if present

                          accepts ``-u myuser -k`` if using password

    Indirect Access       via a bastion (jump host)

    Connection Settings   ``ansible_connection: network_cli``

    |enable_mode|         not supported by SLX-OS

    Returned Data Format  ``stdout[0].``
    ====================  ==========================================

.. |enable_mode| replace:: Enable Mode |br| (Privilege Escalation)


SLX-OS does not support ``ansible_connection: local``. You must use ``ansible_connection: network_cli``.

Using CLI in Ansible
====================

Example CLI ``group_vars/slxos.yml``
------------------------------------

.. code-block:: yaml

   ansible_connection: network_cli
   ansible_network_os: slxos
   ansible_user: myuser
   ansible_password: !vault...
   ansible_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- If you are using SSH keys (including an ssh-agent) you can remove the ``ansible_password`` configuration.
- If you are accessing your host directly (not through a bastion/jump host) you can remove the ``ansible_ssh_common_args`` configuration.
- If you are accessing your host through a bastion/jump host, you cannot include your SSH password in the ``ProxyCommand`` directive. To prevent secrets from leaking out (for example in ``ps`` output), SSH does not support providing passwords via environment variables.

Example CLI Task
----------------

.. code-block:: yaml

   - name: Backup current switch config (slxos)
     slxos_config:
       backup: yes
     register: backup_slxos_location
     when: ansible_network_os == 'slxos'


.. include:: shared_snippets/SSH_warning.txt

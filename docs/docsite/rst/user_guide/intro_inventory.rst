.. _intro_inventory:
.. _inventory:

**********************
Working with Inventory
**********************

.. contents::
   :local:

Ansible works against multiple systems in your infrastructure at the same time.
It does this by selecting portions of systems listed in Ansible's inventory,
which defaults to being saved in the location ``/etc/ansible/hosts``.
You can specify a different inventory file using the ``-i <path>`` option on the command line.

Not only is this inventory configurable, but you can also use multiple inventory files at the same time and
pull inventory from dynamic or cloud sources or different formats (YAML, ini, etc), as described in :ref:`intro_dynamic_inventory`.
Introduced in version 2.4, Ansible has :ref:`inventory_plugins` to make this flexible and customizable.

.. _inventoryformat:

Inventory basics: hosts and groups
==================================

The inventory file can be in one of many formats, depending on the inventory plugins you have.
For this example, the format for ``/etc/ansible/hosts`` is an INI-like (one of Ansible's defaults) and looks like this:

.. code-block:: guess

    mail.example.com

    [webservers]
    foo.example.com
    bar.example.com

    [dbservers]
    one.example.com
    two.example.com
    three.example.com

The headings in brackets are group names, which are used in classifying systems
and deciding what systems you are controlling at what times and for what purpose.

A YAML version would look like:

.. code-block:: yaml

  all:
    hosts:
      mail.example.com:
    children:
      webservers:
        hosts:
          foo.example.com:
          bar.example.com:
      dbservers:
        hosts:
          one.example.com:
          two.example.com:
          three.example.com:

.. _host_multiple_groups:

Hosts in multiple groups
------------------------

You can put systems in more than one group, for instance a server could be both a webserver and in a specific datacenter.  For example, you could create groups that track:

* What - An application, stack or microservice. (For example, database servers, web servers, etc).
* Where - A datacenter or region, to talk to local DNS, storage, etc. (For example, east, west).
* When - The development stage, to avoid testing on production resources. (For example, prod, test).

Extending the previous YAML inventory to include what, when, and where would look like:

.. code-block:: yaml

  all:
    hosts:
      mail.example.com:
    children:
      webservers:
        hosts:
          foo.example.com:
          bar.example.com:
      dbservers:
        hosts:
          one.example.com:
          two.example.com:
          three.example.com:
      east:
        hosts:
          foo.example.com:
          one.example.com:
          two.example.com:
      west:
        hosts:
          bar.example.com:
          three.example.com:
      prod:
        hosts:
          foo.example.com:
          one.example.com:
          two.example.com:
      test:
        hosts:
          bar.example.com:
          three.example.com:

You can see that ``one.example.com`` exists in the ``dbservers``, ``east``, and ``prod`` groups.

You could also use nested groups to simplify ``prod`` and ``test`` in this inventory, for the same result:

.. code-block:: yaml

  all:
    hosts:
      mail.example.com:
    children:
      webservers:
        hosts:
          foo.example.com:
          bar.example.com:
      dbservers:
        hosts:
          one.example.com:
          two.example.com:
          three.example.com:
      east:
        hosts:
          foo.example.com:
          one.example.com:
          two.example.com:
      west:
        hosts:
          bar.example.com:
          three.example.com:
      prod:
        children:
          east:
      test:
        children:
          west:


If you do have systems in multiple groups, note that variables will come from all of the groups they are a member of. Variable precedence is detailed in :ref:`ansible_variable_precedence`.


Hosts and non-standard ports
-----------------------------
If you have hosts that run on non-standard SSH ports you can put the port number after the hostname with a colon.
Ports listed in your SSH config file won't be used with the `paramiko` connection but will be used with the `openssh` connection.

To make things explicit, it is suggested that you set them if things are not running on the default port:

.. code-block:: guess

    badwolf.example.com:5309

Suppose you have just static IPs and want to set up some aliases that live in your host file, or you are connecting through tunnels.
You can also describe hosts via variables:

In INI:

.. code-block:: guess

    jumper ansible_port=5555 ansible_host=192.0.2.50

In YAML:

.. code-block:: yaml

    ...
      hosts:
        jumper:
          ansible_port: 5555
          ansible_host: 192.0.2.50

In the above example, trying to ansible against the host alias "jumper" (which may not even be a real hostname) will contact 192.0.2.50 on port 5555.
Note that this is using a feature of the inventory file to define some special variables.
Generally speaking, this is not the best way to define variables that describe your system policy, but we'll share suggestions on doing this later.

.. note:: Values passed in the INI format using the ``key=value`` syntax are interpreted differently depending on where they are declared.
          * When declared inline with the host, INI values are interpreted as Python literal structures
          (strings, numbers, tuples, lists, dicts, booleans, None). Host lines accept multiple ``key=value`` parameters per line. Therefore they need a way to indicate that a space is part of a value rather than a separator.
          * When declared in a ``:vars`` section, INI values are interpreted as strings. For example ``var=FALSE`` would create a string equal to 'FALSE'. Unlike host lines, ``:vars`` sections accept only a single entry per line, so everything after the ``=`` must be the value for the entry.
          * Do not rely on types set during definition, always make sure you specify type with a filter when needed when consuming the variable.
          * Consider using YAML format for inventory sources to avoid confusion on the actual type of a variable. The YAML inventory plugin processes variable values consistently and correctly.

If you are adding a lot of hosts following similar patterns, you can do this rather than listing each hostname:

In INI:

.. code-block:: guess

    [webservers]
    www[01:50].example.com

In YAML:

.. code-block:: yaml

    ...
      webservers:
        hosts:
          www[01:50].example.com:

For numeric patterns, leading zeros can be included or removed, as desired. Ranges are inclusive.  You can also define alphabetic ranges:

.. code-block:: guess

    [databases]
    db-[a:f].example.com

You can also select the connection type and user on a per host basis:

.. code-block:: guess

   [targets]

   localhost              ansible_connection=local
   other1.example.com     ansible_connection=ssh        ansible_user=mpdehaan
   other2.example.com     ansible_connection=ssh        ansible_user=mdehaan

As mentioned above, setting these in the inventory file is only a shorthand, and we'll discuss how to store them in individual files in the 'host_vars' directory a bit later on.

.. _host_variables:

Assigning a variable to one machine: host variables
===================================================

As described above, it is easy to assign variables to hosts that will be used later in playbooks:

.. code-block:: guess

   [atlanta]
   host1 http_port=80 maxRequestsPerChild=808
   host2 http_port=303 maxRequestsPerChild=909

The YAML version:

.. code-block:: yaml

    atlanta:
      host1:
        http_port: 80
        maxRequestsPerChild: 808
      host2:
        http_port: 303
        maxRequestsPerChild: 909

.. _group_variables:

Assigning a variable to many machines: group variables
======================================================

Variables can also be applied to an entire group at once:

The INI way:

.. code-block:: guess

   [atlanta]
   host1
   host2

   [atlanta:vars]
   ntp_server=ntp.atlanta.example.com
   proxy=proxy.atlanta.example.com

The YAML version:

.. code-block:: yaml

    atlanta:
      hosts:
        host1:
        host2:
      vars:
        ntp_server: ntp.atlanta.example.com
        proxy: proxy.atlanta.example.com

Be aware that this is only a convenient way to apply variables to multiple hosts at once; even though you can target hosts by group, **variables are always flattened to the host level** before a play is executed.

.. _subgroups:

Inheriting variable values: group variables for groups of groups
----------------------------------------------------------------

You can make groups of groups using the ``:children`` suffix in INI or the ``children:`` entry in YAML.
You can apply variables to these groups of groups using ``:vars`` or ``vars:``:


.. code-block:: guess

   [atlanta]
   host1
   host2

   [raleigh]
   host2
   host3

   [southeast:children]
   atlanta
   raleigh

   [southeast:vars]
   some_server=foo.southeast.example.com
   halon_system_timeout=30
   self_destruct_countdown=60
   escape_pods=2

   [usa:children]
   southeast
   northeast
   southwest
   northwest

.. code-block:: yaml

  all:
    children:
      usa:
        children:
          southeast:
            children:
              atlanta:
                hosts:
                  host1:
                  host2:
              raleigh:
                hosts:
                  host2:
                  host3:
            vars:
              some_server: foo.southeast.example.com
              halon_system_timeout: 30
              self_destruct_countdown: 60
              escape_pods: 2
          northeast:
          northwest:
          southwest:

If you need to store lists or hash data, or prefer to keep host and group specific variables separate from the inventory file, see the next section.
Child groups have a couple of properties to note:

 - Any host that is member of a child group is automatically a member of the parent group.
 - A child group's variables will have higher precedence (override) a parent group's variables.
 - Groups can have multiple parents and children, but not circular relationships.
 - Hosts can also be in multiple groups, but there will only be **one** instance of a host, merging the data from the multiple groups.

.. _default_groups:

Default groups
==============

There are two default groups: ``all`` and ``ungrouped``. ``all`` contains every host.
``ungrouped`` contains all hosts that don't have another group aside from ``all``.
Every host will always belong to at least 2 groups (``all`` and ``ungrouped`` or ``all`` and some other group).
Though ``all`` and ``ungrouped`` are always present, they can be implicit and not appear in group listings like ``group_names``.

.. _splitting_out_vars:

Organizing host and group variables
===================================

Although you can store variables in the main inventory file, storing separate host and group variables files may help you track your variable values more easily.

Host and group variables can be stored in individual files relative to the inventory file (not directory, it is always the file).

These variable files are in YAML format. Valid file extensions include '.yml', '.yaml', '.json', or no file extension.
See :ref:`yaml_syntax` if you are new to YAML.

Let's say, for example, that you keep your inventory file at ``/etc/ansible/hosts``. You have a host named 'foosball' that's a member of two groups: 'raleigh' and 'webservers'. That host will use variables
in YAML files at the following locations::

    /etc/ansible/group_vars/raleigh # can optionally end in '.yml', '.yaml', or '.json'
    /etc/ansible/group_vars/webservers
    /etc/ansible/host_vars/foosball

For instance, suppose you have hosts grouped by datacenter, and each datacenter
uses some different servers.  The data in the groupfile '/etc/ansible/group_vars/raleigh' for
the 'raleigh' group might look like::

    ---
    ntp_server: acme.example.org
    database_server: storage.example.org

It is okay if these files do not exist, as this is an optional feature.

As an advanced use case, you can create *directories* named after your groups or hosts, and
Ansible will read all the files in these directories in lexicographical order. An example with the 'raleigh' group::

    /etc/ansible/group_vars/raleigh/db_settings
    /etc/ansible/group_vars/raleigh/cluster_settings

All hosts that are in the 'raleigh' group will have the variables defined in these files
available to them. This can be very useful to keep your variables organized when a single
file starts to be too big, or when you want to use :ref:`Ansible Vault<playbooks_vault>` on a part of a group's
variables.

Tip: The ``group_vars/`` and ``host_vars/`` directories can exist in
the playbook directory OR the inventory directory. If both paths exist, variables in the playbook
directory will override variables set in the inventory directory.

Tip: The ``ansible-playbook`` command looks for playbooks in the current working directory by default. Other Ansible commands (for example, ``ansible``, ``ansible-console``, etc.) will only look for ``group_vars/`` and ``host_vars/`` in the
inventory directory unless you provide the ``--playbook-dir`` option
on the command line.

Tip: Keeping your inventory file and variables in a git repo (or other version control)
is an excellent way to track changes to your inventory and host variables.

.. _how_we_merge:

How variables are merged
========================

By default variables are merged/flattened to the specific host before a play is run. This keeps Ansible focused on the Host and Task, so groups don't really survive outside of inventory and host matching. By default, Ansible overwrites variables including the ones defined for a group and/or host (see :ref:`DEFAULT_HASH_BEHAVIOUR<DEFAULT_HASH_BEHAVIOUR>`). The order/precedence is (from lowest to highest):

- all group (because it is the 'parent' of all other groups)
- parent group
- child group
- host

When groups of the same parent/child level are merged, it is done alphabetically, and the last group loaded overwrites the previous groups. For example, an a_group will be merged with b_group and b_group vars that match will overwrite the ones in a_group.

.. versionadded:: 2.4

Starting in Ansible version 2.4, users can use the group variable ``ansible_group_priority`` to change the merge order for groups of the same level (after the parent/child order is resolved). The larger the number, the later it will be merged, giving it higher priority. This variable defaults to ``1`` if not set. For example:

.. code-block:: yaml

    a_group:
        testvar: a
        ansible_group_priority: 10
    b_group:
        testvar: b

In this example, if both groups have the same priority, the result would normally have been ``testvar == b``, but since we are giving the ``a_group`` a higher priority the result will be ``testvar == a``.

.. note:: ``ansible_group_priority`` can only be set in the inventory source and not in group_vars/ as the variable is used in the loading of group_vars.

.. _using_multiple_inventory_sources:

Using multiple inventory sources
================================

As an advanced use case you can target multiple inventory sources (directories, dynamic inventory scripts
or files supported by inventory plugins) at the same time by giving multiple inventory parameters from the command
line or by configuring :envvar:`ANSIBLE_INVENTORY`. This can be useful when you want to target normally
separate environments, like staging and production, at the same time for a specific action.

Target two sources from the command line like this::

    ansible-playbook get_logs.yml -i staging -i production

Keep in mind that if there are variable conflicts in the inventories, they are resolved according
to the rules described in :ref:`how_we_merge` and :ref:`ansible_variable_precedence`.
The merging order is controlled by the order of the inventory source parameters.
If ``[all:vars]`` in staging inventory defines ``myvar = 1``, but production inventory defines ``myvar = 2``,
the playbook will be run with ``myvar = 2``. The result would be reversed if the playbook was run with
``-i production -i staging``.

**Aggregating inventory sources with a directory**

You can also create an inventory by combining multiple inventory sources and source types under a directory.
This can be useful for combining static and dynamic hosts and managing them as one inventory.
The following inventory combines an inventory plugin source, a dynamic inventory script,
and a file with static hosts::

    inventory/
      openstack.yml          # configure inventory plugin to get hosts from Openstack cloud
      dynamic-inventory.py   # add additional hosts with dynamic inventory script
      static-inventory       # add static hosts and groups
      group_vars/
        all.yml              # assign variables to all hosts

You can target this inventory directory simply like this::

    ansible-playbook example.yml -i inventory

It can be useful to control the merging order of the inventory sources if there's variable
conflicts or group of groups dependencies to the other inventory sources. The inventories
are merged in alphabetical order according to the filenames so the result can
be controlled by adding prefixes to the files::

    inventory/
      01-openstack.yml          # configure inventory plugin to get hosts from Openstack cloud
      02-dynamic-inventory.py   # add additional hosts with dynamic inventory script
      03-static-inventory       # add static hosts
      group_vars/
        all.yml                 # assign variables to all hosts

If ``01-openstack.yml`` defines ``myvar = 1`` for the group ``all``, ``02-dynamic-inventory.py`` defines ``myvar = 2``,
and ``03-static-inventory`` defines ``myvar = 3``, the playbook will be run with ``myvar = 3``.

For more details on inventory plugins and dynamic inventory scripts see :ref:`inventory_plugins` and :ref:`intro_dynamic_inventory`.

.. _behavioral_parameters:

Connecting to hosts: behavioral inventory parameters
====================================================

As described above, setting the following variables control how Ansible interacts with remote hosts.

Host connection:

.. include:: shared_snippets/SSH_password_prompt.txt

ansible_connection
    Connection type to the host. This can be the name of any of ansible's connection plugins. SSH protocol types are ``smart``, ``ssh`` or ``paramiko``.  The default is smart. Non-SSH based types are described in the next section.

General for all connections:

ansible_host
    The name of the host to connect to, if different from the alias you wish to give to it.
ansible_port
    The connection port number, if not the default (22 for ssh)
ansible_user
    The user name to use when connecting to the host
ansible_password
    The password to use to authenticate to the host (never store this variable in plain text; always use a vault. See :ref:`best_practices_for_variables_and_vaults`)


Specific to the SSH connection:

ansible_ssh_private_key_file
    Private key file used by ssh.  Useful if using multiple keys and you don't want to use SSH agent.
ansible_ssh_common_args
    This setting is always appended to the default command line for :command:`sftp`, :command:`scp`,
    and :command:`ssh`. Useful to configure a ``ProxyCommand`` for a certain host (or
    group).
ansible_sftp_extra_args
    This setting is always appended to the default :command:`sftp` command line.
ansible_scp_extra_args
    This setting is always appended to the default :command:`scp` command line.
ansible_ssh_extra_args
    This setting is always appended to the default :command:`ssh` command line.
ansible_ssh_pipelining
    Determines whether or not to use SSH pipelining. This can override the ``pipelining`` setting in :file:`ansible.cfg`.
ansible_ssh_executable (added in version 2.2)
    This setting overrides the default behavior to use the system :command:`ssh`. This can override the ``ssh_executable`` setting in :file:`ansible.cfg`.


Privilege escalation (see :ref:`Ansible Privilege Escalation<become>` for further details):

ansible_become
    Equivalent to ``ansible_sudo`` or ``ansible_su``, allows to force privilege escalation
ansible_become_method
    Allows to set privilege escalation method
ansible_become_user
    Equivalent to ``ansible_sudo_user`` or ``ansible_su_user``, allows to set the user you become through privilege escalation
ansible_become_password
    Equivalent to ``ansible_sudo_password`` or ``ansible_su_password``, allows you to set the privilege escalation password (never store this variable in plain text; always use a vault. See :ref:`best_practices_for_variables_and_vaults`)
ansible_become_exe
    Equivalent to ``ansible_sudo_exe`` or ``ansible_su_exe``, allows you to set the executable for the escalation method selected
ansible_become_flags
    Equivalent to ``ansible_sudo_flags`` or ``ansible_su_flags``, allows you to set the flags passed to the selected escalation method. This can be also set globally in :file:`ansible.cfg` in the ``sudo_flags`` option

Remote host environment parameters:

.. _ansible_shell_type:

ansible_shell_type
    The shell type of the target system. You should not use this setting unless you have set the
    :ref:`ansible_shell_executable<ansible_shell_executable>` to a non-Bourne (sh) compatible shell.  By default commands are
    formatted using ``sh``-style syntax.  Setting this to ``csh`` or ``fish`` will cause commands
    executed on target systems to follow those shell's syntax instead.

.. _ansible_python_interpreter:

ansible_python_interpreter
    The target host python path. This is useful for systems with more
    than one Python or not located at :command:`/usr/bin/python` such as \*BSD, or where :command:`/usr/bin/python`
    is not a 2.X series Python.  We do not use the :command:`/usr/bin/env` mechanism as that requires the remote user's
    path to be set right and also assumes the :program:`python` executable is named python, where the executable might
    be named something like :program:`python2.6`.

ansible_*_interpreter
    Works for anything such as ruby or perl and works just like :ref:`ansible_python_interpreter<ansible_python_interpreter>`.
    This replaces shebang of modules which will run on that host.

.. versionadded:: 2.1

.. _ansible_shell_executable:

ansible_shell_executable
    This sets the shell the ansible controller will use on the target machine,
    overrides ``executable`` in :file:`ansible.cfg` which defaults to
    :command:`/bin/sh`.  You should really only change it if is not possible
    to use :command:`/bin/sh` (i.e. :command:`/bin/sh` is not installed on the target
    machine or cannot be run from sudo.).

Examples from an Ansible-INI host file::

  some_host         ansible_port=2222     ansible_user=manager
  aws_host          ansible_ssh_private_key_file=/home/example/.ssh/aws.pem
  freebsd_host      ansible_python_interpreter=/usr/local/bin/python
  ruby_module_host  ansible_ruby_interpreter=/usr/bin/ruby.1.9.3

Non-SSH connection types
------------------------

As stated in the previous section, Ansible executes playbooks over SSH but it is not limited to this connection type.
With the host specific parameter ``ansible_connection=<connector>``, the connection type can be changed.
The following non-SSH based connectors are available:

**local**

This connector can be used to deploy the playbook to the control machine itself.

**docker**

This connector deploys the playbook directly into Docker containers using the local Docker client. The following parameters are processed by this connector:

ansible_host
    The name of the Docker container to connect to.
ansible_user
    The user name to operate within the container. The user must exist inside the container.
ansible_become
    If set to ``true`` the ``become_user`` will be used to operate within the container.
ansible_docker_extra_args
    Could be a string with any additional arguments understood by Docker, which are not command specific. This parameter is mainly used to configure a remote Docker daemon to use.

Here is an example of how to instantly deploy to created containers::

  - name: create jenkins container
    docker_container:
      docker_host: myserver.net:4243
      name: my_jenkins
      image: jenkins

  - name: add container to inventory
    add_host:
      name: my_jenkins
      ansible_connection: docker
      ansible_docker_extra_args: "--tlsverify --tlscacert=/path/to/ca.pem --tlscert=/path/to/client-cert.pem --tlskey=/path/to/client-key.pem -H=tcp://myserver.net:4243"
      ansible_user: jenkins
    changed_when: false

  - name: create directory for ssh keys
    delegate_to: my_jenkins
    file:
      path: "/var/jenkins_home/.ssh/jupiter"
      state: directory

For a full list with available plugins and examples, see :ref:`connection_plugin_list`.

.. note:: If you're reading the docs from the beginning, this may be the first example you've seen of an Ansible playbook. This is not an inventory file.
          Playbooks will be covered in great detail later in the docs.

.. seealso::

   :ref:`inventory_plugins`
       Pulling inventory from dynamic or static sources
   :ref:`intro_dynamic_inventory`
       Pulling inventory from dynamic sources, such as cloud providers
   :ref:`intro_adhoc`
       Examples of basic commands
   :ref:`working_with_playbooks`
       Learning Ansible's configuration, deployment, and orchestration language.
   `Mailing List <https://groups.google.com/group/ansible-project>`_
       Questions? Help? Ideas?  Stop by the list on Google Groups
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel

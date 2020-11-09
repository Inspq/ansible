.. _installation_guide:
.. _intro_installation_guide:

Installing Ansible
===================

This page describes how to install Ansible on different platforms.
Ansible is an agentless automation tool that by default manages machines over the SSH protocol. Once installed, Ansible does
not add a database, and there will be no daemons to start or keep running.  You only need to install it on one machine (which could easily be a laptop) and it can manage an entire fleet of remote machines from that central point.  When Ansible manages remote machines, it does not leave software installed or running on them, so there's no real question about how to upgrade Ansible when moving to a new version.


.. contents::
  :local:

Prerequisites
--------------

You install Ansible on a control node, which then uses SSH (by default) to communicate with your managed nodes (those end devices you want to automate).

.. _control_node_requirements:

Control node requirements
^^^^^^^^^^^^^^^^^^^^^^^^^

Currently Ansible can be run from any machine with Python 2 (version 2.7) or Python 3 (versions 3.5 and higher) installed. Ansible 2.11 will make Python 3.8 a soft dependency for the control node, but will function with the aforementioned requirements. Ansible 2.12 will require Python 3.8 or newer to function on the control node. Starting with Ansible 2.11, the project will only be packaged for Python 3.8 and newer.
This includes Red Hat, Debian, CentOS, macOS, any of the BSDs, and so on.
Windows is not supported for the control node, read more about this in `Matt Davis's blog post <http://blog.rolpdog.com/2020/03/why-no-ansible-controller-for-windows.html>`_.

When choosing a control node, bear in mind that any management system benefits from being run near the machines being managed. If you are running Ansible in a cloud, consider running it from a machine inside that cloud. In most cases this will work better than on the open Internet.

.. note::

    macOS by default is configured for a small number of file handles, so if you want to use 15 or more forks you'll need to raise the ulimit with ``sudo launchctl limit maxfiles unlimited``. This command can also fix any "Too many open files" error.


.. warning::

    Ansible 2.11 will make Python 3.8 a soft dependency for the control node, but will function with the aforementioned requirements. Ansible 2.12 will require Python 3.8 or newer to function on the control node. Starting with Ansible 2.11, the project will only be packaged for Python 3.8 and newer.

.. warning::

    Please note that some modules and plugins have additional requirements. For modules these need to be satisfied on the 'target' machine (the managed node) and should be listed in the module specific docs.

.. _managed_node_requirements:

Managed node requirements
^^^^^^^^^^^^^^^^^^^^^^^^^

On the managed nodes, you need a way to communicate, which is normally SSH. By
default this uses SFTP. If that's not available, you can switch to SCP in
:ref:`ansible.cfg <ansible_configuration_settings>`.  You also need Python 2 (version 2.6 or later) or Python 3 (version 3.5 or
later).

.. note::

   * If you have SELinux enabled on remote nodes, you will also want to install
     libselinux-python on them before using any copy/file/template related functions in Ansible. You
     can use the :ref:`yum module<yum_module>` or :ref:`dnf module<dnf_module>` in Ansible to install this package on remote systems
     that do not have it.

   * By default, before the first Python module in a playbook runs on a host, Ansible attempts to discover a suitable Python interpreter on that host. You can override the discovery behavior by setting the :ref:`ansible_python_interpreter<ansible_python_interpreter>` inventory variable to a specific interpreter, and in other ways. See :ref:`interpreter_discovery` for details.

   * Ansible's :ref:`raw module<raw_module>`, and the :ref:`script module<script_module>`, do not depend
     on a client side install of Python to run.  Technically, you can use Ansible to install a compatible
     version of Python using the :ref:`raw module<raw_module>`, which then allows you to use everything else.
     For example, if you need to bootstrap Python 2 onto a RHEL-based system, you can install it
     as follows:

     .. code-block:: shell

        $ ansible myhost --become -m raw -a "yum install -y python2"

.. _what_version:

Selecting an Ansible version to install
---------------------------------------

Which Ansible version to install is based on your particular needs. You can choose any of the following ways to install Ansible:

* Install the latest release with your OS package manager (for Red Hat Enterprise Linux (TM), CentOS, Fedora, Debian, or Ubuntu).
* Install with ``pip`` (the Python package manager).
* Install ``ansible-base`` from source to access the development (``devel``) version to develop or test the latest features.

.. note::

	You should only run ``ansible-base`` from ``devel`` if you are modifying ``ansible-base``, or trying out features under development. This is a rapidly changing source of code and can become unstable at any point.


Ansible creates new releases two to three times a year. Due to this short release cycle,
minor bugs will generally be fixed in the next release rather than maintaining backports on the stable branch.
Major bugs will still have maintenance releases when needed, though these are infrequent.


.. _installing_the_control_node:
.. _from_yum:

Installing Ansible on RHEL, CentOS, or Fedora
----------------------------------------------

On Fedora:

.. code-block:: bash

    $ sudo dnf install ansible

On RHEL and CentOS:

.. code-block:: bash

    $ sudo yum install ansible

RPMs for RHEL 7 and RHEL 8 are available from the `Ansible Engine repository <https://access.redhat.com/articles/3174981>`_.

To enable the Ansible Engine repository for RHEL 8, run the following command:

.. code-block:: bash

    $ sudo subscription-manager repos --enable ansible-2.9-for-rhel-8-x86_64-rpms

To enable the Ansible Engine repository for RHEL 7, run the following command:

.. code-block:: bash

    $ sudo subscription-manager repos --enable rhel-7-server-ansible-2.9-rpms

RPMs for currently supported versions of RHEL and CentOS are also available from `EPEL <https://fedoraproject.org/wiki/EPEL>`_.

.. note::

	Since Ansible 2.10 for RHEL is not available at this time,  continue to use Ansible 2.9.

Ansible can manage older operating systems that contain Python 2.6 or higher.

.. _from_apt:

Installing Ansible on Ubuntu
----------------------------

Ubuntu builds are available `in a PPA here <https://launchpad.net/~ansible/+archive/ubuntu/ansible>`_.

To configure the PPA on your machine and install Ansible run these commands:

.. code-block:: bash

    $ sudo apt update
    $ sudo apt install software-properties-common
    $ sudo apt-add-repository --yes --update ppa:ansible/ansible
    $ sudo apt install ansible

.. note:: On older Ubuntu distributions, "software-properties-common" is called "python-software-properties". You may want to use ``apt-get`` instead of ``apt`` in older versions. Also, be aware that only newer distributions (in other words, 18.04, 18.10, and so on) have a ``-u`` or ``--update`` flag, so adjust your script accordingly.

Debian/Ubuntu packages can also be built from the source checkout, run:

.. code-block:: bash

    $ make deb

You may also wish to run from source to get the development branch, which is covered below.

Installing Ansible on Debian
----------------------------

Debian users may leverage the same source as the Ubuntu PPA.

Add the following line to /etc/apt/sources.list:

.. code-block:: bash

    deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main

Then run these commands:

.. code-block:: bash

    $ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
    $ sudo apt update
    $ sudo apt install ansible

.. note:: This method has been verified with the Trusty sources in Debian Jessie and Stretch but may not be supported in earlier versions. You may want to use ``apt-get`` instead of ``apt`` in older versions.

Installing Ansible on Gentoo with portage
-----------------------------------------

.. code-block:: bash

    $ emerge -av app-admin/ansible

To install the newest version, you may need to unmask the Ansible package prior to emerging:

.. code-block:: bash

    $ echo 'app-admin/ansible' >> /etc/portage/package.accept_keywords

Installing Ansible on FreeBSD
-----------------------------

Though Ansible works with both Python 2 and 3 versions, FreeBSD has different packages for each Python version.
So to install you can use:

.. code-block:: bash

    $ sudo pkg install py27-ansible

or:

.. code-block:: bash

    $ sudo pkg install py36-ansible


You may also wish to install from ports, run:

.. code-block:: bash

    $ sudo make -C /usr/ports/sysutils/ansible install

You can also choose a specific version, for example ``ansible25``.

Older versions of FreeBSD worked with something like this (substitute for your choice of package manager):

.. code-block:: bash

    $ sudo pkg install ansible

.. _on_macos:

Installing Ansible on macOS
---------------------------

The preferred way to install Ansible on a Mac is with ``pip``.

The instructions can be found in :ref:`from_pip`. If you are running macOS version 10.12 or older, then you should upgrade to the latest ``pip`` to connect to the Python Package Index securely. It should be noted that pip must be run as a module on macOS, and the linked ``pip`` instructions will show you how to do that.

.. note::

	If you have Ansible 2.9 or older installed, you need to use ``pip uninstall ansible`` first to remove older versions of Ansible before re-installing it.

If you are installing on macOS Mavericks (10.9), you may encounter some noise from your compiler. A workaround is to do the following::

    $ CFLAGS=-Qunused-arguments CPPFLAGS=-Qunused-arguments pip install --user ansible


.. _from_pkgutil:

Installing Ansible on Solaris
-----------------------------

Ansible is available for Solaris as `SysV package from OpenCSW <https://www.opencsw.org/packages/ansible/>`_.

.. code-block:: bash

    # pkgadd -d http://get.opencsw.org/now
    # /opt/csw/bin/pkgutil -i ansible

.. _from_pacman:

Installing Ansible on Arch Linux
---------------------------------

Ansible is available in the Community repository::

    $ pacman -S ansible

The AUR has a PKGBUILD for pulling directly from GitHub called `ansible-git <https://aur.archlinux.org/packages/ansible-git>`_.

Also see the `Ansible <https://wiki.archlinux.org/index.php/Ansible>`_ page on the ArchWiki.

.. _from_sbopkg:

Installing Ansible on Slackware Linux
-------------------------------------

Ansible build script is available in the `SlackBuilds.org <https://slackbuilds.org/apps/ansible/>`_ repository.
Can be built and installed using `sbopkg <https://sbopkg.org/>`_.

Create queue with Ansible and all dependencies::

    # sqg -p ansible

Build and install packages from a created queuefile (answer Q for question if sbopkg should use queue or package)::

    # sbopkg -k -i ansible

.. _from swupd:

Installing Ansible on Clear Linux
---------------------------------

Ansible and its dependencies are available as part of the sysadmin host management bundle::

    $ sudo swupd bundle-add sysadmin-hostmgmt

Update of the software will be managed by the swupd tool::

   $ sudo swupd update

.. _from_pip:

Installing Ansible with ``pip``
--------------------------------

Ansible can be installed with ``pip``, the Python package manager. If ``pip`` isn't already available on your system of Python, run the following commands to install it::

    $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    $ python get-pip.py --user

.. note::

  	If you have Ansible 2.9 or older installed, you need to use ``pip uninstall ansible`` first to remove older versions of Ansible before re-installing it.

Then install Ansible [1]_::

    $ python -m pip install --user ansible


.. tip::

    If this is your first time installing packages with pip, you may need to perform some additional configuration before you are able to run
    Ansible. See the Python documentation on `installing to the user site`_ for more information.

.. _installing to the user site: https://packaging.python.org/tutorials/installing-packages/#installing-to-the-user-site

In order to use the ``paramiko`` connection plugin or modules that require ``paramiko``, install the required module [2]_::

    $ python -m pip install --user paramiko

If you wish to install Ansible globally, run the following commands::

    $ sudo python get-pip.py
    $ sudo python -m pip install ansible

.. note::

    Running ``pip`` with ``sudo`` will make global changes to the system. Since ``pip`` does not coordinate with system package managers, it could make changes to your system that leaves it in an inconsistent or non-functioning state. This is particularly true for macOS. Installing with ``--user`` is recommended unless you understand fully the implications of modifying global files on the system.

.. note::

    Older versions of ``pip`` default to http://pypi.python.org/simple, which no longer works.
    Please make sure you have the latest version of ``pip`` before installing Ansible.
    If you have an older version of ``pip`` installed, you can upgrade by following `pip's upgrade instructions <https://pip.pypa.io/en/stable/installing/#upgrading-pip>`_ .

Upgrading Ansible from version 2.9 and older to version 2.10 or later
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Starting in version 2.10, Ansible is made of two packages. You need to first uninstall the old Ansible version (2.9 or earlier) before upgrading.
If you do not uninstall the older version of Ansible, you will see the following message, and no change will be performed:

.. code-block:: console

    Cannot install ansible-base with a pre-existing ansible==2.x installation.

    Installing ansible-base with ansible-2.9 or older currently installed with
    pip is known to cause problems. Please uninstall ansible and install the new
    version:

    pip uninstall ansible
    pip install ansible-base

    ...

As explained by the message, to upgrade you must first remove the version of Ansible installed and then install it
to the latest version.

.. code-block:: console

    $ pip uninstall ansible
    $ pip install ansible

.. _from_pip_devel:

Installing the development version of ``ansible-base``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In Ansible 2.10 and later, The `ansible/ansible repository <https://github.com/ansible/ansible>`_ contains the code for basic features and functions, such as copying module code to managed nodes. This code is also known as ``ansible-base``.

.. note::

    You should only run ``ansible-base`` from ``devel`` if you are modifying ``ansible-base`` or trying out features under development. This is a rapidly changing source of code and can become unstable at any point.

.. note::

    If you have Ansible 2.9 or older installed, you need to use ``pip uninstall ansible`` first to remove older versions of Ansible before re-installing it.


You can install the development version of ``ansible-base`` directly from GitHub with pip.

.. code-block:: bash

    $ python -m pip install --user https://github.com/ansible/ansible/archive/devel.tar.gz

Replace ``devel`` in the URL mentioned above, with any other branch or tag on GitHub to install older versions of Ansible (prior to ``ansible-base`` 2.10.) This installs all of Ansible.

.. code-block:: bash

    $ python -m pip install --user https://github.com/ansible/ansible/archive/stable-2.9.tar.gz

See :ref:`from_source` for instructions on how to run ``ansible-base`` directly from source, without the requirement of installation.

.. _from_pip_venv:

Virtual Environments
^^^^^^^^^^^^^^^^^^^^

.. note::

	If you have Ansible 2.9 or older installed, you need to use ``pip uninstall ansible`` first to remove older versions of Ansible before re-installing it.

Ansible can also be installed inside a new or existing ``virtualenv``::

    $ python -m virtualenv ansible  # Create a virtualenv if one does not already exist
    $ source ansible/bin/activate   # Activate the virtual environment
    $ python -m pip install ansible

.. _from_source:

Running ``ansible-base`` from source (devel)
---------------------------------------------

In Ansible 2.10 and later, The `ansible/ansible repository <https://github.com/ansible/ansible>`_ contains the code for basic features and functions, such as copying module code to managed nodes. This code is also known as ``ansible-base``.

.. note::

	You should only run ``ansible-base`` from ``devel`` if you are modifying ``ansible-base`` or trying out features under development. This is a rapidly changing source of code and can become unstable at any point.

``ansible-base`` is easy to run from source. You do not need ``root`` permissions
to use it and there is no software to actually install. No daemons
or database setup are required.

.. note::

   If you want to use Ansible Tower as the control node, do not use a source installation of Ansible. Please use an OS package manager (like ``apt`` or ``yum``) or ``pip`` to install a stable version.


To install from source, clone the ``ansible-base`` git repository:

.. code-block:: bash

    $ git clone https://github.com/ansible/ansible.git
    $ cd ./ansible

Once ``git`` has cloned the ``ansible-base`` repository, setup the Ansible environment:

Using Bash:

.. code-block:: bash

    $ source ./hacking/env-setup

Using Fish::

    $ source ./hacking/env-setup.fish

If you want to suppress spurious warnings/errors, use::

    $ source ./hacking/env-setup -q

If you don't have ``pip`` installed in your version of Python, install it::

    $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    $ python get-pip.py --user

Ansible also uses the following Python modules that need to be installed [1]_:

.. code-block:: bash

    $ python -m pip install --user -r ./requirements.txt

To update ``ansible-base`` checkouts, use pull-with-rebase so any local changes are replayed.

.. code-block:: bash

    $ git pull --rebase

.. code-block:: bash

    $ git pull --rebase #same as above
    $ git submodule update --init --recursive

Once running the env-setup script you'll be running from checkout and the default inventory file
will be ``/etc/ansible/hosts``. You can optionally specify an inventory file (see :ref:`inventory`)
other than ``/etc/ansible/hosts``:

.. code-block:: bash

    $ echo "127.0.0.1" > ~/ansible_hosts
    $ export ANSIBLE_INVENTORY=~/ansible_hosts

You can read more about the inventory file at :ref:`inventory`.

Now let's test things with a ping command:

.. code-block:: bash

    $ ansible all -m ping --ask-pass

You can also use "sudo make install".

.. _tagged_releases:

Finding tarballs of tagged releases
-----------------------------------

Packaging Ansible or wanting to build a local package yourself, but don't want to do a git checkout?  Tarballs of releases are available from ``pypi`` as https://pypi.python.org/packages/source/a/ansible/ansible-{{VERSION}}.tar.gz. You can make VERSION a variable in your package managing system that you update in one place whenever you package a new version. Alternately, you can download https://pypi.python.org/project/ansible  to get the latest stable release.

.. note::

	If you are creating your own Ansible package, you must also download or package ``ansible-base`` as part of your Ansible package. You can download it as https://pypi.python.org/packages/source/a/ansible-base/ansible-base-{{VERSION}}.tar.gz.

These releases are also tagged in the `git repository <https://github.com/ansible/ansible/releases>`_ with the release version.


.. _shell_completion:

Ansible command shell completion
--------------------------------

As of Ansible 2.9, shell completion of the Ansible command line utilities is available and provided through an optional dependency
called ``argcomplete``. ``argcomplete`` supports bash, and has limited support for zsh and tcsh.

You can install ``python-argcomplete`` from EPEL on Red Hat Enterprise based distributions, and or from the standard OS repositories for many other distributions.

For more information about installing and configuration see the `argcomplete documentation <https://argcomplete.readthedocs.io/en/latest/>`_.

Installing ``argcomplete`` on RHEL, CentOS, or Fedora
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On Fedora:

.. code-block:: bash

    $ sudo dnf install python-argcomplete

On RHEL and CentOS:

.. code-block:: bash

    $ sudo yum install epel-release
    $ sudo yum install python-argcomplete


Installing ``argcomplete`` with ``apt``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ sudo apt install python-argcomplete


Installing ``argcomplete`` with ``pip``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ python -m pip install argcomplete

Configuring ``argcomplete``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are 2 ways to configure ``argcomplete`` to allow shell completion of the Ansible command line utilities: globally or per command.

Globally
"""""""""

Global completion requires bash 4.2.

.. code-block:: bash

    $ sudo activate-global-python-argcomplete

This will write a bash completion file to a global location. Use ``--dest`` to change the location.

Per command
"""""""""""

If you do not have bash 4.2, you must register each script independently.

.. code-block:: bash

    $ eval $(register-python-argcomplete ansible)
    $ eval $(register-python-argcomplete ansible-config)
    $ eval $(register-python-argcomplete ansible-console)
    $ eval $(register-python-argcomplete ansible-doc)
    $ eval $(register-python-argcomplete ansible-galaxy)
    $ eval $(register-python-argcomplete ansible-inventory)
    $ eval $(register-python-argcomplete ansible-playbook)
    $ eval $(register-python-argcomplete ansible-pull)
    $ eval $(register-python-argcomplete ansible-vault)

You should place the above commands into your shells profile file such as ``~/.profile`` or ``~/.bash_profile``.

``argcomplete`` with zsh or tcsh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See the `argcomplete documentation <https://argcomplete.readthedocs.io/en/latest/>`_.

.. _getting_ansible:

``ansible-base`` on GitHub
---------------------------

You may also wish to follow the `GitHub project <https://github.com/ansible/ansible>`_ if
you have a GitHub account. This is also where we keep the issue tracker for sharing
bugs and feature ideas.


.. seealso::

   :ref:`intro_adhoc`
       Examples of basic commands
   :ref:`working_with_playbooks`
       Learning ansible's configuration management language
   :ref:`installation_faqs`
       Ansible Installation related to FAQs
   `Mailing List <https://groups.google.com/group/ansible-project>`_
       Questions? Help? Ideas?  Stop by the list on Google Groups
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel

.. [1] If you have issues with the "pycrypto" package install on macOS, then you may need to try ``CC=clang sudo -E pip install pycrypto``.
.. [2] ``paramiko`` was included in Ansible's ``requirements.txt`` prior to 2.8.

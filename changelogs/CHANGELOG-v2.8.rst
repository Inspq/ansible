===============================================
Ansible 2.8 "How Many More Times" Release Notes
===============================================

.. contents:: Topics


v2.8.5
======

Release Summary
---------------

| Release Date: 2019-09-12
| `Porting Guide <https://docs.ansible.com/ansible/devel/porting_guides.html>`__


Minor Changes
-------------

- ovirt_vm - add documentation warning about linux boot params - they will not be suported since oVirt 4.4 (https://bugzilla.redhat.com/1732437)
- ovirt_vm - add warning message about linux boot params - they will not be suported since oVirt 4.4 (https://bugzilla.redhat.com/1732437)

Bugfixes
--------

- Backported to stable-2.8 - Fix
- Extended loop variables now work with includes (https://github.com/ansible/ansible/pull/61231)
- Fix nxos_install_os test cases typo (https://github.com/ansible/ansible/pull/58825).
- Pipelining now works with the buildah plugin.
- acme_certificate - improve compatibility when finalizing ACME v2 orders. Fixes problem with Buypass' ACME v2 testing endpoint.
- apt_facts - fix performance regression when getting facts about apt packages (https://github.com/ansible/ansible/issues/60450)
- aws_s3 - Try to wait for the bucket to exist before setting the access control list.
- bigip_monitor_http - fix issue with receive parameter idempotency (https://github.com/ansible/ansible/pull/59999)
- ce_bfd_global - update to fix some bugs - When BFD is unavailable, tosExp and other parameters are sent down to report errors; this error is corrected and the query results are processed again. (https://github.com/ansible/ansible/pull/60412)
- constructed - Add a warning for the change in behavior in the sanitization of the groups option.
- digital_ocean_droplet - Fix creation of DigitalOcean droplets using digital_ocean_droplet module (https://github.com/ansible/ansible/pull/61655)
- docker_compose - fix issue where docker deprecation warning results in ansible erroneously reporting a failure
- docker_container - improve error behavior when parsing port ranges fails.
- docker_login - report change on successful logout (https://github.com/ansible/ansible/issues/59232)
- docker_swarm_service - allow the same port to be published both with TCP and UDP.
- meraki_syslog - Module would ignore net_id parameter if passed.
- meraki_syslog - Properly handle tasks with `net_id` instead of `net_name`.
- netapp_e_lun_mapping - Fix hosts with same lun number conflict in netapp_e_lun_mapping
- netapp_e_lun_mapping - Fix netapp_e_host module bug when lun=0
- openssl_certificate - if both private key and CSR were specified, the idempotency check for ``selfsigned`` and ``ownca`` providers ignored the CSR.
- os_user - when domain is provided, default_project will be taken from this domain.
- ovirt_vm - update tempalte search by datacenter (https://github.com/ansible/ansible/issues/59189)
- proxmox_kvm - fixed issue when vm has not yet a name item (https://github.com/ansible/ansible/issues/58194)
- purefa_facts - Fix bug which causes module failure when selecting I(admins) or I(all) against an old Purity version
- systemd - wait for a service which is in deactivating state when using ``state=stopped`` (https://github.com/ansible/ansible/pull/59471)
- user - allow 13 asterisk characters in password field without warning
- user - update docs to reflect proper way to remove account from all groups
- vmware - Ensure we can use the modules with Python < 2.7.9 or RHEL/CentOS < 7.4, this as soon as ``validate_certs`` is disabled.
- win_domain - Set reboot required dependent on exception and add exception id to error message
- win_domain_controller - Do not fail the play without the user being able to catch dcpromo failing because of a pending reboot within a playbook using ignore_error or retry logic.
- xenserver_guest - when adding disks to a VM in powered on state, disks are now properly plugged/activated (https://github.com/ansible/ansible/issues/60693).

v2.8.4
======

Release Summary
---------------

| Release Date: 2019-08-15
| `Porting Guide <https://docs.ansible.com/ansible/devel/porting_guides.html>`__


Minor Changes
-------------

- Correct the return values of matched and examined from string to int
- Fix call from "merge_dictionaries" to "_merge_dictionaries" in GcpSession object (https://github.com/ansible/ansible/issues/57140).
- Fixes comparison of list to integer in gluster_volume (https://github.com/ansible/ansible/issues/56844).
- The `podman` connection plugin now supports pipelining.
- With Python3, we cannot iterate on a dict and modify it at the same time (https://github.com/ansible/ansible/issues/54869).
- ovirt_host - update force parameter documentation (https://bugzilla.redhat.com/show_bug.cgi?id=1719271#c11)
- remove ambiguity in module naming; use "my_test" as module name

Bugfixes
--------

- Add no_log to credentials field to avoid disclosures (CVE-2019-10217)
- Do not re-use remote_user from previous loop iteration (https://github.com/ansible/ansible/issues/58876)
- Fix netconf connection command timeout issue (https://github.com/ansible/ansible/pull/58322)
- Fix strategy functions that update inventory and back 'add_host' and 'group_by' actions.
- Fixed issue where `ansible_net_model` was not being populated in iosxr_facts (https://github.com/ansible/ansible/pull/58488)
- ansible.basics - fix core C# recursive call when logging fails (e.g. if insufficient permissions are held) (https://github.com/ansible/ansible/pull/59503)
- async - Fix async callback plugins to allow async output to be displayed when running command/shell (https://github.com/ansible/ansible/issues/15988)
- aws_s3 - Improve usability when the execution host lacks MD5 support (e.g. due to FIPS-140-2).
- aws_s3 module - Improve ETag calculation, allow overwrite=always to work on FIPS-140-2
- ce_aaa_server - update to fix some bugs - When you want to delete a parameter, a conflict will occur, causing the download configuration to fail. (https://github.com/ansible/ansible/pull/60270)
- ce_aaa_server_host - update to fix some bugs - module CMD update in ansible is inconsistent with switch; when parameter is bool type, it is impossible to judge the value of expensive parameter. (https://github.com/ansible/ansible/pull/60272)
- ce_acl - update to fix some bugs - When the frag_type parameter is in the module and the configuration is repeatedly sent to the device, the module displays change = True. (https://github.com/ansible/ansible/pull/60274)
- ce_bgp_af - update to fix some bugs - XML query result error, update_cmds statement missing. (https://github.com/ansible/ansible/pull/59678)
- ce_config  - It is also necessary to undo mmi-mode enable after running commands.Otherwise it will make a effect to next tasks.(https://github.com/ansible/ansible/pull/60071).
- ce_config - Optimize multi-level views & fix a bug. (https://github.com/ansible/ansible/pull/59523)
- ce_mlag_config - update to fix some bugs - Configuration does not absent as expect. (https://github.com/ansible/ansible/pull/59336)
- ce_mtu - bug-info - unable to parse request, to fix the bug (https://github.com/ansible/ansible/pull/59343)
- ce_netstream_global - The 'get_config', which is from 'ansible.module_utils.network.cloudengine.ce', try to return the result from cache,however the configure has changed. (https://github.com/ansible/ansible/pull/59689)
- ce_netstream_global - The 'get_config', which is from 'ansible.module_utils.network.cloudengine.ce', try to return the result from cache,however the configure has changed. (https://github.com/ansible/ansible/pull/59690)
- ce_ntp_auth - update to fix "state is present but all of the following are missing-password" bug(https://github.com/ansible/ansible/pull/59344)
- ce_rollback - set mmi-mode enable to run commands and unset after running(https://github.com/ansible/ansible/pull/60075).
- ce_rollback - shouldn't load xml configure via network_cli(https://github.com/ansible/ansible/pull/59345)
- ce_startup - update to fix a bug - netconf and cli are all used to load configure at a time (https://github.com/ansible/ansible/pull/59346 )
- ce_stp - update to fix some bugs - The config of first time showing is same as second because of 'get_config', using regular to search & show config (https://github.com/ansible/ansible/pull/59347 )
- ce_vrrp - update to fix some bugs - Solving the mistake of parameter judgment, update_cmds statement missing. (https://github.com/ansible/ansible/pull/59677)
- consul_session - ``state`` parameter: use ``required_if``, document ``id`` parameter, update ``name`` parameter documentation
- docker_container - fix port bindings with IPv6 addresses.
- documented ``ignore`` option for ``TRANSFORM_INVALID_GROUP_CHARS``
- ec2_group - Don't truncate the host bits off of IPv6 CIDRs. CIDRs will be passed thru to EC2 as-is provided they are valid IPv6 representations.  (https://github.com/ansible/ansible/issues/53297)
- ec2_instance - Ensures ``ebs.volume_size`` and ``ebs.iops`` are ``int`` to avoid issues with Jinja2 templating
- facts - fixed double-counting of CPUs on POWER systems
- group - The group module errored of if the gid exists with the same group name. This prevents reruns of the playbook. This fixes a regression introduced by 4898b0a.
- nagios - Removed redundant type check which caused crashes. Guardrails added elsewhere in earlier change.
- openssh_keypair - add public key and key comment validation on change
- os_subnet - it is valid to specify an explicit ``subnetpool_id`` rather than ``use_default_subnetpool`` or ``cidr``

- ovirt_host - add event log on failure (https://github.com/oVirt/ovirt-ansible-infra/issues/8)
- ovirt_vnic_profile - fix for updating vnic profile (https://github.com/ansible/ansible/pull/56518)
- ovirt_vnic_profile - update qos and pass_through logic (https://bugzilla.redhat.com/show_bug.cgi?id=1597537)
- pbrun - add default user for become plugin (https://github.com/ansible/ansible/pull/59754)
- plugin loader - Restore adding plugin loader playbook dir to ``Playbook`` in addition to ``PlaybookCLI`` to solve sub directory playbook relative plugins to be located (https://github.com/ansible/ansible/issues/59548)
- podman_image - handle new output format for image build
- postgresql_db.py - Fix code formatting (https://github.com/ansible/ansible/pull/59497)
- postgresql_ext.py - Remove pg_quote_identifier unused import (https://github.com/ansible/ansible/pull/59497)
- postgresql_lang.py - Remove pg_quote_identifier and to_native unused imports (https://github.com/ansible/ansible/pull/59497)
- postgresql_membership - turn off the default database warning (https://github.com/ansible/ansible/pull/60043)
- postgresql_ping - turn off the default database warning (https://github.com/ansible/ansible/pull/60043)
- postgresql_slot - turn off the default database warning for slot_type physical (https://github.com/ansible/ansible/issues/60043)
- postgresql_table.py - Fix code formatting (https://github.com/ansible/ansible/pull/59497)
- postgresql_tablespace - turn off the default database warning (https://github.com/ansible/ansible/pull/60043)
- resolves CVE-2019-10206, by avoiding templating passwords from prompt as it is probable they have special characters.
- sysctl - check system values, not just sysctl.conf file, when determing state (https://github.com/ansible/ansible/pull/56153#issuecomment-514384922)
- user - do not warn when using ``local: yes`` if user already exists (https://github.com/ansible/ansible/issues/58063)
- win_domain_group_membership - Fix missing @extra_args on Get-ADObject to support dirrent domain and credentials for retrival (https://github.com/ansible/ansible/issues/57404)
- win_dsc - Be more leniant around the accepted DateTime values for backwards compatibility - https://github.com/ansible/ansible/issues/59667
- win_user - Get proper error code when failing to validate the user's credentials

v2.8.3
======

Release Summary
---------------

| Release Date: 2019-07-25
| `Porting Guide <https://docs.ansible.com/ansible/devel/porting_guides.html>`__


Minor Changes
-------------

- In ec2_eip, device_id is required when private_ip_address is set, but the reverse is not true (https://github.com/ansible/ansible/pull/55194).
- Typecast vlan id to string in nmcli module (https://github.com/ansible/ansible/issues/58949).
- Warn user about Distributed vSwitch permission in vmware_object_role_permission (https://github.com/ansible/ansible/issues/55248).
- When using `fetch_nested` fetch also list of href, instead only single object hrefs.
- dnf - set lock_timeout to a sane default (30 seconds, as is the cli)
- fix exception when tower_verify_ssl parameter is used in tower_role module (https://github.com/ansible/ansible/pull/57518).
- vApp setting can be set while VM creation in vmware_guest (https://github.com/ansible/ansible/issues/50617).
- yum - set lock_timeout to a sane default (30 seconds, as is the cli)

Bugfixes
--------

- Check when user does pass empty dict to sysprep. Fixes https://github.com/oVirt/ovirt-ansible-vm-infra/issues/104
- Do not assume None is equal as connection and become tools can have different unspecified defaults.
- Fix broken slxos_config due to changed backup options (https://github.com/ansible/ansible/pull/58804).
- Fix regression when including a role with a custom filter (https://github.com/ansible/ansible/issues/57351)
- Fixed disk already exists issue while cloning guest in vmware_guest module (https://github.com/ansible/ansible/issues/56861).
- Gather facts should use gather_subset config by default.
- Make max_connections parameter work again in vmware_guest module (https://github.com/ansible/ansible/pull/58061).
- To find specified interfaces, add a interface-type.
- To resolve NoneType error as it was missing NoneType check for l3protocol param in aci_l3out. (https://github.com/ansible/ansible/pull/58618).
- Use templated loop_var/index_var when looping include_* (https://github.com/ansible/ansible/issues/58820)
- Using neconf API to send cli commands is a bug, now fix it(https://github.com/ansible/ansible/pull/59071)
- aws_secret - Document region so the config manager can retrieve its value.
- ce_bfd_global - line284, 'data' tag of xpath should be removed. line498, add "self.existing == self.end_state" to compare the status and get 'changed'.
- ce_bfd_view - line287, line293, 'data' tag of a xpath should be removed to find a element.line500, running result judgment.
- ce_evpn_bd_vni - modify xml function to find data.(https://github.com/ansible/ansible/pull/58227)
- ce_evpn_bgp_rr - fix bugs,get wrong config, get wrong result.changed .(https://github.com/ansible/ansible/pull/58228)
- ce_interface - It is not a good way to find data from a xml tree by regular. lin379 line405.
- ce_interface - line 750,779 Some attributes of interfaces are missing, 'ifAdminStatus', 'ifDescr', 'isL2SwitchPort'.So add them when get interface status.
- ce_interface_ospf - remove the 'data' tag to fix a bug,.(https://github.com/ansible/ansible/pull/58229)
- ce_link_status - remove the 'data' tag to fix a bug,.(https://github.com/ansible/ansible/pull/58229)
- ce_netstream_aging - line318, Redundant regular. line326,line33, there may be out of array rang,some time.(https://github.com/ansible/ansible/pull/58231)
- ce_static_route The IPv6 binary system has a length of 128 bits and is grouped by 16 bits. Each group is separated by a colon ":" and can be divided into 8 groups, each group being represented by 4 hexadecimal. You can use a double colon "::" to represent a group of 0 or more consecutive 0s, but only once. Divisible compatible with Python2 and Python3. To find all elements, Data root node that is taged 'data' should be removed.(https://github.com/ansible/ansible/pull/58251)
- ce_vrrp - tag 'data' is the root node of data xml tree,remove 'data' tag to find all. line 700,747 "vrrp_group_info["adminIgnoreIfDown"]", value is string and lower case. line 1177,1240. Compare wrong! They should be same key of value to be compared.
- ce_vxlan_gateway - update the regular expression to match the more.(https://github.com/ansible/ansible/pull/58226)
- ce_vxlan_global - line 242 , bd_info is a string array,and it should be 'extend' operation. line 423, 'if' and 'else' should set a different value. if 'exist', that value is 'enable'. line 477, To get state of result, if it is changed or not.
- docker_* modules - behave better when requests errors are not caught by docker-py.
- docker_container - add support for ``nocopy`` mode for volumes.
- docker_image - validate ``tag`` option value.
- dzdo did not work with password authentication
- facts - handle situation where ``ansible_architecture`` may not be defined (https://github.com/ansible/ansible/issues/55400)
- fixed collection-based plugin loading in ansible-connection (eg networking plugins)
- gather_facts now correctly passes back the full output of modules on error and skipped, fixes
- group - properly detect duplicate GIDs when local=yes (https://github.com/ansible/ansible/issues/56481)
- ios_config - fixed issue where the "no macro" command was erroneously handled by edit_macro(). https://github.com/ansible/ansible/issues/55212
- machinectl become plugin - correct bugs which induced errors on plugin usage
- nagios module - Fix nagios module to recognize if ``cmdfile`` exists and is fifo pipe.
- nmcli - fixed regression caused by commit b7724fd, github issue
- openssl_privatekey - ``secp256r1`` got accidentally forgotten in the curve list.
- os_quota - fix failure to set compute or network quota when volume service is not available
- ovirt add host retry example to documentation BZ(https://bugzilla.redhat.com/show_bug.cgi?id=1719271)
- ovirt migrate virtual machine with state present and not only running BZ(https://bugzilla.redhat.com/show_bug.cgi?id=1722403)
- ovirt update vm migration domunetation BZ(https://bugzilla.redhat.com/show_bug.cgi?id=1724535)
- ovirt vnic profile: remove duplication in readme
- ovirt_vm - fix for module failure on creation (https://github.com/ansible/ansible/issues/59385)
- postgresql_schema - Parameter ensure replaced by state in the drop schema example (https://github.com/ansible/ansible/pull/59342)
- setup (Windows) - prevent setup module failure if Get-MachineSid fails (https://github.com/ansible/ansible/issues/47813)
- user - omit incompatible options when operating in local mode (https://github.com/ansible/ansible/issues/48722)
- vmware_guest accepts 0 MB of memory reservation, fix regression introduced via 193f69064fb40a83e3e7d2112ef24868b45233b3 (https://github.com/ansible/ansible/issues/59190).
- win_domain_user - Do not hide error and stacktrace on failures
- win_get_url - Fix proxy_url not used correctly (https://github.com/ansible/ansible/issues/58691)
- win_reg_stat - fix issue when trying to check keys in ``HKU:\`` - https://github.com/ansible/ansible/issues/59337
- yum - handle stale/invalid yum.pid lock file (https://github.com/ansible/ansible/issues/57189)

v2.8.2
======

Release Summary
---------------

| Release Date: 2019-07-03
| `Porting Guide <https://docs.ansible.com/ansible/devel/porting_guides.html>`__


Minor Changes
-------------

- Make VM name and VM UUID as mutual exclusive and required one of (https://github.com/ansible/ansible/issues/57580).
- Skip orphan VMs from inventory while running vmware_vm_inventory as VMs does not return any facts (https://github.com/ansible/ansible/pull/55929).
- dnf - Provide a better error message including python version info when installing python-dnf fails
- gcp_compute - Added additional environment variables to the ``gcp_compute`` inventory plugin to align with the rest of the ``gcp_*`` modules.
- gitlab_group - Adds missing visibility parameter to gitlab group creation
- purefa_user - change module parameter ``api_token`` to ``api`` and to stop clash with known variable.
- purefa_user - change resulting facts from ``api_token`` to ``user_api`` for clarity. An facts alias has been added, but will be removed in 2.9. (https://github.com/ansible/ansible/pull/57588)
- update ce_ntp.py and remove the root tag name to find all nodes(https://github.com/ansible/ansible/pull/56976).

Bugfixes
--------

- Bug fixes to nios_member module
- Don't return nested information in ovirt_host_facts when fetch_nested is false
- Fix --diff to produce output when creating a new file (https://github.com/ansible/ansible/issues/57618)
- Fix foreman inventory plugin when inventory caching is disabled
- Fix in netconf plugin when data element is empty in xml response (https://github.com/ansible/ansible/pull/57981)
- Fix ios_facts ansible_net_model - https://github.com/ansible/ansible/pull/58159
- Fix iosxr netconf config diff and integration test failures (https://github.com/ansible/ansible/pull/57909)
- Fix issue in resetting the storage domain lease in ovirt_vm module.
- Fix issues in iosxr integration test (https://github.com/ansible/ansible/pull/57882)
- Fix junos integration test failures (https://github.com/ansible/ansible/pull/57309)
- Fix media type of RESTCONF requests.
- Fix nxapi local failures nxos_install_os (https://github.com/ansible/ansible/pull/55993).
- Fix python3 compat issue with network/common/config.py - https://github.com/ansible/ansible/pull/55223
- Fix python3 encoding issue with iosxr_config.
- Fix regression warning on jinja2 delimiters in when statements (https://github.com/ansible/ansible/issues/56830)
- Fix the issue that disk is not activated after its creation (https://github.com/ansible/ansible/issues/57412)
- Fixed ce_bgp,first the pattern to be searched is need to change, otherwise there is no data to be found.then after running a task with this module,it will not show 'changed' correctly.
- Fixed ce_bgp_af,'changed' of module run restult is not showed, however the module run correctly,and update coommands of result is not correct.
- Fixed ce_bgp_neighbor, find specify bgp as information, as number is necessary and so on.
- Fixed ce_bgp_neighbor_af,update commands should be showed correctly, and xml for filter and edit are also re-factor as the software version upgrade and update.
- Fixes the IOS_NTP integration TC failure, where TC was failing coz of missing configuration which needed to be set before firing the TC. - https://github.com/ansible/ansible/pull/57481.
- Fixes the IOS_SMOKE integration TC failure - https://github.com/ansible/ansible/pull/57665.
- Handle improper variable substitution that was happening in safe_eval, it was always meant to just do 'type enforcement' and have Jinja2 deal with all variable interpolation. Also see CVE-2019-10156
- Only warn for bare variables if they are not type boolean (https://github.com/ansible/ansible/issues/53428)
- Remove lingering ansible vault cipher (AES) after it beeing removed in
- TaskExecutor - Create new instance of the action plugin on each iteration when using until (https://github.com/ansible/ansible/issues/57886)
- This PR fixes the issue raised where idempotency was failing when DNS bypassing was set to False and also exception error faced in nios_host_reord - https://github.com/ansible/ansible/pull/57221.
- To fix the netvisor failure with network_cli connection - https://github.com/ansible/ansible/pull/57938
- Update lib/ansible/plugins/action/ce.py.Add some modules names that modules use network_cli to connect remote hosts when connection type is 'local'
- Update ovirt vnic profile module BZ(https://bugzilla.redhat.com/show_bug.cgi?id=1597537)
- When nic has only one vnic profile use it as default or raise error (https://github.com/ansible/ansible/pull/57945)
- ce_acl - tag named data of a xpath is unnecessay for old sotfware version to find a element from xml tree, but element can not be found with 'data' tag for new version, so remove.
- ce_acl_advance - remove 'data' tag, and fix a bug that the 'changed' of result is not correct.
- ce_acl_interface - Strict regularity can't find anything.
- ce_acl_interface - do not used 'get_config' to show specific configuration, and use display command directly.
- ce_dldp - tag named data of a xpath is unnecessay for old sotfware version to find a element from xml tree, but element can not be found with 'data' tag for new version, so remove.
- ce_dldp - tag named data of a xpath is unnecessay for old sotfware version to find a element from xml tree, but element can not be found with 'data' tag for new version, so remove.
- ce_dldp_interface - tag named data of a xpath is unnecessay for old sotfware version to find a element from xml tree, but element can not be found with 'data' tag for new version, so remove.
- ce_dldp_interface - tag named data of a xpath is unnecessay for old sotfware version to find a element from xml tree, but element can not be found with 'data' tag for new version, so remove.
- ce_snmp_community - it should be 'config' end of 'edit-config', not filter that is used to 'get-config'.As well the changed state is not correct.
- ce_snmp_contact - overwrite get_config,and fix array out of range bug(line173 line183)
- ce_snmp_location - overwrite get_config.
- ce_snmp_target_host - None has no 'lower()' attribute.
- ce_snmp_target_host -do not use netconf and network_cli together in one module.
- ce_snmp_traps - overwrite get_config;do not use netconf and network_cli together in one module.
- ce_snmp_user - do not use netconf and network_cli together in one module.
- ce_vxlan_arp - override 'get_config' to show specific configuration.
- ce_vxlan_arp - override 'get_config' to show specific configuration.
- ce_vxlan_gateway - override 'get_config' to show specific configuration.
- ce_vxlan_gateway - override 'get_config' to show specific configuration.
- ce_vxlan_global - Netwrok_cli and netconf should be not mixed together, otherwise something bad will happen. Function get_nc_config uses netconf and load_config uses network_cli.
- ce_vxlan_global - Netwrok_cli and netconf should be not mixed together, otherwise something bad will happen. Function get_nc_config uses netconf and load_config uses network_cli.
- ce_vxlan_tunnel - Netwrok_cli and netconf should be not mixed together, otherwise something bad will happen. Function get_nc_config uses netconf and load_config uses network_cli.
- ce_vxlan_tunnel - Netwrok_cli and netconf should be not mixed together, otherwise something bad will happen. Function get_nc_config uses netconf and load_config uses network_cli.
- ce_vxlan_vap - tag named data of a xpath is unnecessay for old sotfware version to find a element from xml tree, but element can not be found with 'data' tag for new version, so remove.
- ce_vxlan_vap - tag named data of a xpath is unnecessay for old sotfware version to find a element from xml tree, but element can not be found with 'data' tag for new version, so remove.
- crypto modules - improve error messages when required Python library is missing.
- dellos9_facts - Fix RuntimeError on Python 3.8.
- docker_* modules - improve error message when docker-py is missing / has wrong version.
- docker_* modules - improve robustness when not handled Docker errors occur.
- docker_container - switch to ``Config`` data source for images (API>=1.21).
- docker_swarm_service - fix resource lookup if mounts.source="".
- fact_cache - Define the first_order_merge method for the legacy FactCache.update(key, value).
- facts - Restore the minor version number for CentOS and Debian.  Debian has a minor release number but doesn't put it in os-release.  CentOS doesn't have a minor version number but users want to try to match CentOS versions to RHEL equivalents so we grab the RHEL version instead.
- fix bug - out of array index.There should be a judgement about array length before the value of the array is taken out.
- ftd_configuration - fix a bug with response parsing when the server returns a list of objects
- gather_facts - Clean up tmp files upon completion (https://github.com/ansible/ansible/issues/57248)
- gather_facts - Prevent gather_facts from being verbose, just like is done in the normal action plugin for setup (https://github.com/ansible/ansible/issues/58310)
- gcp_compute - Speed up dynamic invetory up to 30x.
- gitlab_runner - Fix idempotency when creating runner (https://github.com/ansible/ansible/issues/57759)
- handlers - Only notify a handler if the handler is an exact match by ensuring `listen` is a list of strings. (https://github.com/ansible/ansible/issues/55575)
- hostname - Readded support for Cumulus Linux which broke in v2.8.0 (https://github.com/ansible/ansible/pull/57493)
- hostname - make module work on CoreOS, Oracle Linux, Clear Linux, OpenSUSE Leap, ArchARM (https://github.com/ansible/ansible/issues/42726)
- inventory_hostnames lookup - use the same order for the returned hosts as the inventory manager
- ipaddr: prevent integer indices from being parsed as ip nets (https://github.com/ansible/ansible/issues/57895).
- kubevirt: fix regression when combining `inline:` yaml with module parameters
- lineinfile - fix a race / file descriptor leak when writing the file (https://github.com/ansible/ansible/issues/57327)
- lvg - Fixed warning shown when using default value for pesize about conversion from int to str.
- meraki_network - Restructure code execution so net_id parameter works in all situations.
- na_ontap_export_policy_rule - duplicate rules created if index was not set
- na_ontap_interface - was not checking for vserver
- na_ontap_portset - Fixed issue that portset did not allow you to add port when creating a portset
- na_ontap_quotas - Fix RuntimeError on Python 3.8.
- netbox - Fix missing implementation of `groups` option (https://github.com/ansible/ansible/issues/57688)
- netbox_ip_address - Fixed issue where it would create duplicate IP addresses when trying to serialize the IP address object which doesn't have the ``.serialize()`` method. This should also prevent future duplicate objects being created if they don't have the ``.serialize()`` method as well.

- netconf - Make netconf_get python3 compatible.
- nxos_logging facilties defaults (https://github.com/ansible/ansible/pull/57144).
- nxos_vlan fix broken purge behavior (https://github.com/ansible/ansible/pull/57229).
- openssh_keypair - The fingerprint return value was incorrectly returning a list of ssh-keygen output; it now returns just the fingerprint value as a string
- openssh_keypair - make regeneration of valid keypairs with the ``force`` option possible, add better handling for invalid files
- openssl_certificate - fix Subject Alternate Name comparison, which was broken for IPv6 addresses with PyOpenSSL, or with older cryptography versions (before 2.1).
- openvswitch_bridge - The module was not properly updating the vlan when updating a bridge. This is now fixed so vlans are properly updated and tests has been put in place to check that this doesn't break again.
- option is marked as required but specifies a default.(https://github.com/ansible/ansible/pull/57257)
- os_port - handle binding:vnic_type as optional (https://github.com/ansible/ansible/issues/55524, https://github.com/ansible/ansible/issues/55525)
- podman_image_info - do not fail if invalid or non-existant image name is provided (https://github.com/ansible/ansible/issues/57899)
- postgresql - move params mapping from main to connect_to_db() function (https://github.com/ansible/ansible/pull/55799)
- postgresql_membership - Remove debug print.
- postgresql_pg_hba - After splitting fields, merge authentication options back into a single field to prevent losing options beyond the first (https://github.com/ansible/ansible/issues/57505)
- postgresql_pg_hba - Fix TypeError after which pg_hba.conf is wiped (https://github.com/ansible/ansible/issues/56430)
- postgresql_pg_hba - Fix multiple options for local type connections
- postgresql_pg_hba - Fix sorting errors between local type connections that lack a src
- postgresql_privs - Fix incorrect views handling (https://github.com/ansible/ansible/issues/27327).
- postgresql_table - fix schema handling (https://github.com/ansible/ansible/pull/57391)
- purefa_pgsnap - handle exit correctly if selected remote volume or snapshot does not exist.
- rds_instance - Fixed EnablePerformanceInsights setting (https://github.com/ansible/ansible/issues/50081)
- rds_instance no longer fails when passing neither storage_type nor iops
- remove all temporary directories created by ansible-config (https://github.com/ansible/ansible/issues/56488)
- show host_vars in ansible-inventory's --graph option.
- ssh connection plugin - Ensure that debug messages are properly encoded as text
- suppress "default will change" warnings for ``TRANSFORM_INVALID_GROUP_CHARS`` setting when non-default option value is chosen
- update acl to fix bugs.(https://github.com/ansible/ansible/pull/57268)
- update ce_facts to fix array out of range bug(https://github.com/ansible/ansible/pull/57187).
- update info-center to fix bugs.(https://github.com/ansible/ansible/pull/57269 )
- update ospf modules to fix bugs as software version changes(https://github.com/ansible/ansible/pull/56974).
- update scmp to fix bugs(https://github.com/ansible/ansible/pull/57025).
- update scmp to fix bugs.(https://github.com/ansible/ansible/pull/57264)
- update vrf to fix bugs.(https://github.com/ansible/ansible/pull/57270 )
- vault - Fix traceback using Python2 if a vault contains non-ascii characters (https://github.com/ansible/ansible/issues/58351).
- win_chocolatey - Better support detecting multiple packages installed at different versions on newer Chocolatey releases
- win_chocolatey - Install the specific Chocolatey version if the ``version`` option is set.
- win_get_url - Fix handling of restricted headers as per (https://github.com/ansible/ansible/issues/57880)
- win_pagefile - not using testPath
- win_shell - Fix bug when setting ``args.executable`` to an executable with a space

v2.8.1
======

Release Summary
---------------

| Release Date: 2019-06-06
| `Porting Guide <https://docs.ansible.com/ansible/devel/porting_guides.html>`__


Minor Changes
-------------

- Improve creating VM from template. Merge VM disks/interfaces with the template defaults.
- Remove duplicate implementation of memory reservation parameter in vmware_guest (https://github.com/ansible/ansible/issues/54335).
- Use shorter and unique random task name for scheduled task created by vmware_guest_powerstate (https://github.com/ansible/ansible/issues/56987).
- meraki_ssid - Add examples to documentation.
- rabbitmq_queue - corrected name field description
- vmware_guest now accepts Python 2 and Python 3 compatible string translate method (https://github.com/ansible/ansible/issues/54118).
- vmware_guest_disk module supports use_instance_uuid parameter since Ansible 2.8 (https://github.com/ansible/ansible/issues/56021).
- xenserver_guest - wait_for_ip_address is now ignored when state=absent (https://github.com/ansible/ansible/issues/55348).

Bugfixes
--------

- ACI - DO not encode query_string
- ACI modules - Fix non-signature authentication
- Add missing directory provided via ``--playbook-dir`` to adjacent collection loading
- Fix "Interface not found" errors when using eos_l2_interface with nonexistant interfaces configured
- Fix cannot get credential when `source_auth` set to `credential_file`.
- Fix netconf_config backup string issue (https://github.com/ansible/ansible/issues/56022)
- Fix privilege escalation support for the docker connection plugin when credentials need to be supplied (e.g. sudo with password).
- Fix vyos cli prompt inspection (https://github.com/ansible/ansible/pull/55589)
- Fixed loading namespaced documentation fragments from collections.
- Fixing bug came up after running cnos_vrf module against coverity.
- Properly handle data importer failures on PVC creation, instead of timing out.
- To fix the ios static route TC failure in CI  - https://github.com/ansible/ansible/pull/56292
- To fix the nios member module params - https://github.com/ansible/ansible/pull/54419
- To fix the nios_zone module idempotency failure  - https://github.com/ansible/ansible/pull/55595
- add terminal initial prompt for initial connection(https://github.com/ansible/ansible/pull/57057).
- allow include_role to work with ansible command
- allow python_requirements_facts to report on dependencies containing dashes
- asa_config fix <https://github.com/ansible/ansible/pull/56559>
- azure_rm_roledefinition - fix a small error in build scope. (https://github.com/ansible/ansible/pull/55797)
- azure_rm_virtualnetworkpeering - fix cross subscriptions virtual network peering. (https://github.com/ansible/ansible/pull/55854)
- cgroup_perf_recap - When not using file_per_task, make sure we don't prematurely close the perf files
- display underlying error when reporting an invalid ``tasks:`` block.
- dnf - fix wildcard matching for state: absent (https://github.com/ansible/ansible/issues/55938)
- docker connection plugin - accept version ``dev`` as 'newest version' and print warning.
- docker_container - ``oom_killer`` and ``oom_score_adj`` options are available since docker-py 1.8.0, not 2.0.0 as assumed by the version check.
- docker_container - fix network creation when ``networks_cli_compatible`` is enabled.
- docker_container - use docker API's ``restart`` instead of ``stop``/``start`` to restart a container.
- docker_image - if ``build`` was not specified, the wrong default for ``build.rm`` is used.
- docker_image - if ``nocache`` set to ``yes`` but not ``build.nocache``, the module failed.
- docker_image - module failed when ``source: build`` was set but ``build.path`` options not specified.
- docker_network module - fix idempotency when using ``aux_addresses`` in ``ipam_config``.
- ec2_instance - make Name tag idempotent (https://github.com/ansible/ansible/pull/55224)
- eos: don't fail modules without become set, instead show message and continue
- eos_config: check for session support when asked to 'diff_against: session'
- eos_eapi: fix idempotency issues when vrf was unspecified.
- fix bugs for ce - more info see
- fix incorrect uses of to_native that should be to_text instead.
- hcloud_volume - Fix idempotency when attaching a server to a volume.
- ibm_storage - Added a check for null fields in ibm_storage utils module.
- include_tasks - whitelist ``listen`` as a valid keyword (https://github.com/ansible/ansible/issues/56580)
- k8s - resource updates applied with force work correctly now
- keep results subset also when not no_log.
- kubevirt_pvc – fix regression breaking any CDI features.
- meraki_switchport - improve reliability with native VLAN functionality.
- netapp_e_iscsi_target - fix netapp_e_iscsi_target chap secret size and clearing functionality
- netapp_e_volumes - fix workload profileId indexing when no previous workload tags exist on the storage array.
- nxos_acl some platforms/versions raise when no ACLs are present (https://github.com/ansible/ansible/pull/55609).
- nxos_facts fix <https://github.com/ansible/ansible/pull/57009>
- nxos_file_copy fix passwordless workflow (https://github.com/ansible/ansible/pull/55441).
- nxos_interface Fix admin_state check for n6k (https://github.com/ansible/ansible/pull/55673).
- nxos_snmp_traps fix group all for N35 platforms (https://github.com/ansible/ansible/pull/55995).
- nxos_snmp_user fix platform fixes for get_snmp_user (https://github.com/ansible/ansible/pull/55832).
- nxos_vlan mode idempotence bug (https://github.com/ansible/ansible/pull/55144).
- nxos_vlan vlan names containing regex ctl chars should be escaped (https://github.com/ansible/ansible/pull/55463).
- nxos_vtp_* modules fix n6k issues (https://github.com/ansible/ansible/pull/55737).
- openssl_certificate - fix private key passphrase handling for ``cryptography`` backend.
- openssl_pkcs12 - fixes crash when private key has a passphrase and the module is run a second time.
- os_stack - Apply tags conditionally so that the module does not throw up an error when using an older distro of openstacksdk (https://github.com/ansible/ansible/pull/56710)
- pass correct loading context to persistent connections other than local
- pkg_mgr - Ansible 2.8.0 failing to install yum packages on Amazon Linux (https://github.com/ansible/ansible/issues/56583)
- postgresql - added initial SSL related tests
- postgresql - added missing_required_libs, removed excess param mapping
- postgresql - move connect_to_db and get_pg_version into module_utils/postgres.py (https://github.com/ansible/ansible/pull/55514)
- postgresql_db - add note to the documentation about state dump and the incorrect rc (https://github.com/ansible/ansible/pull/57297)
- postgresql_db - fix for postgresql_db fails if stderr contains output (https://github.com/ansible/ansible/issues/56703)
- postgresql_ping - fixed a typo in the module documentation (https://github.com/ansible/ansible/pull/56608)
- preserve actual ssh error when we cannot connect.
- route53_facts - the module did not advertise check mode support, causing it not to be run in check mode.
- sysctl: the module now also checks the output of STDERR to report if values are correctly set (https://github.com/ansible/ansible/pull/55695)
- ufw - correctly check status when logging is off (https://github.com/ansible/ansible/issues/56674)
- uri - always return a value for status even during failure (https://github.com/ansible/ansible/issues/55897)
- urls - Handle redirects properly for IPv6 address by not splitting on ``:`` and rely on already parsed hostname and port values (https://github.com/ansible/ansible/issues/56258)
- vmware_vm_facts - fix the support with regular ESXi
- vyos_interface fix <https://github.com/ansible/ansible/pull/57169>
- we don't really need to template vars on definition as we do this on demand in templating.
- win_acl - Fix qualifier parser when using UNC paths - https://github.com/ansible/ansible/issues/55875
- win_hostname - Fix non netbios compliant name handling (https://github.com/ansible/ansible/issues/55283)
- winrm - Fix issue when attempting to parse CLIXML on send input failure
- xenserver_guest - fixed an issue where VM whould be powered off even though check mode is used if reconfiguration requires VM to be powered off.
- xenserver_guest - proper error message is shown when maximum number of network interfaces is reached and multiple network interfaces are added at once.
- yum - Fix false error message about autoremove not being supported (https://github.com/ansible/ansible/issues/56458)
- yum - fix failure when using ``update_cache`` standalone (https://github.com/ansible/ansible/issues/56638)
- yum - handle special "_none_" value for proxy in yum.conf and .repo files (https://github.com/ansible/ansible/issues/56538)

v2.8.0
======

Release Summary
---------------

| Release Date: 2019-05-16
| `Porting Guide <https://docs.ansible.com/ansible/devel/porting_guides.html>`__


Major Changes
-------------

- Experimental support for Ansible Collections and content namespacing - Ansible content can now be packaged in a collection and addressed via namespaces. This allows for easier sharing, distribution, and installation of bundled modules/roles/plugins, and consistent rules for accessing specific content via namespaces.
- Python interpreter discovery - The first time a Python module runs on a target, Ansible will attempt to discover the proper default Python interpreter to use for the target platform/version (instead of immediately defaulting to ``/usr/bin/python``). You can override this behavior by setting ``ansible_python_interpreter`` or via config. (see https://github.com/ansible/ansible/pull/50163)
- become - The deprecated CLI arguments for ``--sudo``, ``--sudo-user``, ``--ask-sudo-pass``, ``-su``, ``--su-user``, and ``--ask-su-pass`` have been removed, in favor of the more generic ``--become``, ``--become-user``, ``--become-method``, and ``--ask-become-pass``.
- become - become functionality has been migrated to a plugin architecture, to allow customization of become functionality and 3rd party become methods (https://github.com/ansible/ansible/pull/50991)

Minor Changes
-------------

- A k8s module defaults group has now been added to reduce the amount of parameters required for multiple k8s tasks. This group contains all non-deprecated kubernetes modules - `k8s`, `k8s_auth`, `k8s_facts`, `k8s_scale` and `k8s_service` as well as the CRD-handling `kubevirt_*` modules.
- AWS EC2's Autoscaling Group (`ec2_asg`) module now supports the use of Launch Templates in addition to existing support for Launch Configurations.
- Add ``ansible_play_name`` magic var (https://github.com/ansible/ansible/issues/11349)
- Add better parsing for gathering facts about free memory in Mac OS (https://github.com/ansible/ansible/pull/52917).
- Add config option for chroot binary for chroot connection plugin
- Add configurable backup path option support for network config modules
- Add examples in documentation to explain how to handle multiple conditions in changed_when and failed_when.
- Add new meta task end_host - https://github.com/ansible/ansible/issues/40904
- Add option to read zabbix inventory per each host
- Add option to set ansible_ssh_host based on first interface settings
- Add parameters to module vmware_guest for conversion of disk to thin or thick when vm is cloned or deployed with template or virtual machine.
- Add stats on rescued/ignored tasks to play recap (https://github.com/ansible/ansible/pull/48418)
- Add support for hex color values in Slack module.
- Add support for per_host:no stats for the callback plugin **json** (https://github.com/ansible/ansible/pull/43123)
- Add variable type for performance_insights_retention_period (https://github.com/ansible/ansible/issues/49904).
- Add warning about falling back to jinja2_native=false when Jinja2 version is lower than 2.10.
- Added Ansible.Basic C# util that contains a module wrapper and handles common functions like argument parsing and module return. This is gives the user more visibility over what the module has run and aligns PowerShell modules more closely to how Python modules are defined.
- Added check for assert module for msg and failed_msg as a list or string types.
- Added documentation about the folder parameter with examples in vmware_deploy_ovf (https://github.com/ansible/ansible/issues/51825).
- Added documentation about using VMware dynamic inventory plugin.
- Added experimental support for connecting to Windows hosts over SSH using ``ansible_shell_type=cmd`` or ``ansible_shell_type=powershell``
- Added missing deprecation warning for param 'reboot' and use without param 'name' to the cron module.
- Added parameter checking before the module attempts to do an action to give helpful error message
- Added support for MX and SRV record in ipa_dnsrecord module (https://github.com/ansible/ansible/pull/42482).
- Added support for gateway parameter in iptables module (https://github.com/ansible/ansible/issues/53170).
- Added support for iptables module iprange and its parameters src-range and dst-range
- All environment variables defined by ansible now start with the `ANSIBLE_` prefix.  The old environment vars still work for now.  The new environment vars added are: ANSIBLE_LIBVIRT_LXC_NOSECLABEL, ANSIBLE_DISPLAY_SKIPPED_HOSTS, and ANSIBLE_NETWORK_GROUP_MODULES
- Allow default callback plugin to send unreachable host/task to stderr using toggle flag.
- Allow for vaulted templates in template lookup (https://github.com/ansible/ansible/issues/34209)
- An `os` module_defaults group has been added to simplify parameters for multiple OpenStack tasks.  This group includes all OpenStack modules with an `os_`-prefixed module name.
- Ansible.ModuleUtils.Privilege - moved C# code to it's own util called ``Ansible.Privilege`` and expanded the tests
- Catch all connection timeout related exceptions and raise AnsibleConnectionError instead
- Change the position to search os-release since clearlinux new versions are providing /etc/os-release too
- Changed output of tags dictionary in results to standard Ansible format
- Cleaned up module code to remove all calls to the deprecated get_exception() function
- Connection plugins have been standardized to allow use of ``ansible_<conn-type>_user`` and ``ansible_<conn-type>_password`` variables.  Variables such as ``ansible_<conn-type>_pass`` and ``ansible_<conn-type>_username`` are treated with lower priority than the standardized names and may be deprecated in the future.  In general, the ``ansible_user`` and ``ansible_password`` vars should be used unless there is a reason to use the connection-specific variables.
- Display - Add a ``Singleton`` metaclass and apply it to ``Display`` to remove the need of using ``__main__.Display`` as a pseudo singleton
- Drop the use of pkg_resources.  Importing pkg_resources was the costliest part of startup time for Ansible.  pkg_resources was used so that platforms with old versions of PyCrypto and Jinja2 could use parallel installed, updated versions.  Since we no longer support Python-2.6 on the controller side, we no longer have to support parallel installation to work around those old stacks.
- Embed an overridable static sanitization method into base inventory plugin class to allow individual plugins to optionally override Add override implementation to inital set of cloud plugins
- Ensures 'elapsed' is always returned, when timed out or failed
- Fix API call to _wait_for_response in k8s modules (https://github.com/ansible/ansible/pull/53937).
- Fix documentation of match test. Match requires zero or more characters at beginning of the string.
- Fixed bug around populating host_ip in hostvars in vmware_vm_inventory.
- Gather NVMe NQN fact (https://github.com/ansible/ansible/pull/50164)
- Handle vault filename with UTF-8 while decrypting vault file using ansible-vault.
- Improve the deprecation message for squashing, to not give misleading advice
- Increase the default persistent command_timeout value from 10 to 30 seconds to reduce frequent timeout issues.
- Modules and plugins have been standardized on a well-defined set of TLS-related parameters.  The old names remain as aliases for compatibility. In general, the new names will override the old names if both are specified. The standard names are: ``client_cert`` (certificate for client identity, might also include the private key), ``client_key`` (private key for ``client_cert``), ``ca_cert`` (public key to validate server's identity, usually a root certificate), and ``validate_certs`` (boolean to enable or disable certificate validity checking).
- Moved the FactCache code from ansible.plugins.cache.FactCache to ansible.vars.fact_cache.FactCache as it is not meant to be used to implement cache plugins.
- Now emits 'elapsed' as a return value for get_url, uri and win_uri
- On Solaris, the `ansible_product_name` fact is populated for a wider range of older hardware models, and `ansible_system_vendor` fact is populated for certain known vendors.
- Parsing plugin filter may raise TypeError, gracefully handle this exception and let user know about the syntax error in plugin filter file.
- Python-3.8 removes platform.dist() from the standard library. To maintain compatibility we've switched to an alternative library, nir0s/distro, to detect the distribution for fact gathering.  Distributions facts may change slightly as nir0s/distro has bugfixes which the standard library's platform.dist() has lacked.
- Raise AnsibleConnectionError on winrm connection errors
- Refactored the CLI code to parse the CLI arguments and then save them into a non-mutatable global singleton.  This should make it easier to modify.
- Removed the private ``_options`` attribute of ``CallbackBase``.  See the porting guide if you need access to the command line arguments in a callback plugin.
- Support for Cumulus Linux 2.5.4 and 3.7.3 added in setup facts (https://github.com/ansible/ansible/pull/52309).
- Support for Linux Mint 18.3 added in setup facts (https://github.com/ansible/ansible/pull/52224).
- The ``acme_account_facts`` module has been renamed to ``acme_account_info``.
- The ``docker_image_facts`` module has been renamed to ``docker_image_info``.
- The ``docker_service`` module has been renamed to ``docker_compose``.
- The restart/idempotency behavior of docker_container can now be controlled with the new comparisons parameter.
- Try to use bundled urllib3 first, then falls back to non-bundled version in vmware_tools (https://github.com/ansible/ansible/pull/55187).
- Update docs and return section of vmware_host_service_facts module.
- Updated Ansible version help message in help section.
- Updated VMware Update tag API as new specifications (https://github.com/ansible/ansible/issues/53060).
- Windows/PSRP - Ensure that a connection timeout or connection error results in host being unreachable
- ``contains`` jinja2 test - Add a ``contains`` jinja2 test designed for use in ``select``, ``reject``, ``selectattr`` or ``rejectattr`` filters (https://github.com/ansible/ansible/pull/45798)
- ``osx_say`` callback plugin was renamed into ``say``.
- ``to_yaml`` filter updated to maintain formatting consistency when used with ``pyyaml`` versions 5.1 and later (https://github.com/ansible/ansible/pull/53772)
- acme_account: add support for diff mode.
- acme_account_facts: also return ``public_account_key`` in JWK format.
- acme_certificate - add experimental support for IP address identifiers.
- acme_challenge_cert_helper - add support for IP address identifiers.
- add ``STRING_CONVERSION_ACTION`` option to warn, error, or ignore when a module parameter is string type but the value from YAML is not a string type and it is converted (https://github.com/ansible/ansible/issues/50503)
- add facility for playbook attributes that are not templatable, i.e register
- add from_handlers option to include_role/import_role
- add option to azure_rm inventory plugin which will allow the legacy script host names to be used
- add option to shell/command to control stripping of empty lines at end of outputs
- add parameter to checkpoint_object_facts to filter out by object type
- add support for extending volumes in os_volume, also add module support for check_mode and diff
- add toggle to allow user to override invalid group character filter
- added 'unsafe' keyword to vars_prompt so users can signal 'template unsafe' content
- adds launch type to ecs task to support fargate launch type.
- allow user to force install a role and it's dependencies
- allow user to force verbose messages to stderr
- ansible facts properly detect xen paravirt vs hvm
- ansible-galaxy: properly warn when git isn't found in an installed bin path instead of traceback
- ansible.vars.unsafe_proxy - Removed deprecated file (https://github.com/ansible/ansible/issues/45040)
- assert - added ``quiet`` option to the ``assert`` module to avoid verbose output (https://github.com/ansible/ansible/issues/27124).
- aws_kms is now able to create keys and manage grants and tags
- azure_rm_appgateway - add redirect configurations and probes
- become - Change the default value for `AGNOSTIC_BECOME_PROMPT` to `True` so become prompts display `BECOME password:` regardless of the become method used. To display the become method in the prompt (for example, `SUDO password:`), set this config option to `False`.
- callbacks - New ``v2_runner_on_start`` callback added to indicate the start of execution for a host in a specific task (https://github.com/ansible/ansible/pull/47684)
- change default connection plugin on macOS when using smart mode to ssh instead of paramiko (https://github.com/ansible/ansible/pull/54738)
- change default value for ``configs`` from ``[]`` to ``null`` and for ``update_order`` from ``stop-first`` to ``null``, matching docker API and allowing the module to interact with older docker daemons.
- cloudstack - The choice list for the param 'hypervisor' had been removed to allow the API to validate depending on your setup directly.
- cmdline fact parsing can return multiple values of a single key. Deprecate cmdline fact in favor of proc_cmdline.
- command/shell - new `stdin_add_newline` arg allows suppression of automatically-added newline `\n` character to the specified in the `stdin` arg.
- conn_limit type is set to 'int' in postgresql_user module. This will allow module to compare conn_limit with record value without type casting.
- copy - support recursive copying with remote_src
- cs_network_offering - new for_vpc parameter which allows the creation of network offers for VPC.
- cs_volume - add volumes extraction and upload features.
- cs_zone - The option network_type uses capitalized values for the types e.g. 'Advanced' and 'Basic' to match the return from the API.
- default value for ``INVENTORY_ENABLED`` option was ``['host_list', 'script', 'yaml', 'ini', 'toml', 'auto']`` and is now ``['host_list', 'script', 'auto', 'yaml', 'ini', 'toml']``
- diff mode outputs in YAML form when used with yaml callback plugin
- dnf - added the module option ``install_weak_deps`` to control whether DNF will install weak dependencies
- dnf - group removal does not work if group was installed with Ansible because of dnf upstream bug https://bugzilla.redhat.com/show_bug.cgi?id=1620324
- dnf appropriately handles disable_excludes repoid argument
- dnf module now supports loading substitution overrides from the installroot
- dnf module properly load and initialize dnf package manager plugins
- dnf properly honor disable_gpg_check for local (on local disk of remote node) package installation
- dnf properly support modularity appstream installation via overloaded group modifier syntax
- dnf removal with wildcards now works: Fixes https://github.com/ansible/ansible/issues/27744
- docker_container - Add runtime option.
- docker_container - Add support for device I/O rate limit parameters. This includes ``device_read_bps``, ``device_write_bps``, ``device_read_iops`` and ``device_write_iops``
- docker_container - Added support for ``pids_limit`` parameter in docker_container.
- docker_container - Added support for healthcheck.
- docker_container - Allow to use image ID instead of image name.
- docker_container - ``stop_timeout`` is now also used to set the ``StopTimeout`` property of the docker container when creating the container.
- docker_container - a new option ``networks_cli_compatible`` with default value ``no`` has been added. The default value will change to ``yes`` in Ansible 2.12. Setting it to ``yes`` lets the module behave similar to ``docker create --network`` when at least one network is specified, i.e. the default network is not automatically attached to the container in this case.
- docker_container - improved ``diff`` mode to show output.
- docker_container - mount modes in ``volumes`` allow more values, similar to when using the ``docker`` executable.
- docker_container - published_ports now supports port ranges, IPv6 addresses, and no longer accepts hostnames, which were never used correctly anyway.
- docker_container, docker_network, docker_volume - return facts as regular variables ``container``, ``network`` respectively ``volume`` additionally to facts. This is now the preferred way to obtain results. The facts will be removed in Ansible 2.12.
- docker_image - Add ``build.cache_from`` option.
- docker_image - Allow to use image ID instead of image name for deleting images.
- docker_image - add option ``build.use_proxy_config`` to pass proxy config from the docker client configuration to the container while building.
- docker_image - all build-related options have been moved into a suboption ``build``. This affects the ``dockerfile``, ``http_timeout``, ``nocache``, ``path``, ``pull``, ``rm``, and ``buildargs`` options.
- docker_image - set ``changed`` to ``false`` when using ``force: yes`` to load or build an image that ends up being identical to one already present on the Docker host.
- docker_image - set ``changed`` to ``false`` when using ``force: yes`` to tag or push an image that ends up being identical to one already present on the Docker host or Docker registry.
- docker_image - the ``force`` option has been deprecated; more specific options ``force_source``, ``force_absent`` and ``force_tag`` have been added instead.
- docker_image - the ``source`` option has been added to clarify the action performed by the module.
- docker_image - the default for ``build.pull`` will change from ``yes`` to ``no`` in Ansible 2.12. Please update your playbooks/roles now.
- docker_image - the deprecated settings ``state: build`` and ``use_tls`` now display warnings when being used. They will be removed in Ansible 2.11.
- docker_image_facts - Allow to use image ID instead of image name.
- docker_network - Add support for IPv6 networks.
- docker_network - Minimum docker API version explicitly set to ``1.22``.
- docker_network - Minimum docker server version increased from ``1.9.0`` to ``1.10.0``.
- docker_network - Minimum docker-py version increased from ``1.8.0`` to ``1.10.0``.
- docker_network - ``attachable`` is now used to set the ``Attachable`` property of the docker network during creation.
- docker_network - ``internal`` is now used to set the ``Internal`` property of the docker network during creation.
- docker_network - ``scope`` is now used to set the ``Scope`` property of the docker network during creation.
- docker_network - add new option ``ipam_driver_options``.
- docker_network - added support for specifying labels
- docker_network - changed return value ``diff`` from ``list`` to ``dict``; the original list is contained in ``diff.differences``.
- docker_network - improved ``diff`` mode to show output.
- docker_secret - ``data`` can now accept Base64-encoded data via the new ``data_is_b64`` option. This allows to pass binary data or JSON data in unmodified form. (https://github.com/ansible/ansible/issues/35119)
- docker_service - return results as regular variable ``services``; this is a dictionary mapping service names to container dictionaries. The old ansible facts are still returned, but it is recommended to use ``register`` and ``services`` in the future. The facts will be removed in Ansible 2.12.
- docker_swarm - Added support for ``default_addr_pool`` and ``subnet_size``.
- docker_swarm - ``UnlockKey`` will now be returned when ``autolock_managers`` is ``true``.
- docker_swarm - module now supports ``--diff`` mode.
- docker_swarm_service - Add option ``limits`` as a grouper for resource limit options.
- docker_swarm_service - Add option ``logging`` as a grouper for logging options.
- docker_swarm_service - Add option ``placement`` as a grouper for placement options.
- docker_swarm_service - Add option ``reservations`` as a grouper for resource reservation options.
- docker_swarm_service - Add option ``restart_config`` as a grouper for restart options.
- docker_swarm_service - Add option ``update_config`` as a grouper for update options.
- docker_swarm_service - Added option ``resolve_image`` which enables resolving image digests from registry to detect and deploy changed images.
- docker_swarm_service - Added support for ``command`` parameter.
- docker_swarm_service - Added support for ``env_files`` parameter.
- docker_swarm_service - Added support for ``groups`` parameter.
- docker_swarm_service - Added support for ``healthcheck`` parameter.
- docker_swarm_service - Added support for ``hosts`` parameter.
- docker_swarm_service - Added support for ``rollback_config`` parameter.
- docker_swarm_service - Added support for ``stop_grace_period`` parameter.
- docker_swarm_service - Added support for ``stop_signal`` parameter.
- docker_swarm_service - Added support for ``working_dir`` parameter.
- docker_swarm_service - Added support for passing period as string to ``restart_policy_delay``.
- docker_swarm_service - Added support for passing period as string to ``restart_policy_window``.
- docker_swarm_service - Added support for passing period as string to ``update_delay``.
- docker_swarm_service - Added support for passing period as string to ``update_monitor``.
- docker_swarm_service - Extended ``mounts`` options. It now also accepts ``labels``, ``propagation``, ``no_copy``, ``driver_config``, ``tmpfs_size``, ``tmpfs_mode``.
- docker_swarm_service - ``env`` parameter now supports setting values as a dict.
- docker_swarm_service - added ``diff`` mode.
- docker_swarm_service: use docker defaults for the ``user`` parameter if it is set to ``null``
- docker_volume - changed return value ``diff`` from ``list`` to ``dict``; the original list is contained in ``diff.differences``.
- docker_volume - improved ``diff`` mode to show output.
- docker_volume - option minimal versions now checked. (https://github.com/ansible/ansible/issues/38833)
- docker_volume - reverted changed behavior of ``force``, which was released in Ansible 2.7.1 to 2.7.5, and Ansible 2.6.8 to 2.6.11. Volumes are now only recreated if the parameters changed **and** ``force`` is set to ``true`` (instead of or). This is the behavior which has been described in the documentation all the time.
- docker_volume - the ``force`` option has been deprecated, and a new option ``recreate`` has been added with default value ``never``. If you use ``force: yes`` in a playbook, change it to ``recreate: options-changed`` instead.
- ecs_service - adds support for service_registries and scheduling_strategies. desired_count may now be none to support scheduling_strategies
- facts - Alias ``ansible_model`` to ``ansible_product_name`` to more closely match other OSes (https://github.com/ansible/ansible/issues/52233)
- fetch - Removed deprecated validate_md5 alias (https://github.com/ansible/ansible/issues/45039)
- fix yum and dnf autoremove input sanitization to properly warn user if invalid options passed and update documentation to match
- gather Fibre Channel WWNs fact (https://github.com/ansible/ansible/pull/37043)
- gather Fibre Channel WWNs fact on AIX (extends https://github.com/ansible/ansible/pull/37043)
- gcp_compute - add the image field to map to disk source iamges in the configured zones bringing it in line with old gce inventory script data
- hashi_vault lookup plugin now supports username and password method for the authentication (https://github.com/ansible/ansible/issues/38878).
- identity - Added support for GSSAPI authentication for the FreeIPA modules. This is enabled by either using the KRB5CCNAME or the KRB5_CLIENT_KTNAME environment variables when calling the ansible playbook. Note that to enable this feature, one has to install the urllib_gssapi python library.
- include better error handling for Windows errors to help with debugging module errors
- include/import - Promote ``include_tasks``, ``import_tasks``, ``include_role``, and ``import_role`` to ``stableinterface``
- include_role/import_role - Removed deprecated private argument (https://github.com/ansible/ansible/issues/45038)
- influxdb_user - Implemented the update of the admin role of a user
- inheritance - Improve ``FieldAttribute`` inheritance, by using a sentinel instead of ``None`` to indicate that the option has not been explicitly set
- inventory - added new TOML inventory plugin (https://github.com/ansible/ansible/pull/41593)
- inventory keyed_groups - allow the parent_group to be specified as a variable by using brackets, such as "{{ placement.region }}", or as a string if brackets are not used.
- inventory plugins - Inventory plugins that support caching can now use any cache plugin shipped with Ansible.
- inventory/docker - Group containers by docker-swarm "service" and "stack"
- jenkins_plugin - Set new default value for the update_url parameter (https://github.com/ansible/ansible/issues/52086)
- jinja2 - Add ``now()`` function for getting the current time
- jinja2 - accesses to attributes on an undefined value now return further undefined values rather than throwing an exception
- jinja2 - accesses to keys/indices on an undefined value now return further undefined values rather than throwing an exception
- junit callback plug-in - introduce a new option to consider a task only as test case if it has this value as prefix.
- junit callback plug-in - introduce a new option to hide task arguments similar to no_log.
- k8s - add ability to wait for some kinds of Kubernetes resources to be in the desired state
- k8s - add validate parameter to k8s module to allow resources to be validated against their specification
- k8s - append_hash parameter adds a hash to the name of ConfigMaps and Secrets for easier immutable resources
- keyed_groups now has a 'parent_group' keyword that allows assigning all generated groups to the same parent group
- loop - expose loop var name as ``ansible_loop_var``
- loop_control - Add new ``extended`` option to return extended loop information (https://github.com/ansible/ansible/pull/42134)
- loop_control's pause now allows for fractions of a second
- macports - add upgrade parameter and replace update_ports parameter with selfupdate (https://github.com/ansible/ansible/pull/45049)
- magic variables - added a new ``ansible_dependent_role_names`` magic variable to contain the names of roles applied to the host indirectly, via dependencies.
- magic variables - added a new ``ansible_play_role_names`` magic variable to mimic the old functionality of ``role_names``. This variable only lists the names of roles being applied to the host directly, and does not include those added via dependencies
- magic variables - added a new ``ansible_role_names`` magic variable to include the names of roles being applied to the host both directly and indirectly (via dependencies).
- mattstuff filter - fix py3 scope for unique filter errors
- meraki_device - Add support for attaching notes to a device.
- meraki_network - type parameter no longer accepts combined. Instead, the network types should be specified in a list.
- mongodb_user - Change value for parameter roles to empty (https://github.com/ansible/ansible/issues/46443)
- more complete information when pear module has an error message
- mount - make last two fields optional (https://github.com/ansible/ansible/issues/43855)
- moved some operations to inside VariableManager to make using it simpler and slightly optimized, but creating API changes
- now galaxy shows each path where it finds roles when listing them
- npm ci feature added which allows to install a project with a clean slate: https://docs.npmjs.com/cli/ci.html
- openssl_certificate - Add support for relative time offsets in the ``selfsigned_not_before``/``selfsigned_not_after``/``ownca_not_before``/``ownca_not_after`` and ``valid_in`` parameters.
- openssl_certificate - add ``backup`` option.
- openssl_certificate - change default value for ``acme_chain`` from ``yes`` to ``no``. Current versions of `acme-tiny <https://github.com/diafygi/acme-tiny/>`_ do not support the ``--chain`` command anymore. This default setting caused the module not to work with such versions of acme-tiny until ``acme_chain: no`` was explicitly set.
- openssl_certificate - now works with both PyOpenSSL and cryptography Python libraries. Autodetection can be overridden with ``select_crypto_backend`` option.
- openssl_certificate - the messages of the ``assertonly`` provider with respect to private key and CSR checking are now more precise.
- openssl_csr - add ``backup`` option.
- openssl_csr - add ``useCommonNameForSAN`` option which allows to disable using the common name as a SAN if no SAN is specified.
- openssl_csr - now works with both PyOpenSSL and cryptography Python libraries. Autodetection can be overridden with ``select_crypto_backend`` option.
- openssl_dhparam - add ``backup`` option.
- openssl_pkcs12 - Fixed idempotency checks, the module will regenerate the pkcs12 file if any of the parameters differ from the ones in the file. The ``ca_certificates`` parameter has been renamed to ``other_certificates``. 
- openssl_pkcs12 - add ``backup`` option.
- openssl_pkcs12, openssl_privatekey, openssl_publickey - These modules no longer delete the output file before starting to regenerate the output, or when generating the output failed.
- openssl_privatekey - add ``backup`` option.
- openssl_privatekey - now works with both PyOpenSSL and cryptography Python libraries. Autodetection can be overridden with ``select_crypto_backend`` option.
- openssl_publickey - add ``backup`` option.
- os_server_facts - added all_projects option to gather server facts from all available projects
- package_facts, now supports multiple package managers per system. New systems supported include Gentoo's portage with portage-utils installed, as well as FreeBSD's pkg
- pamd: remove description from RETURN values as it is unnecessary
- paramiko is now optional.  There is no compat package on certain platforms to worry about.
- postgres_privs now accepts 'ALL_IN_SCHEMA' objs for 'function' type (https://github.com/ansible/ansible/pull/35331).
- postgresql_db - Added paramter conn_limit to limit the number of concurrent connection to a certain database
- postgresql_privs - add fail_on_role parameter to control the behavior (fail or warn) when target role does not exist.
- postgresql_privs - introduces support for FOREIGN DATA WRAPPER and FOREIGN SERVER as object types in postgresql_privs module. (https://github.com/ansible/ansible/issues/38801)
- postgresql_privs - introduces support to postgresql_privs to use 'FOR { ROLE | USER } target_role' in 'ALTER DEFAULT PRIVILEGES'. (https://github.com/ansible/ansible/issues/50877)
- reboot - Expose timeout value in error message
- reboot - add parameter for specifying paths to search for the ``shutdown`` command (https://github.com/ansible/ansible/issues/51190)
- regex_escape - added re_type option to enable escaping POSIX BRE chars

This distinction is necessary because escaping non-special chars such as
'(' or '{' turns them into special chars, the opposite of what is intended
by using regex_escape on strings being passed as a Basic Regular
Expression.

- rename safeConfigParser to ConfigParser to suppress DeprecationWarning (The SafeConfigParser class has been renamed to ConfigParser in Python 3.2.)
- renamed `dellemc_idrac_firmware` module to `idrac_firmware`
- retry_files_enabled now defaults to False instead of True.
- run_command - Add a new keyword argument expand_user_and_vars, which defaults to True, allowing the module author to decide whether or paths and variables are expanded before running the command when use_unsafe_shell=False (https://github.com/ansible/ansible/issues/45418)
- s3_bucket - Walrus users: ``s3_url`` must be a FQDN without scheme not path.
- s3_bucket - avoid failure when ``policy``, ``requestPayment``, ``tags`` or ``versioning`` operations aren't supported by the endpoint and related parameters aren't set
- service_facts - provide service state and status information about disabled systemd service units
- setup - gather iSCSI facts for HP-UX (https://github.com/ansible/ansible/pull/44644)
- slack: Explicitly set Content-Type header to "application/json" for improved compatibility with non-Slack chat systems
- sns - Ported to boto3 and added support for additional protocols
- spotinst - Added "SPOTINST_ACCOUNT_ID" or "ACCOUNT" env var
- spotinst - Added Instance Health Check Validation on creation of Elastigroup if "health_check_type" parameter set in playbook
- synchronize module - Warn when the empty string is present in rsync_opts as it is likely unexpected that it will transfer the current working directory.
- tower_credential - Expect ssh_key_data to be the content of a ssh_key file instead of the path to the file (https://github.com/ansible/ansible/pull/45158)
- tower_project - getting project credential falls back to project organization if there's more than one cred with the same name
- ufw - ``proto`` can now also be ``gre`` and ``igmp``.
- ufw - enable "changed" status while check mode is enabled
- ufw - new ``insert_relative_to`` option allows to specify rule insertion position relative to first/last IPv4/IPv6 address.
- ufw - type of option ``insert`` is now enforced to be ``int``.
- uri/urls - Support unix domain sockets (https://github.com/ansible/ansible/pull/43560)
- use ansible.module_utils.six for all scripts in contrib/inventory
- vmware_deploy_ovf - Add support for 'inject_ovf_env' for injecting user input properties in OVF environment.
- vmware_portgroup accepts list of ESXi hostsystem. Modified get_all_host_objs API to accept list of hostsystems.
- when showing defaults for CLI options in manpage/docs/--help avoid converting paths
- win_chocolatey - Added the ability to pin a package using the ``pinned`` option - https://github.com/ansible/ansible/issues/38526
- win_chocolatey - added the allow_multiple module option to allow side by side installs of the same package
- win_chocolatey - support bootstrapping Chocolatey from other URLs with any PS script that ends with ``.ps1``, originally this script had to be ``install.ps1``
- win_dsc - Display the warnings produced by the DSC engine for better troubleshooting - https://github.com/ansible/ansible/issues/51543
- win_dsc - The Verbose logs will be returned when running with ``-vvv``.
- win_dsc - The module invocation and possible options will be displayed when running with ``-vvv``.
- win_dsc - The win_dsc module will now fail if an invalid DSC property is set.
- win_get_url - Add idempotency check if the remote file has the same contents as the dest file.
- win_get_url - Add the ``checksum`` option to verify the integrity of a downloaded file.
- win_nssm - Add support for check and diff modes.
- win_nssm - Add the ``executable`` option to specify the location of the NSSM utility.
- win_nssm - Add the ``working_directory``, ``display_name`` and ``description`` options.
- win_nssm - Change default value for ``state`` from ``start`` to ``present``.
- win_package - added the ``chdir`` option to specify the working directory used when installing and uninstalling a package.
- win_psmodule - The ``url`` parameter is deprecated and will be removed in Ansible 2.12. Use the ``win_psrepository`` module to manage repositories instead
- win_say - If requested voice is not found a warning is now displayed.
- win_say - Ported code to use Ansible.Basic.
- win_say - Some error messages worded differently now that the module uses generic module parameter validation.
- win_scheduled_task - defining a trigger repetition as an array is deprecated and will be removed in Ansible 2.12. Define the repetition as a dictionary instead.
- win_script - added support for running a script with become
- win_security_policy - warn users to use win_user_right instead when editing ``Privilege Rights``
- win_shortcut - Added support for setting the ``Run as administrator`` flag on a shortcut pointing to an executable
- win_stat - added the ``follow`` module option to follow ``path`` when getting the file or directory info
- win_updates - Reworked filtering updates based on category classification - https://github.com/ansible/ansible/issues/45476
- windows async - async directory is now controlled by the ``async_dir`` shell option and not ``remote_tmp`` to match the POSIX standard.
- windows async - change default directory from ``$env:TEMP\.ansible_async`` to ``$env:USERPROFILE\.ansible_async`` to match the POSIX standard.
- windows become - Add support for passwordless become.
- windows become - Moved to shared C# util so modules can utilize the code.
- xml - Introduce ``insertbefore`` and ``insertafter`` to specify the position (https://github.com/ansible/ansible/pull/44811)
- yum - provide consistent return data structure when run in check mode and not in check mode
- yum - when checking for updates, now properly include Obsoletes (both old and new) package data in the module JSON output, fixes https://github.com/ansible/ansible/issues/39978
- yum and dnf can now handle installing packages from URIs that are proxy redirects and don't end in the .rpm file extension
- yum and dnf can now perform C(update_cache) as a standalone operation for consistency with other package manager modules
- yum now properly supports update_only option
- yum/dnf - Add download_dir param (https://github.com/ansible/ansible/issues/24004)
- zabbix_template - Module no longer requires ``template_name`` to be provided when importing with ``template_json`` option (https://github.com/ansible/ansible/issues/50833)

Deprecated Features
-------------------

- Ansible-defined environment variables not starting with `ANSIBLE_` have been deprecated.  New names match the old name plus the `ANSIBLE_` prefix. These environment variables have been deprecated: LIBVIRT_LXC_NOSECLABEL, DISPLAY_SKIPPED_HOSTS, and NETWORK_GROUP_MODULES
- async - setting the async directory using ``ANSIBLE_ASYNC_DIR`` as an environment key in a task or play is deprecated and will be removed in Ansible 2.12. Set a var name ``ansible_async_dir`` instead.
- cache plugins - Importing cache plugins directly is deprecated and will be removed in 2.12. Cache plugins should use the cache_loader instead so cache options can be reconciled via the configuration system rather than constants.
- docker_network - Deprecate ``ipam_options`` in favor of ``ipam_config``.
- docker_swarm_service - Deprecate ``constraints`` in favor of ``placement``.
- docker_swarm_service - Deprecate ``limit_cpu`` and ``limit_memory`` in favor of ``limits``.
- docker_swarm_service - Deprecate ``log_driver`` and ``log_driver_options`` in favor of ``logging``.
- docker_swarm_service - Deprecate ``reserve_cpu`` and ``reserve_memory`` in favor of ``reservations``.
- docker_swarm_service - Deprecate ``restart_policy``, ``restart_policy_attempts``, ``restart_policy_delay`` and ``restart_policy_window`` in favor of ``restart_config``.
- docker_swarm_service - Deprecate ``update_delay``, ``update_parallelism``, ``update_failure_action``, ``update_monitor``, ``update_max_failure_ratio`` and ``update_order`` in favor of ``update_config``.
- inventory plugins - Inventory plugins using self.cache is deprecated and will be removed in 2.12. Inventory plugins should use self._cache as a dictionary to store results.
- magic variables - documented the deprecation of the ``role_names`` magic variable in favor of either ``ansible_role_names`` (including dependency role names) or ``ansible_play_role_names`` (excluding dependencies).
- win_nssm - Deprecate ``app_parameters`` option in favor of ``arguments``.
- win_nssm - Deprecate ``dependencies``, ``start_mode``, ``user``, and ``password`` options, in favor of using the ``win_service`` module.
- win_nssm - Deprecate ``start``, ``stop``, and ``restart`` values for ``state`` option, in favor of using the ``win_service`` module.

Removed Features (previously deprecated)
----------------------------------------

- azure - deprecated module removed (https://github.com/ansible/ansible/pull/44985)
- cs_nic - deprecated module removed (https://github.com/ansible/ansible/pull/44985)
- ec2_remote_facts - deprecated module removed (https://github.com/ansible/ansible/pull/44985)
- netscaler - deprecated module removed (https://github.com/ansible/ansible/pull/44985)
- win_feature - Removed deprecated 'restart_needed' returned boolean, use standardized 'reboot_required' instead
- win_get_url - Removed deprecated 'skip_certificate_validation' parameter, use standardized 'validate_certs' instead
- win_get_url - Removed deprecated 'win_get_url' returned dictionary, contained values are returned directly
- win_msi - deprecated module removed (https://github.com/ansible/ansible/pull/44985)
- win_package - Removed deprecated 'exit_code' returned int, use standardized 'rc' instead
- win_package - Removed deprecated 'restart_required' returned boolean, use standardized 'reboot_required' instead

Bugfixes
--------

- ACME modules support `POST-as-GET <https://community.letsencrypt.org/t/acme-v2-scheduled-deprecation-of-unauthenticated-resource-gets/74380>`__ and will be able to access Let's Encrypt ACME v2 endpoint after November 1st, 2019.
- ACME modules: improve error messages in some cases (include error returned by server).
- AWS plugins - before 2.8 the environment variable precedence was incorrectly reversed.
- Add code to detect correctly a host running openSUSE Tumbleweed
- Add new ``AnsibleTemplateError`` that various templating related exceptions inherit from, making it easier to catch them without enumerating. (https://github.com/ansible/ansible/issues/50154)
- Added missing domain module fields to the ibm_sa_utils module.
- Added unit test for VMware module_utils.
- All K8S_AUTH_* environment variables are now properly loaded by the k8s lookup plugin
- Allow to use rundeck_acl_policy with python 2 and 3
- Also check stdout for interpreter errors for more intelligent messages to user
- Ansible JSON Decoder - Switch from decode to object_hook to support nested use of __ansible_vault and __ansible_unsafe (https://github.com/ansible/ansible/pull/45514)
- Ansible.Basic - Fix issue when deserializing a JSON string that is not a dictionary - https://github.com/ansible/ansible/pull/55691
- Attempt to avoid race condition based on incorrect buffer size assumptions
- Be sure to use the active state when checking for any_errors_fatal
- Correctly detect multiple ipv6 addresses per device in facts (https://github.com/ansible/ansible/issues/49473)
- Detect FreeBSD KVM guests in facts (https://github.com/ansible/ansible/issues/49158)
- Detect IP addresses on a system with busybox properly (https://github.com/ansible/ansible/issues/50871)
- Enable azure manged disk test
- Enhance the conditional check to include main.yml if it is not from 'role/vars/' (https://github.com/ansible/ansible/pull/51926).
- Extend support for Devuan ascii distribution
- FieldAttribute - Do not use mutable defaults, instead allow supplying a callable for defaults of mutable types (https://github.com/ansible/ansible/issues/46824)
- Fix Amazon system-release version parsing (https://github.com/ansible/ansible/issues/48823)
- Fix VMware module utils for self usage.
- Fix aws_ec2 inventory plugin code to automatically populate regions when missing as documentation states, also leverage config system vs self default/type validation
- Fix bug where some inventory parsing tracebacks were missing or reported under the wrong plugin.
- Fix consistency issue in grafana_dashboard module where the module would detect absence of 'dashboard' key on dashboard create but not dashboard update.
- Fix detection string for SUSE distribution variants like Leap and SLES (SUSE Enterprise Linux Server).
- Fix for callback plugins on Python3 when a module returns non-string field names in its results.  (https://github.com/ansible/ansible/issues/49343)
- Fix handlers to allow for templated values in run_once (https://github.com/ansible/ansible/issues/27237)
- Fix how debconf handles boolean questions to accurately compare
- Fix invalid src option return response for network config modules (https://github.com/ansible/ansible/pull/56076)
- Fix issue getting output from failed ios commands when ``check_rc=False``
- Fix net_get and net_put task run failure - https://github.com/ansible/ansible/pull/56145
- Fix rabbitmq_plugin idempotence due to information message in new version of rabbitmq (https://github.com/ansible/ansible/pull/52166)
- Fix searchpath in the template lookup to work the same way as in the template module.
- Fix the password lookup when run from a FIPS enabled system.  FIPS forbids the use of md5 but we can use sha1 instead. https://github.com/ansible/ansible/issues/47297
- Fix unexpected error when using Jinja2 native types with non-strict constructed keyed_groups (https://github.com/ansible/ansible/issues/52158).
- Fix unwanted ACLs when using copy module (https://github.com/ansible/ansible/issues/44412)
- Fix using omit on play keywords (https://github.com/ansible/ansible/issues/48673)
- Fix using vault encrypted data with jinja2_native (https://github.com/ansible/ansible/issues/48950)
- Fixed KeyError issue in vmware_host_config_manager when a supported option isn't already set (https://github.com/ansible/ansible/issues/44561).
- Fixed an issue with ansible-doc -l failing when parsing some plugin documentation.
- Fixed issue related to --yaml flag in vmware_vm_inventory. Also fixed caching issue in vmware_vm_inventory (https://github.com/ansible/ansible/issues/52381).
- Fixed to handle arguments correctly even if inventory and credential variables are not specified (#25017,#37567)
- Fixes an issue when subscription_id is masked in the output when it's passed as one of the parameters.
- Fixes replacing load balancer with application gateway in Azure virtualmachine scaleset, as leaning up old load balancer was not done properly.
- Give user better error messages and more information on verbose about inventory plugin behavior
- Guard ``HTTPSClientAuthHandler`` under HTTPS checks, to avoid tracebacks when python is compiled without SSL support (https://github.com/ansible/ansible/issues/50339)
- Handle ClientError exceptions when describing VPC peering connections.
- Handle error paginating object versions when bucket does not exist (https://github.com/ansible/ansible/issues/49393)
- Handle exception when there is no snapshot available in virtual machine or template while cloning using vmware_guest.
- Hardware fact gathering now completes on Solaris 8.  Previously, it aborted with error `Argument 'args' to run_command must be list or string`.
- If large integers are passed as options to modules under Python 2, module argument parsing will reject them as they are of type ``long`` and not of type ``int``.
- Include partition tables in the ALL_IN_SCHEMA option for postgresql-privs (https://github.com/ansible/ansible/issues/54516)
- Last loaded handler with the same name is used
- Meraki - Lookups using org_name or net_name no longer query Meraki twice, only once. Major performance improvements.
- Move netconf import errors from import to use.
- Narrow the cases in which we warn about Jinja2 unique filters https://github.com/ansible/ansible/issues/46189
- Now be specific about the entry that trips an error
- PLUGIN_FILTERS_CFG - Ensure that the value is treated as type=path, and that we use the standard section of ``defaults`` instead of ``default`` (https://github.com/ansible/ansible/pull/45994)
- Remove recommendation to use sort_json_policy_dict in the AWS guidelines
- Replace the fix for https://github.com/ansible/ansible/issues/39412 made in https://github.com/ansible/ansible/pull/39483 when using a compression program. This now uses a FIFO file to ensure failure detection of pg_dump. The Windows compatibility is completely dropped in this case.
- Restore SIGPIPE to SIG_DFL when creating subprocesses to avoid it being ignored under Python 2.
- Restore timeout in set_vm_power_state operation in vmware_guest_powerstate module.
- Retry deleting the autoscaling group if there are scaling activities in progress.
- SECURITY Fixed the python interpreter detection, added in 2.8.0alpha1, to properly mark the returned data as untemplatable. This prevents a malicious managed machine from running code on the controller via templating.
- States ``dump`` and ``restore`` only need pg_dump and pg_restore. These tools don't use psycopg2 so this change tries to avoid the use of it in these cases. Fixes https://github.com/ansible/ansible/issues/35906
- The internal key `results` in vmware_guest_snapshot module return renamed to `snapshot_results`.
- The patch fixing the regression of no longer preferring matching security groups in the same VPC https://github.com/ansible/ansible/pull/45787 (which was also backported to 2.6) broke EC2-Classic accounts. https://github.com/ansible/ansible/pull/46242 removes the assumption that security groups must be in a VPC.
- This reverts some changes from commit 723daf3. If a line is found in the file, exactly or via regexp matching, it must not be added again. `insertafter`/`insertbefore` options are used only when a line is to be inserted, to specify where it must be added.
- Use custom JSON encoder in conneciton.py so that ansible objects (AnsibleVaultEncryptedUnicode, for example) can be sent to the persistent connection process
- Windows - prevent sensitive content from appearing in scriptblock logging (CVE 2018-16859)
- aci_aaa_user - Fix setting user description (https://github.com/ansible/ansible/issues/51406)
- aci_access_port_to_interface_policy_leaf_profile - Support missing policy_group
- aci_interface_policy_leaf_policy_group - Support missing aep
- aci_rest - Fix issue ignoring custom port
- aci_switch_leaf_selector - Support empty policy_group
- acme_certificate - use ``ipaddress`` module bundled with Ansible for normalizations needed for OpenSSL backend.
- acme_certificate - writing result failed when no path was specified (i.e. destination in current working directory).
- acme_challenge_cert_helper - the module no longer crashes when the required ``cryptography`` library cannot be found.
- add resource group test
- adhoc always added async_val and poll to tasks, but now includes are enforcing non valid parameters, this bypasses the error.
- allow 'dict()' jinja2 global to function the same even though it has changed in jinja2 versions
- allow loading inventory plugins adjacent to playbooks
- allow nice error to work when auto plugin reads file w/o `plugin` field
- allow using openstack inventory plugin w/o a cache
- ansible-doc, --json now is 'type intelligent' and reinstated --all option
- ansible-doc, removed local hardcoded listing, now uses the 'central' list from constants and other minor issues
- ansible-galaxy - Prevent unicode errors when searching - https://github.com/ansible/ansible/issues/42866
- apt - Show a warning hint in case apt auto-installs its dependencies.
- apt_repository - do not require a tty to prevent errors parsing GPG keys (https://github.com/ansible/ansible/issues/49949)
- assemble - avoid extra newline on Python 3 (https://github.com/ansible/ansible/issues/44739)
- async - fixed issue where the shell option ``async_dir`` was not being used when setting the async directory.
- async_wrapper - Allocate an explicit stdin (https://github.com/ansible/ansible/issues/50758)
- avoid empty groups in ansible-inventory JSON output as they will be interpreted as hosts
- avoid making multiple 'sub copies' when traversing already 'clean copy' of dict
- aws_ec2 - fixed issue where cache did not contain the computed groups
- azure_rm inventory plugin - fix azure batch request (https://github.com/ansible/ansible/pull/50006)
- azure_rm inventory plugin - fix runtime error under Python3 (https://github.com/ansible/ansible/pull/46608)
- azure_rm_deployment - fixed regression that prevents resource group from being created (https://github.com/ansible/ansible/issues/45941)
- azure_rm_functionapp - adding two properties which need to be set by default, otherwise function app won't behave correctly in Azure Portal.
- azure_rm_managed_disk_facts - added missing implementation of listing managed disks by resource group
- azure_rm_mysqlserver - fixed issues with passing parameters while updating existing server instance
- azure_rm_postgresqldatabase - fix force_update bug (https://github.com/ansible/ansible/issues/50978).
- azure_rm_postgresqldatabase - fix force_update bug.
- azure_rm_postgresqlserver - fixed issues with passing parameters while updating existing server instance
- basic - modify the correct variable when determining available hashing algorithms to avoid errors when md5 is not available (https://github.com/ansible/ansible/issues/51355)
- better error message when bad type in config, deal with EVNAR= more gracefully https://github.com/ansible/ansible/issues/22470
- blockinfile - use bytes rather than a native string to prevent a stacktrace in Python 3 when writing to the file (https://github.com/ansible/ansible/issues/46237)
- callbacks - Do not filter out exception, warnings, deprecations on failure when using debug (https://github.com/ansible/ansible/issues/47576)
- change function to in place replacement, compose with module_args_copy for 'new clean copy'
- chroot connection - Support empty files with copying to target (https://github.com/ansible/ansible/issues/36725)
- clear all caches in plugin loader for a plugin type when adding new paths, otherwise new versions of already loaded plugin won't be discovered
- cloudscale - Fix compatibilty with Python3 in version 3.5 and lower.
- configuration retrieval would fail on non primed plugins
- convert input into text to ensure valid comparisons in nmap inventory plugin
- copy - Ensure that the src file contents is converted to unicode in diff information so that it is properly wrapped by AnsibleUnsafeText to prevent unexpected templating of diff data in Python3 (https://github.com/ansible/ansible/issues/45717)
- copy - align invocation in return value between check and normal mode
- cs_ip_address - fix vpc use case failed if network param provided. Ensured vpc and network are mutually exclusive.
- cs_iso - Add the 'is_public' param into argument_spec to allow the registering of public iso.
- cs_network_offering - Add a choice list for supported_services parameter in arg_spec.
- cs_template - Fixed a KeyError on state=extracted.
- delegate_to - Fix issue where delegate_to was applied via ``apply`` on an include, where a loop was present on the include
- delegate_to - When templating ``delegate_to`` in a loop, don't use the task for a cache, return a special cache through ``get_vars`` allowing looping over a hostvar (https://github.com/ansible/ansible/issues/47207)
- dict2items - Allow dict2items to work with hostvars
- disallow non dict results from module and allow user to continue using with a warning.
- distribution - add check to remove incorrect matches of Clear Linux when processing distribution files (https://github.com/ansible/ansible/issues/50009)
- dnf - allow to operate on file paths (https://github.com/ansible/ansible/issues/50843)
- dnf - enable package name specification for absent
- dnf - fix issue where ``conf_file`` was not being loaded properly
- dnf - fix issue with dnf API calls to adapt to changes in upstream dnf version 4.2.2
- dnf - fix package parsing to handle git snapshot nevra
- dnf - fix update_cache combined with install operation to not cause dnf transaction failure
- do not return ``state: absent`` when the module returns either ``path`` or ``dest`` but the file does not exists (https://github.com/ansible/ansible/issues/35382)
- docker connection - Support empty files with copying to target (https://github.com/ansible/ansible/issues/36725)
- docker_compose - fixed an issue where ``remove_orphans`` doesn't work reliably.
- docker_container - Fix idempotency problems with ``cap_drop`` and ``groups`` (when numeric group IDs were used).
- docker_container - Fix type conversion errors for ``log_options``.
- docker_container - Fixing various comparison/idempotency problems related to wrong comparisons. In particular, comparisons for ``command`` and ``entrypoint`` (both lists) no longer ignore missing elements during idempotency checks.
- docker_container - Makes ``blkio_weight``, ``cpuset_mems``, ``dns_opts`` and ``uts`` options actually work.
- docker_container - ``init`` and ``shm_size`` are now checked for idempotency.
- docker_container - ``publish_ports: all`` was not used correctly when checking idempotency.
- docker_container - do not fail when removing a container which has ``auto_remove: yes``.
- docker_container - fail if ``ipv4_address`` or ``ipv6_address`` is used with a too old docker-py version.
- docker_container - fail when non-string env values are found, avoiding YAML parsing issues. (https://github.com/ansible/ansible/issues/49802)
- docker_container - fix ``ipc_mode`` and ``pid_mode`` idempotency if the ``host:<container-name>`` form is used (as opposed to ``host:<container-id>``).
- docker_container - fix ``network_mode`` idempotency if the ``container:<container-name>`` form is used (as opposed to ``container:<container-id>``) (https://github.com/ansible/ansible/issues/49794)
- docker_container - fix ``paused`` option (which never worked).
- docker_container - fix behavior of ``detach: yes`` if ``auto_remove: yes`` is specified.
- docker_container - fix idempotency check for published_ports in some special cases.
- docker_container - fix idempotency of ``log_options`` when non-string values are used. Also warn user that this is the case.
- docker_container - fix idempotency problems with docker-py caused by previous ``init`` idempotency fix.
- docker_container - fix interplay of docker-py version check with argument_spec validation improvements.
- docker_container - fixing race condition when ``detach`` and ``auto_remove`` are both ``true``.
- docker_container - now returns warnings from docker daemon on container creation and updating.
- docker_container - refactored minimal docker-py/API version handling, and fixing such handling of some options.
- docker_container - the behavior is improved in case ``image`` is not specified, but needed for (re-)creating the container.
- docker_container, docker_image, docker_image_facts - also find local image when image name is prefixed with ``docker.io/library/`` or ``docker.io/``.
- docker_host_info - ``network_filters`` needs docker-py 2.0.2, ``disk_usage`` needs docker-py 2.2.0.
- docker_network - ``driver_options`` containing Python booleans would cause Docker to throw exceptions.
- docker_network - now returns warnings from docker daemon on network creation.
- docker_swarm - Fixed node_id parameter not working for node removal (https://github.com/ansible/ansible/issues/53501)
- docker_swarm - do not crash with older docker daemons (https://github.com/ansible/ansible/issues/51175).
- docker_swarm - fixes idempotency for the ``ca_force_rotate`` option.
- docker_swarm - improve Swarm detection.
- docker_swarm - improve idempotency checking; ``rotate_worker_token`` and ``rotate_manager_token`` are now also used when all other parameters have not changed.
- docker_swarm - now supports docker-py 1.10.0 and newer for most operations, instead only docker 2.6.0 and newer.
- docker_swarm - properly implement check mode (it did apply changes).
- docker_swarm - the ``force`` option was ignored when ``state: present``.
- docker_swarm_service - Added support for ``read_only`` parameter.
- docker_swarm_service - Change the type of options ``gid`` and ``uid`` on ``secrets`` and ``configs`` to ``str``.
- docker_swarm_service - Document ``labels`` and ``container_labels`` with correct type.
- docker_swarm_service - Document ``limit_memory`` and ``reserve_memory`` correctly on how to specify sizes.
- docker_swarm_service - Document minimal API version for ``configs`` and ``secrets``.
- docker_swarm_service - Don't recreate service when ``networks`` parameter changes when running Docker API >= 1.29.
- docker_swarm_service - Don't set ``10`` as default for ``update_delay``.
- docker_swarm_service - Don't set ``1`` as default for ``update_parallelism``.
- docker_swarm_service - Don't set ``root`` as the default user.
- docker_swarm_service - Raise minimum required docker-py version for ``secrets`` to 2.4.0.
- docker_swarm_service - Raise minimum required docker-py version for module to 2.0.2.
- docker_swarm_service - Removed redundant defaults for ``uid``, ``gid``, and ``mode`` from ``configs`` and ``secrets``.
- docker_swarm_service - The ``publish``.``mode`` parameter was being ignored if docker-py version was < 3.0.0. Added a parameter validation test.
- docker_swarm_service - Validate choices for option ``mode``.
- docker_swarm_service - Validate minimum docker-py version of 2.4.0 for option ``constraints``.
- docker_swarm_service - When docker fails to update a container with an ``update out of sequence`` error, the module will retry to update up to two times, and only fail if all three attempts do not succeed.
- docker_swarm_service - fix use of Docker API so that services are not detected as present if there is an existing service whose name is a substring of the desired service
- docker_swarm_service - fixing falsely reporting ``publish`` as changed when ``publish.mode`` is not set.
- docker_swarm_service - fixing falsely reporting ``update_order`` as changed when option is not used.
- docker_swarm_service - fixing wrong option type for ``update_order`` which prevented using that option.
- docker_swarm_service - now returns warnings from docker daemon on service creation.
- docker_swarm_service - the return value was documented as ``ansible_swarm_service``, but the module actually returned ``ansible_docker_service``. Documentation and code have been updated so that the variable is now called ``swarm_service``. In Ansible 2.7.x, the old name ``ansible_docker_service`` can still be used to access the result.
- docker_swarm_service: fails because of default "user: root" (https://github.com/ansible/ansible/issues/49199)
- docker_swarm_service_info - work around problems with older docker-py versions such as 2.0.2.
- docker_volume - ``labels`` now work (and are a ``dict`` and no longer a ``list``).
- docker_volume - fix ``force`` and change detection logic. If not both evaluated to ``True``, the volume was not recreated.
- document debug's var already having implicit moustaches
- document old option that was initally missed
- dynamic includes - Add missed ``run_once`` to valid include attributes (https://github.com/ansible/ansible/pull/48068)
- dynamic includes - Use the copied and merged task for calculating task vars in the free strategy (https://github.com/ansible/ansible/issues/47024)
- ec2 - Correctly sets the end date of the Spot Instance request. Sets `ValidUntil` value in proper way so it will be auto-canceled through `spot_wait_timeout` interval.
- ec2 - Only use user_data if the user has specified a value. This prevents setting the instance's user data to b'None'.
- ec2 - if the private_ip has been provided for the new network interface it shouldn't also be added to top level parameters for run_instances()
- ec2_asg - Fix error where ASG dict has no launch config or launch template key
- ec2_asg - Fix scenario where min_size can end up passing None type to boto
- ec2_group - Sanitize the ingress and egress rules before operating on them by flattening any lists within lists describing the target CIDR(s) into a list of strings. Prior to Ansible 2.6 the ec2_group module accepted a list of strings, a list of lists, or a combination of strings and lists within a list. https://github.com/ansible/ansible/pull/45594
- ec2_group - There can be multiple security groups with the same name in different VPCs. Prior to 2.6 if a target group name was provided, the group matching the name and VPC had highest precedence. Restore this behavior by updated the dictionary with the groups matching the VPC last.
- ec2_instance - Correctly adds description when adding a single ENI to the instance
- ec2_instance - Does not return ``instances`` when ``wait: false`` is specified
- ecs_ecr and iam_role - replace uses of sort_json_policy_dict with compare_policies which is compatible with Python 3
- elb_target_group - cast target ports to integers before making API calls after the key 'Targets' is in params.
- ensure module results and facts are marked untrusted as templates for safer use within the same task
- ensure we always have internal module attributes set, even if not being passed (fixes using modules as script)
- ensure we have a XDG_RUNTIME_DIR, as it is not handled correctly by some privilege escalation configurations
- explain 'bare variables' in error message
- fact gathering to obey play tags
- facts - detect VMs from google cloud engine and scaleway
- facts - ensure that the default package manager for RHEL < 8 is yum, and dnf for newer
- facts - properly detect package manager for a Fedora/RHEL/CentOS system that has rpm-ostree installed
- facts - set virtualization_role for KVM hosts (https://github.com/ansible/ansible/issues/49734)
- fetch_url did not always return lower-case header names in case of HTTP errors (https://github.com/ansible/ansible/pull/45628).
- file - Allow state=touch on file the user does not own https://github.com/ansible/ansible/issues/50943
- fix DNSimple to ensure check works even when the number of records is larger than 100
- fix FactCache.update() to conform to the dict API.
- fix ansible-pull handling of extra args, complex quoting is needed for inline JSON
- fix elasticsearch_plugin force to be bool (https://github.com/ansible/ansible/pull/47134)
- fix handling of firewalld port if protocol is missing
- flatpak - Makes querying of present flatpak name more robust, fixes
- gce inventory plugin was misusing the API and needlessly doing late validation.
- gcp_compute inventory plugin - apply documented default when one is not provided.
- gcp_compute_instance - fix crash when the instance metadata is not set
- gcp_utils - fix google auth scoping issue with application default credentials or google cloud engine credentials. Only scope credentials that can be scoped.
- get_url - Don't re-download files unnecessarily when force=no (https://github.com/ansible/ansible/issues/45491)
- get_url - Fix issue with checksum validation when using a file to ensure we skip lines in the file that do not contain exactly 2 parts. Also restrict exception handling to the minimum number of necessary lines (https://github.com/ansible/ansible/issues/48790)
- get_url - support remote checksum files with paths specified with leading dots (`./path/to/file`)
- gitlab modules - Update version deprecations to use strings instead of integers so that ``2.10`` isn't converted to ``2.1``. (https://github.com/ansible/ansible/pull/55395)
- handle non strings in requirements version for ansible-galaxy
- handle option json errors more gracefully, also document options are not vaultable.
- handle xmlrpc errors in the correct fashion for rhn_channel
- handlers - fix crash when handler task include tasks
- host execution order - Fix ``reverse_inventory`` not to change the order of the items before reversing on python2 and to not backtrace on python3
- icinga2_host - fixed the issue with not working ``use_proxy`` option of the module.
- imports - Prevent the name of an import from being addressable as a handler, only the tasks within should be addressable. Use an include instead of an import if you need to execute many tasks from a single handler (https://github.com/ansible/ansible/issues/48936)
- include_role - Don't swallow errors when processing included files/roles (https://github.com/ansible/ansible/issues/54786)
- include_tasks - Ensure we give IncludedFile the same context as TaskExecutor when templating the parent include path allowing for lookups in the included file path (https://github.com/ansible/ansible/issues/49969)
- include_tasks - Fixed an unexpected exception if no file was given to include.
- include_vars - error handlers now generate proper error messages with non-ASCII args
- influxdb_user - An unspecified password now sets the password to blank, except on existing users. This previously caused an unhandled exception.
- influxdb_user - Fixed unhandled exception when using invalid login credentials (https://github.com/ansible/ansible/issues/50131)
- inventory plugins - Fix creating groups from composed variables by getting the latest host variables
- inventory_aws_ec2 - fix no_log indentation so AWS temporary credentials aren't displayed in tests
- ipaddr - fix issue where network address was blank for 0-size networks (https://github.com/ansible/ansible/issues/17872)
- issue a warning when local fact is not correctly loaded, old behavior just updated fact value with the error.
- jail connection - Support empty files with copying to target (https://github.com/ansible/ansible/issues/36725)
- jenkins_plugin - Prevent plugin to be reinstalled when state=present (https://github.com/ansible/ansible/issues/43728)
- jenkins_plugin - ``version: latest`` should install new plugins with their dependencies
- jira - description field is not always required
- k8s modules and plugins now bubble up error message when the openshift python client fails to import.
- k8s_facts now returns a resources key in all situations
- k8s_facts: fix handling of unknown resource types
- kubectl connection - Support empty files with copying to target (https://github.com/ansible/ansible/issues/36725)
- libvirt_lxc connection - Support empty files with copying to target (https://github.com/ansible/ansible/issues/36725)
- lineinfile - fix index out of range error when using insertbefore on a file with only one line (https://github.com/ansible/ansible/issues/46043)
- loop - Do not evaluate a empty literal list ``[]`` as falsy, it should instead cause the task to skip ()
- loop - Ensure that a loop with a when condition that evaluates to false and delegate_to, will short circuit if the loop references an undefined variable. This matches the behavior in the same scenario without delegate_to (https://github.com/ansible/ansible/issues/45189)
- loop_control - Catch exceptions when templating label individually for loop iterations which caused the templating failure as the full result. This instead only registers the templating exception for a single loop result (https://github.com/ansible/ansible/issues/48879)
- lvg - Take into account current PV in the VG to fix PV removal
- lvol - fixed ValueError when using float size (https://github.com/ansible/ansible/issues/32886, https://github.com/ansible/ansible/issues/29429)
- mail - fix python 2.7 regression
- make YAML inventory more tolerant to comments/empty/None entries
- meraki_config_template - Fix conditions which prevented code from executing when specifying net_id
- meraki_ssid - Fix module to actually perform changes when state is present and SSID is referenced by number and not name.
- meraki_static_route - Module would make unnecessary API calls to Meraki when ``net_id`` is specified in task.
- meraki_static_route - Module would make unnecessary API calls to Meraki when ``net_id`` is specified in task.
- meraki_vlan - Module would make unnecessary API calls to Meraki when net_id is specified in task.
- modprobe - The modprobe module now detects builtin kernel modules. If a kernel module is builtin the modprobe module will now: succeed (without incorrectly reporting changed) if ``state`` is ``present``; and fail if ``state`` is ``absent`` (with an error message like ``modprobe: ERROR: Module nfs is builtin.``). (https://github.com/ansible/ansible/pull/37150)
- mysql - MySQLdb doesn't import the cursors module for its own purposes so it has to be imported in MySQL module utilities before it can be used in dependent modules like the proxysql module family.
- mysql - fixing unexpected keyword argument 'cursorclass' issue after migration from MySQLdb to PyMySQL.
- mysql_*, proxysql_* - PyMySQL (a pure-Python MySQL driver) is now a preferred dependency also supporting Python 3.X.
- mysql_user: fix compatibility issues with various MySQL/MariaDB versions
- mysql_user: fix the working but incorrect regex used to check the user privileges.
- mysql_user: match backticks, single and double quotes when checking user privileges.
- now default is ``list`` so ``None`` is bad comparison for gathering
- now no log is being respected on retry and high verbosity. CVE-2018-16876
- omit - support list types containing dicts (https://github.com/ansible/ansible/issues/45907)
- onepassword_facts - Fix an issue looking up some 1Password items which have a 'password' attribute alongside the 'fields' attribute, not inside it.
- openshift inventory plugin - do not default create client if auth parameters were given.
- openssl_* - fix error when ``path`` contains a file name without path.
- openssl_certificate - ``has_expired`` correctly checks if the certificate is expired or not
- openssl_certificate - fix ``state=absent``.
- openssl_certificate - make sure that extensions are actually present when their values should be checked.
- openssl_certificate, openssl_csr, openssl_pkcs12, openssl_privatekey, openssl_publickey - The modules are now able to overwrite write-protected files (https://github.com/ansible/ansible/issues/48656).
- openssl_csr - SAN normalization for IP addresses for the pyOpenSSL backend was broken.
- openssl_csr - fix byte encoding issue on Python 3
- openssl_csr - fix problem with idempotency of keyUsage option.
- openssl_csr - fixes idempotence problem with PyOpenSSL backend when no Subject Alternative Names were specified.
- openssl_csr - improve ``subject`` validation.
- openssl_csr - improve error messages for invalid SANs.
- openssl_csr - the cryptography backend's idempotency checking for basic constraints was broken.
- openssl_csr, openssl_certificate, openssl_publickey - properly validate private key passphrase; if it doesn't match, fail (and not crash or ignore).
- openssl_csr, openssl_csr_info - use ``ipaddress`` module bundled with Ansible for normalizations needed for pyOpenSSL backend.
- openssl_dhparam - fix ``state=absent`` idempotency and ``changed`` flag.
- openssl_pkcs12 - No need to specify ``privatekey_path`` when ``friendly_name`` is specified.
- openssl_pkcs12 - fix byte encoding issue on Python 3
- openssl_pkcs12, openssl_privatekey - These modules now accept the output file mode in symbolic form or as a octal string (https://github.com/ansible/ansible/issues/53476).
- openssl_privatekey - no longer hang or crash when passphrase does not match or was not specified, but key is protected with one. Also regenerate key if passphrase is specified but existing key has no passphrase.
- openssl_publickey - fixed crash on Python 3 when OpenSSH private keys were used with passphrases.
- openstack inventory plugin - send logs from sdk to stderr so they do not combine with output
- os_network - According to the OpenStack Networking API the attribute provider:segmentation_id of a network has to be an integer. (https://github.com/ansible/ansible/issues/51655)
- os_security_group_rule - os_security_group_rule doesn't exit properly when secgroup doesn't exist and state=absent (https://github.com/ansible/ansible/issues/50057)
- ovirt_host_network - Fix type conversion (https://github.com/ansible/ansible/pull/47617).
- ovirt_network - fix getting network labels (https://github.com/ansible/ansible/pull/52499).
- pamd - Allow for validation of definitive control in pamd module.
- pamd - fix idempotence issue when removing rules
- pamd: add delete=False to NamedTemporaryFile() fixes OSError on module completion, and removes print statement from module code. (see https://github.com/ansible/ansible/pull/47281 and https://github.com/ansible/ansible/issues/47080)
- pamd: fix state: args_present idempotence (see https://github.com/ansible/ansible/issues/47197)
- pamd: fix state: updated idempotence (see https://github.com/ansible/ansible/issues/47083)
- pamd: update regex to allow leading dash and retain EOF newline (see https://github.com/ansible/ansible/issues/47418)
- paramiko_ssh - add auth_timeout parameter to ssh.connect when supported by installed paramiko version. This will prevent "Authentication timeout" errors when a slow authentication step (>30s) happens with a host (https://github.com/ansible/ansible/issues/42596)
- pass correct loading context to persistent connections
- pip - idempotence in check mode now works correctly.
- play order is now applied under all circumstances, fixes
- postgresql_db - the module fails not always when pg_dump errors occurred (https://github.com/ansible/ansible/issues/40424).
- postgresql_idx - removed useless rows that remained after the previous refactoring
- postgresql_privs - change fail to warn if PostgreSQL role does not exist (https://github.com/ansible/ansible/issues/46168).
- postgresql_slot - fixed sslrootcert mapping to psycopg2 connection string
- postgresql_user - create pretty error message when creating a user without an encrypted password on newer PostgreSQL versions
- preserve Noneness of pwdfile when it is None in virtualbox inventory plugin
- prevent import_role from inserting dupe into `roles:` execution when duplicate signature role already exists in the section.
- profile_tasks callback - Fix the last task time when running multiple plays (https://github.com/ansible/ansible/issues/52760)
- properly report errors when k=v syntax is mixed with YAML syntax in a task (https://github.com/ansible/ansible/issues/27210)
- psexec - Handle socket.error exceptions properly
- psexec - give proper error message when the psexec requirements are not installed
- psrp - Explicitly documented the extra auth options that could have been passed in - https://github.com/ansible/ansible/issues/54664
- psrp - Fix UTF-8 output - https://github.com/ansible/ansible/pull/46998
- psrp - Fix blank newlines appearing before ``stdout`` when using ``script`` or ``raw`` with the ``psrp`` connection plugin
- psrp - Fix issue when dealing with unicode values in the output for Python 2
- psrp - Fix issues when fetching large files causing a memory leak - https://github.com/ansible/ansible/issues/55239
- psrp - Fix issues with propagating errors back to Ansible with ``raw`` tasks
- psrp - do not display bootstrap wrapper for each module exec run
- purefa_facts - remove unnecessary line that could cause failure in rare circumstances.
- purefa_facts and purefb_facts now correctly adds facts into main ansible_fact dictionary (https://github.com/ansible/ansible/pull/50349)
- rabbitmq_binding - Delete binding when ``state`` is ``absent``.
- random_mac - generate a proper MAC address when the provided vendor prefix is two or four characters (https://github.com/ansible/ansible/issues/50838)
- rds_instance - Cluster_id which is an alias of db_cluster_identifier is a mandatory check target.
- re allow empty plays for now, but add deprecation msg.
- reboot - Fix bug where the connection timeout was not reset in the same task after rebooting
- reboot - add appropriate commands to make the plugin work with VMware ESXi (https://github.com/ansible/ansible/issues/48425)
- reboot - add reboot_timeout parameter to the list of parameters so it can be used.
- reboot - add support for OpenBSD
- reboot - add support for rebooting AIX (https://github.com/ansible/ansible/issues/49712)
- reboot - change default reboot time command to prevent hanging on certain systems (https://github.com/ansible/ansible/issues/46562)
- reboot - gather distribution information in order to support Alpine and other distributions (https://github.com/ansible/ansible/issues/46723)
- reboot - search common paths for the shutdown command and use the full path to the binary rather than depending on the PATH of the remote system (https://github.com/ansible/ansible/issues/47131)
- reboot - use IndexError instead of TypeError in exception
- reboot - use a common set of commands for older and newer Solaris and SunOS variants (https://github.com/ansible/ansible/pull/48986)
- reboot - use unicode instead of bytes for stdout and stderr to match the type returned from low_level_execute()
- redfish_utils - fix "406 Not Acceptable" issue with some OOB controllers (https://github.com/ansible/ansible/issues/55078)
- redfish_utils - fix reference to local variable 'systems_service'
- redhat_subscription - For compatibility using the redhat_subscription module on hosts set to use a python 3 interpreter, use string values when updating yum plugin configuration files.
- redis cache - Support version 3 of the redis python library (https://github.com/ansible/ansible/issues/49341)
- rely on method existing vs loosely related _cache attribute, also fix data persistence issue on plugin reuse across sources.
- remote home directory - Disallow use of remote home directories that include relative pathing by means of `..` (CVE-2019-3828) (https://github.com/ansible/ansible/pull/52133)
- remote_management foreman - Fixed issue where it was impossible to createdelete a product because product was missing in dict choices ( https://github.com/ansible/ansible/issues/48594 )
- remove bare var handling from conditionals (not needed since we removed bare vars from `with_` loops) to normalize handling of variable values, no matter if the string value comes from a top level variable or from a dictionary key or subkey
- remove deprecation notice since validation makes it very noisy
- remove rendundant path uniquifying in inventory plugins.  This removes use of md5 hashing and fixes inventory plugins when run in FIPS mode.
- replace - fix behavior when ``before`` and ``after`` are used together (https://github.com/ansible/ansible/issues/31354)
- replaced if condition requester_pays is None with True or False instead
- reverted change in af55b8e which caused the overwrite parameter to be ignored
- rhn_register - require username/password when unregistering and provide useful error message (https://github.com/ansible/ansible/issues/22300)
- rhsm_repository - compile regular expressions to improve performance when looping over available repositories
- rhsm_repository - handle systems without any repos
- rhsm_repository - prevent duplicate repository entries from being entered in the final command
- roles - Ensure that we don't overwrite roles that have been registered (from imports) while parsing roles under the roles header (https://github.com/ansible/ansible/issues/47454)
- s3_bucket - Prior to 2.6 using non-text tags worked, although was not idempotent. In 2.6 waiters were introduced causing non-text tags to be fatal to the module's completion. This fixes the module failure as well as idempotence using integers as tags.
- scaleway inventory plugin - Fix response.getheaders regression (https://github.com/ansible/ansible/pull/48671)
- script inventory plugin - Don't pass file_name to DataLoader.load, which will prevent misleading error messages (https://github.com/ansible/ansible/issues/34164)
- setup - properly detect is_chroot on Btrfs (https://github.com/ansible/ansible/issues/55006)
- setup - properly gather iSCSI information for AIX (https://github.com/ansible/ansible/pull/44644)
- simple code collapse, avoid a lot of repetition
- skip invalid plugin after warning in loader
- slurp - Fix issues when using paths on Windows with glob like characters, e.g. ``[``, ``]``
- small code cleanup to make method signatures match their parents and nicer 'unsafe' handling.
- ssh - Check the return code of the ssh process before raising AnsibleConnectionFailure, as the error message for the ssh process will likely contain more useful information. This will improve the missing interpreter messaging when using modules such as setup which have a larger payload to transfer when combined with pipelining. (https://github.com/ansible/ansible/issues/53487)
- ssh - Properly quote the username to allow usernames containing spaces (https://github.com/ansible/ansible/issues/49968)
- ssh connection - Support empty files with piped transfer_method (https://github.com/ansible/ansible/issues/45426)
- ssh connection - do not retry with invalid credentials to prevent account lockout (https://github.com/ansible/ansible/issues/48422)
- systemd - warn when executing in a chroot environment rather than failing (https://github.com/ansible/ansible/pull/43904)
- tags - allow tags to be specified by a variable (https://github.com/ansible/ansible/issues/49825)
- templar - Do not strip new lines in native jinja - https://github.com/ansible/ansible/issues/46743
- terraform - fixed issue where state "planned" wouldn't return an output and the project_path had to exist in two places (https://github.com/ansible/ansible/issues/39689)
- tower_job_wait - Fixed wrong variable specification in examples
- tweak inv plugin skip msg to be more precise, also require higher verbosity to view
- udm_dns_record - Fix issues when state is absent with undefined variable diff at the module return.
- udm_dns_zone - Fix issues when state is absent with undefined variable diff at the module return.
- udm_group - Fix issues when state is absent with undefined variable diff at the module return.
- udm_share - Fix issues when state is absent with undefined variable diff at the module return.
- udm_user - Fix issues when state is absent with undefined variable diff at the module return.
- ufw - when ``default`` is specified, ``direction`` does not needs to be specified. This was accidentally introduced in Ansible 2.7.8.
- ufw: make sure that only valid values for ``direction`` are passed on.
- unarchive - add two more error conditions to unarchive to present more accurate error message (https://github.com/ansible/ansible/issues/51848)
- unsafe - Add special casing to sets, to support wrapping elements of sets correctly in Python 3 (https://github.com/ansible/ansible/issues/47372)
- uri - Ensure the ``uri`` module supports async (https://github.com/ansible/ansible/issues/47660)
- uri - do not write the file after failure (https://github.com/ansible/ansible/issues/53491)
- uri: fix TypeError when file can't be saved
- urls - When validating SSL certs using an a non-SSL proxy, do not send "Connection: close" when requesting a tunnel. This prevents some proxy servers from dropping the connection (https://github.com/ansible/ansible/issues/32750)
- use to_native (py2/3 safe) instead of str for 'textualizing' intput in async_status
- user - add documentation on what underlying tools are used on each platform (https://github.com/ansible/ansible/issues/44266)
- user - do not report changes every time when setting password_lock (https://github.com/ansible/ansible/issues/43670)
- user - fix a bug when checking if a local user account exists on a system using directory authentication (https://github.com/ansible/ansible/issues/50947, https://github.com/ansible/ansible/issues/38206)
- user - fixed the fallback mechanism for creating a user home directory when the directory isn't created with `useradd` command. Home directory will now have a correct mode and it won't be created in a rare situation when a local user is being deleted but it exists on a central user system (https://github.com/ansible/ansible/pull/49262).
- user - on FreeBSD set the user expiration time as seconds since the epoch in UTC to avoid timezone issues
- user - properly parse the shadow file on AIX (https://github.com/ansible/ansible/issues/54461)
- user - properly remove expiration when set to a negative value (https://github.com/ansible/ansible/issues/47114)
- user - remove warning when creating a disabled account with '!' or '*' in the password field (https://github.com/ansible/ansible/issues/46334)
- user module - do not pass ssh_key_passphrase on cmdline (CVE-2018-16837)
- vault - Improve error messages encountered when reading vault files (https://github.com/ansible/ansible/issues/49252)
- vmware - The VMware modules now enable the SSL certificate check unless ``validate_certs`` is ``false``.
- vsphere_guest - creating machines without vm_extra_config allowed
- vsphere_guest - powering on/off absent virtual machine will fail
- vultr - fixed the handling of an inconsistency in the response from Vultr API when it returns an unexpected empty list instead a empty dict.
- vultr_server - Fix idempotency for options ``ipv6_enabled`` and ``private_network_enabled``.
- vultr_server - fixed multiple ssh keys were not handled.
- vultr_server_facts - fixed facts gathering fails if firewall is enabled.
- win_acl - Fix issues when using paths with glob like characters, e.g. ``[``, ``]``
- win_acl_inheritance - Fix issues when using paths with glob like characters, e.g. ``[``, ``]``
- win_certificate_store - Fix exception handling typo
- win_certificate_store - Fix issues when using paths with glob like characters, e.g. ``[``, ``]``
- win_chocolatey - Fix hang when used with proxy for the first time - https://github.com/ansible/ansible/issues/47669
- win_chocolatey - Fix incompatibilities with the latest release of Chocolatey ``v0.10.12+``
- win_chocolatey - Fix issue when parsing a beta Chocolatey install - https://github.com/ansible/ansible/issues/52331
- win_chocolatey_source - fix bug where a Chocolatey source could not be disabled unless ``source`` was also set - https://github.com/ansible/ansible/issues/50133
- win_copy - Fix copy of a dir that contains an empty directory - https://github.com/ansible/ansible/issues/50077
- win_copy - Fix issue where the dest return value would be enclosed in single quote when dest is a folder - https://github.com/ansible/ansible/issues/45281
- win_copy - Fix issues when using paths with glob like characters, e.g. ``[``, ``]``
- win_domain - Do not fail if DC is already promoted but a reboot is required, return ``reboot_required: True``
- win_domain - Fix checking for a domain introduced in a recent patch
- win_domain - Fix when running without credential delegated authentication - https://github.com/ansible/ansible/issues/53182
- win_file - Fix issue when managing hidden files and directories - https://github.com/ansible/ansible/issues/42466
- win_file - Fix issues when using paths with glob like characters, e.g. ``[``, ``]``
- win_find - Ensure found files are sorted alphabetically by the path instead of it being random
- win_find - Fix issues when using paths with glob like characters, e.g. ``[``, ``]``
- win_firewall_rule - Remove invalid 'bypass' action
- win_get_url - Fix issues when using paths with glob like characters, e.g. ``[``, ``]``
- win_group_membership - fix intermittent issue where it failed to convert the ADSI object to the .NET object after using it once
- win_lineinfile - Fix issue where a malformed json block was returned causing an error
- win_mapped_drive - Updated win_mapped_drive to use the proper Win32 APIs and updated documentation for proper usage
- win_nssm - Fix several escaping and quoting issues of paths and parameters.
- win_nssm - Switched to Argv-ToString for escaping NSSM credentials (https://github.com/ansible/ansible/issues/48728)
- win_owner - Fix issues when using paths with glob like characters, e.g. ``[``, ``]``
- win_power_plan - Fix issue where win_power_plan failed on newer Windows 10 builds - https://github.com/ansible/ansible/issues/43827
- win_psexec - Support executables with a space in the path
- win_reboot - Fix reboot command validation failure when running under the psrp connection plugin
- win_reboot - pass return value for ``test_command`` result when using the ``psrp`` connection plugin
- win_reg_stat - Fix issue where the key's ``(Default)`` property was not being returned if it was set
- win_reg_stat - Support registry paths with special characters - https://github.com/ansible/ansible/issues/41791
- win_regedit - Fix issue where creating a new key would set the ``(Default)`` key property to an empty string instead of undefined
- win_regedit - Support registry paths with special characters - https://github.com/ansible/ansible/issues/41791
- win_region - Fix the check for ``format`` when running on the ``psrp`` connection plugin
- win_route - Corrected issue where the wrong network interface was used for new static routes. - https://github.com/ansible/ansible/issues/28051
- win_say - fix syntax error in module and get tests working
- win_shortcut - Added idempotency checks when ``src`` is a special shell folder like ``shell:RecycleBinFolder``
- win_tempfile - Always return the full NTFS absolute path and not a DOS 8.3 path.
- win_updates - Correctly report changes on success
- win_uri - allow to send a JSON array with just one item into - https://github.com/ansible/ansible/issues/49483
- win_uri - stop junk output from being returned to Ansible - https://github.com/ansible/ansible/issues/47998
- win_user_right - Fix output containing non json data - https://github.com/ansible/ansible/issues/54413
- win_xml - use New-Object System.Xml.XmlDocument rather than Get-Content for parsing xml (https://github.com/ansible/ansible/issues/48471)
- windows - Fixed various module utils that did not work with path that had glob like chars
- winrm - Only use pexpect for auto kerb auth if it is installed and contains the required kwargs - https://github.com/ansible/ansible/issues/43462
- winrm - attempt to recover from a WinRM send input failure if possible
- yum - Remove incorrect disable_includes error message when using disable_excludes (https://github.com/ansible/ansible/issues/51697)
- yum - fix "package == version" syntax (https://github.com/ansible/ansible/pull/47744)
- yum - fix disable_excludes on systems with yum rhn plugin enabled (https://github.com/ansible/ansible/issues/53134)
- yum - properly handle a proxy config in yum.conf for an unauthenticated proxy
- yum allows comparison operators like '>=' for selecting package version
- zabbix_hostmacro - Added missing validate_certs logic for running module against Zabbix servers with untrused SSL certificates (https://github.com/ansible/ansible/issues/47611)
- zabbix_hostmacro - Fixed support for user macros with context (https://github.com/ansible/ansible/issues/46953)
- zabbix_template - Failed template import will no longer leave empty templates configured on Zabbix server
- zabbix_template - Fixed cryptic error when ``template_groups`` option wasn't provided (https://github.com/ansible/ansible/issues/50834)
- zabbix_template - Fixed idempotency of the module when using ``link_templates``, ``macros`` or ``template_json`` options (https://github.com/ansible/ansible/issues/48337)
- zone connection - Support empty files with copying to target (https://github.com/ansible/ansible/issues/36725)

New Plugins
-----------

Become
~~~~~~

- doas - Do As user
- dzdo - Centrify's Direct Authorize
- enable - Switch to elevated permissions on a network device
- ksu - Kerberos substitute user
- machinectl - Systemd's machinectl privilege escalation
- pbrun - PowerBroker run
- pfexec - profile based execution
- pmrun - Privilege Manager run
- runas - Run As user
- sesu - CA Privileged Access Manager
- su - Substitute User
- sudo - Substitute User DO

Callback
~~~~~~~~

- aws_resource_actions - summarizes all "resource:actions" completed
- cgroup_perf_recap - Profiles system activity of tasks and full execution using cgroups
- nrdp - post task result to a nagios server through nrdp

Cliconf
~~~~~~~

- edgeswitch - Use edgeswitch cliconf to run command on EdgeSwitch platform
- frr - Use frr cliconf to run command on Free Range Routing platform
- netvisor - Use netvisor cliconf to run command on Pluribus netvisor platform

Connection
~~~~~~~~~~

- napalm - Provides persistent connection using NAPALM
- podman - Interact with an existing podman container
- qubes - Interact with an existing QubesOS AppVM
- vmware_tools - Execute tasks inside a VM via VMware Tools

Httpapi
~~~~~~~

- checkpoint - HttpApi Plugin for Checkpoint devices
- exos - Use EXOS REST APIs to communicate with EXOS platform
- fortimanager - HttpApi Plugin for Fortinet FortiManager Appliance or VM
- qradar - HttpApi Plugin for IBM QRadar appliances
- restconf - HttpApi Plugin for devices supporting Restconf API
- splunk - HttpApi Plugin for Splunk

Inventory
~~~~~~~~~

- cloudscale - cloudscale.ch inventory source
- docker_swarm - Ansible dynamic inventory plugin for Docker swarm nodes.
- gitlab_runners - Ansible dynamic inventory plugin for Gitlab runners.
- hcloud - Ansible dynamic inventory plugin for the Hetzner Cloud.
- kubevirt - KubeVirt inventory source
- linode - Ansible dynamic inventory plugin for Linode.
- toml - Uses a specific TOML file as an inventory source.

Lookup
~~~~~~

- aws_secret - Look up secrets stored in AWS Secrets Manager.
- laps_password - Retrieves the LAPS password for a server.
- manifold - get credentials from Manifold.co
- rabbitmq - Retrieve messages from an AMQP/AMQPS RabbitMQ queue.
- skydive - Query Skydive objects
- varnames - Lookup matching variable names

Shell
~~~~~

- cmd - Windows Command Prompt

New Modules
-----------

Cloud
~~~~~

alicloud
^^^^^^^^

- ali_instance - Create, Start, Stop, Restart or Terminate an Instance in ECS. Add or Remove Instance to/from a Security Group.
- ali_instance_facts - Gather facts on instances of Alibaba Cloud ECS.

amazon
^^^^^^

- aws_codecommit - Manage repositories in AWS CodeCommit
- aws_secret - Manage secrets stored in AWS Secrets Manager.
- aws_ses_rule_set - Manages SES inbound receipt rule sets
- ec2_launch_template - Manage EC2 launch templates
- ec2_transit_gateway - Create and delete AWS Transit Gateways.
- iam_password_policy - Update an IAM Password Policy
- redshift_cross_region_snapshots - Manage Redshift Cross Region Snapshots

azure
^^^^^

- azure_rm_aksversion_facts - Get available kubernetes versions supported by Azure Kubernetes Service.
- azure_rm_applicationsecuritygroup - Manage Azure Application Security Group.
- azure_rm_applicationsecuritygroup_facts - Get Azure Application Security Group facts.
- azure_rm_cdnendpoint - Manage a Azure CDN endpoint.
- azure_rm_cdnendpoint_facts - Get Azure CDN endpoint facts
- azure_rm_cdnprofile - Manage a Azure CDN profile.
- azure_rm_cdnprofile_facts - Get Azure CDN profile facts
- azure_rm_containerinstance_facts - Get Azure Container Instance facts.
- azure_rm_cosmosdbaccount - Manage Azure Database Account instance.
- azure_rm_cosmosdbaccount_facts - Get Azure Cosmos DB Account facts.
- azure_rm_deployment_facts - Get Azure Deployment facts.
- azure_rm_devtestlab - Manage Azure DevTest Lab instance.
- azure_rm_devtestlab_facts - Get Azure DevTest Lab facts.
- azure_rm_devtestlabarmtemplate_facts - Get Azure DevTest Lab ARM Template facts.
- azure_rm_devtestlabartifact_facts - Get Azure DevTest Lab Artifact facts.
- azure_rm_devtestlabartifactsource - Manage Azure DevTest Labs Artifacts Source instance.
- azure_rm_devtestlabartifactsource_facts - Get Azure DevTest Lab Artifact Source facts.
- azure_rm_devtestlabcustomimage - Manage Azure DevTest Lab Custom Image instance.
- azure_rm_devtestlabcustomimage_facts - Get Azure DevTest Lab Custom Image facts.
- azure_rm_devtestlabenvironment - Manage Azure DevTest Lab Environment instance.
- azure_rm_devtestlabenvironment_facts - Get Azure Environment facts.
- azure_rm_devtestlabpolicy - Manage Azure Policy instance.
- azure_rm_devtestlabpolicy_facts - Get Azure DTL Policy facts.
- azure_rm_devtestlabschedule - Manage Azure DevTest Lab Schedule instance.
- azure_rm_devtestlabschedule_facts - Get Azure Schedule facts.
- azure_rm_devtestlabvirtualmachine - Manage Azure DevTest Lab Virtual Machine instance.
- azure_rm_devtestlabvirtualmachine_facts - Get Azure DevTest Lab Virtual Machine facts.
- azure_rm_devtestlabvirtualnetwork - Manage Azure DevTest Lab Virtual Network instance.
- azure_rm_devtestlabvirtualnetwork_facts - Get Azure DevTest Lab Virtual Network facts.
- azure_rm_hdinsightcluster - Manage Azure HDInsight Cluster instance.
- azure_rm_hdinsightcluster_facts - Get Azure HDInsight Cluster facts.
- azure_rm_image_facts - Get facts about azure custom images.
- azure_rm_loganalyticsworkspace - Manage Azure Log Analytics workspaces.
- azure_rm_loganalyticsworkspace_facts - Get facts of Azure Log Analytics workspaces.
- azure_rm_mariadbconfiguration - Manage Configuration instance.
- azure_rm_mariadbconfiguration_facts - Get Azure MariaDB Configuration facts.
- azure_rm_mariadbdatabase - Manage MariaDB Database instance.
- azure_rm_mariadbdatabase_facts - Get Azure MariaDB Database facts.
- azure_rm_mariadbfirewallrule - Manage MariaDB firewall rule instance.
- azure_rm_mariadbfirewallrule_facts - Get Azure MariaDB Firewall Rule facts.
- azure_rm_mariadbserver - Manage MariaDB Server instance.
- azure_rm_mariadbserver_facts - Get Azure MariaDB Server facts.
- azure_rm_mysqlconfiguration - Manage Configuration instance.
- azure_rm_mysqlconfiguration_facts - Get Azure MySQL Configuration facts.
- azure_rm_mysqlfirewallrule - Manage MySQL firewall rule instance.
- azure_rm_mysqlfirewallrule_facts - Get Azure MySQL Firewall Rule facts.
- azure_rm_postgresqlconfiguration - Manage Azure PostgreSQL Configuration.
- azure_rm_postgresqlconfiguration_facts - Get Azure PostgreSQL Configuration facts.
- azure_rm_postgresqlfirewallrule - Manage PostgreSQL firewall rule instance.
- azure_rm_postgresqlfirewallrule_facts - Get Azure PostgreSQL Firewall Rule facts.
- azure_rm_rediscache - Manage Azure Cache for Redis instance.
- azure_rm_rediscache_facts - Get Azure Cache for Redis instance facts
- azure_rm_rediscachefirewallrule - Manage Azure Cache for Redis Firewall rules.
- azure_rm_roleassignment - Manage Azure Role Assignment.
- azure_rm_roleassignment_facts - Gets Azure Role Assignment facts.
- azure_rm_roledefinition - Manage Azure Role Definition.
- azure_rm_roledefinition_facts - Get Azure Role Definition facts.
- azure_rm_servicebus - Manage Azure Service Bus.
- azure_rm_servicebus_facts - Get servicebus facts.
- azure_rm_servicebusqueue - Manage Azure Service Bus queue.
- azure_rm_servicebussaspolicy - Manage Azure Service Bus SAS policy.
- azure_rm_servicebustopic - Manage Azure Service Bus.
- azure_rm_servicebustopicsubscription - Manage Azure Service Bus subscription.
- azure_rm_sqldatabase_facts - Get Azure SQL Database facts.
- azure_rm_sqlfirewallrule_facts - Get Azure SQL Firewall Rule facts.
- azure_rm_subnet_facts - Get Azure Subnet facts.
- azure_rm_virtualmachineextension_facts - Get Azure Virtual Machine Extension facts.
- azure_rm_virtualmachinescalesetextension - Managed Azure Virtual Machine Scale Set extension
- azure_rm_virtualmachinescalesetextension_facts - Get Azure Virtual Machine Scale Set Extension facts.
- azure_rm_virtualmachinescalesetinstance - Get Azure Virtual Machine Scale Set Instance facts.
- azure_rm_virtualmachinescalesetinstance_facts - Get Azure Virtual Machine Scale Set Instance facts.
- azure_rm_virtualnetworkgateway - Manage Azure virtual network gateways.
- azure_rm_virtualnetworkpeering - Manage Azure Virtual Network Peering.
- azure_rm_virtualnetworkpeering_facts - Get facts of Azure Virtual Network Peering.
- azure_rm_webappslot - Manage Azure Web App slot.

cloudscale
^^^^^^^^^^

- cloudscale_server_group - Manages server groups on the cloudscale.ch IaaS service
- cloudscale_volume - Manages volumes on the cloudscale.ch IaaS service

cloudstack
^^^^^^^^^^

- cs_image_store - Manages CloudStack Image Stores.
- cs_instance_password_reset - Allows resetting VM the default passwords on Apache CloudStack based clouds.
- cs_physical_network - Manages physical networks on Apache CloudStack based clouds.
- cs_traffic_type - Manages traffic types on CloudStack Physical Networks
- cs_vlan_ip_range - Manages VLAN IP ranges on Apache CloudStack based clouds.

digital_ocean
^^^^^^^^^^^^^

- digital_ocean_droplet - Create and delete a DigitalOcean droplet
- digital_ocean_firewall_facts - Gather facts about DigitalOcean firewalls

docker
^^^^^^

- docker_config - Manage docker configs.
- docker_container_info - Retrieves facts about docker container
- docker_host_info - Retrieves facts about docker host and lists of objects of the services.
- docker_network_info - Retrieves facts about docker network
- docker_node - Manage Docker Swarm node
- docker_node_info - Retrieves facts about docker swarm node from Swarm Manager
- docker_prune - Allows to prune various docker objects
- docker_stack - docker stack module
- docker_swarm_info - Retrieves facts about Docker Swarm cluster.
- docker_swarm_service_info - Retrieves information about docker services from a Swarm Manager
- docker_volume_info - Retrieve facts about Docker volumes

google
^^^^^^

- gcp_bigquery_dataset - Creates a GCP Dataset
- gcp_bigquery_dataset_facts - Gather facts for GCP Dataset
- gcp_bigquery_table - Creates a GCP Table
- gcp_bigquery_table_facts - Gather facts for GCP Table
- gcp_cloudbuild_trigger - Creates a GCP Trigger
- gcp_cloudbuild_trigger_facts - Gather facts for GCP Trigger
- gcp_compute_interconnect_attachment - Creates a GCP InterconnectAttachment
- gcp_compute_interconnect_attachment_facts - Gather facts for GCP InterconnectAttachment
- gcp_compute_region_disk - Creates a GCP RegionDisk
- gcp_compute_region_disk_facts - Gather facts for GCP RegionDisk
- gcp_container_cluster_facts - Gather facts for GCP Cluster
- gcp_container_node_pool_facts - Gather facts for GCP NodePool
- gcp_dns_managed_zone_facts - Gather facts for GCP ManagedZone
- gcp_dns_resource_record_set_facts - Gather facts for GCP ResourceRecordSet
- gcp_iam_role - Creates a GCP Role
- gcp_iam_role_facts - Gather facts for GCP Role
- gcp_iam_service_account - Creates a GCP ServiceAccount
- gcp_iam_service_account_facts - Gather facts for GCP ServiceAccount
- gcp_iam_service_account_key - Creates a GCP ServiceAccountKey
- gcp_pubsub_subscription_facts - Gather facts for GCP Subscription
- gcp_pubsub_topic_facts - Gather facts for GCP Topic
- gcp_redis_instance - Creates a GCP Instance
- gcp_redis_instance_facts - Gather facts for GCP Instance
- gcp_resourcemanager_project - Creates a GCP Project
- gcp_resourcemanager_project_facts - Gather facts for GCP Project
- gcp_sourcerepo_repository - Creates a GCP Repository
- gcp_sourcerepo_repository_facts - Gather facts for GCP Repository
- gcp_spanner_database_facts - Gather facts for GCP Database
- gcp_spanner_instance_facts - Gather facts for GCP Instance
- gcp_sql_database_facts - Gather facts for GCP Database
- gcp_sql_instance_facts - Gather facts for GCP Instance
- gcp_sql_user_facts - Gather facts for GCP User
- gcp_storage_object - Creates a GCP Object

hcloud
^^^^^^

- hcloud_datacenter_facts - Gather facts about the Hetzner Cloud datacenters.
- hcloud_floating_ip_facts - Gather facts about the Hetzner Cloud Floating IPs.
- hcloud_image_facts - Gather facts about your Hetzner Cloud images.
- hcloud_location_facts - Gather facts about your Hetzner Cloud locations.
- hcloud_server - Create and manage cloud servers on the Hetzner Cloud.
- hcloud_server_facts - Gather facts about your Hetzner Cloud servers.
- hcloud_server_type_facts - Gather facts about the Hetzner Cloud server types.
- hcloud_ssh_key - Create and manage ssh keys on the Hetzner Cloud.
- hcloud_ssh_key_facts - Gather facts about your Hetzner Cloud ssh_keys.
- hcloud_volume - Create and manage block volumes on the Hetzner Cloud.
- hcloud_volume_facts - Gather facts about your Hetzner Cloud volumes.

huawei
^^^^^^

- hwc_network_vpc - Creates a Huawei Cloud VPC
- hwc_smn_topic - Creates a resource of SMNTopic in Huaweicloud Cloud

kubevirt
^^^^^^^^

- kubevirt_cdi_upload - Upload local VM images to CDI Upload Proxy.
- kubevirt_preset - Manage KubeVirt virtual machine presets
- kubevirt_pvc - Manage PVCs on Kubernetes
- kubevirt_rs - Manage KubeVirt virtual machine replica sets
- kubevirt_template - Manage KubeVirt templates
- kubevirt_vm - Manage KubeVirt virtual machine

linode
^^^^^^

- linode_v4 - Manage instances on the Linode cloud.

memset
^^^^^^

- memset_memstore_facts - Retrieve Memstore product usage information.
- memset_server_facts - Retrieve server information.

online
^^^^^^

- online_server_facts - Gather facts about Online servers.

openstack
^^^^^^^^^

- os_coe_cluster - Add/Remove COE cluster from OpenStack Cloud

oracle
^^^^^^

- oci_vcn - Manage Virtual Cloud Networks(VCN) in OCI

ovh
^^^

- ovh_ip_failover - Manage OVH IP failover address

ovirt
^^^^^

- ovirt_event - Create or delete an event in oVirt/RHV
- ovirt_event_facts - This module can be used to retrieve facts about one or more oVirt/RHV events
- ovirt_instance_type - Module to manage Instance Types in oVirt/RHV
- ovirt_role - Module to manage roles in oVirt/RHV
- ovirt_vnic_profile - Module to manage vNIC profile of network in oVirt/RHV

podman
^^^^^^

- podman_image - Pull images for use by podman
- podman_image_info - Gather info about images using podman

scaleway
^^^^^^^^

- scaleway_ip - Scaleway IP management module
- scaleway_lb - Scaleway load-balancer management module
- scaleway_security_group - Scaleway Security Group management module
- scaleway_security_group_rule - Scaleway Security Group Rule management module
- scaleway_user_data - Scaleway user_data management module

smartos
^^^^^^^

- nictagadm - Manage nic tags on SmartOS systems

vmware
^^^^^^

- vcenter_extension - Register/deregister vCenter Extensions
- vcenter_extension_facts - Gather facts vCenter extensions
- vmware_drs_group - Creates vm/host group in a given cluster.
- vmware_drs_group_facts - Gathers facts about DRS VM/Host groups on the given cluster
- vmware_dvs_portgroup_facts - Gathers facts DVS portgroup configurations
- vmware_dvswitch_lacp - Manage LACP configuration on a Distributed Switch
- vmware_dvswitch_pvlans - Manage Private VLAN configuration of a Distributed Switch
- vmware_dvswitch_uplink_pg - Manage uplink portproup configuration of a Distributed Switch
- vmware_export_ovf - Exports a VMware virtual machine to an OVF file, device files and a manifest file
- vmware_guest_customization_facts - Gather facts about VM customization specifications
- vmware_guest_disk - Manage disks related to virtual machine in given vCenter infrastructure
- vmware_guest_tools_upgrade - Module to upgrade VMTools
- vmware_guest_video - Modify video card configurations of specified virtual machine in given vCenter infrastructure
- vmware_guest_vnc - Manages VNC remote display on virtual machines in vCenter
- vmware_host_active_directory - Joins an ESXi host system to an Active Directory domain or leaves it
- vmware_host_feature_facts - Gathers facts about an ESXi host's feature capability information
- vmware_host_hyperthreading - Enables/Disables Hyperthreading optimization for an ESXi host system
- vmware_host_ipv6 - Enables/Disables IPv6 support for an ESXi host system
- vmware_host_kernel_manager - Manage kernel module options on ESXi hosts
- vmware_host_powermgmt_policy - Manages the Power Management Policy of an ESXI host system
- vmware_host_scanhba - Rescan host HBA's and optionally refresh the storage system
- vmware_host_snmp - Configures SNMP on an ESXi host system
- vmware_host_vmhba_facts - Gathers facts about vmhbas available on the given ESXi host
- vmware_object_role_permission - Manage local roles on an ESXi host
- vmware_tag_manager - Manage association of VMware tags with VMware objects
- vmware_vcenter_settings - Configures general settings on a vCenter server
- vmware_vcenter_statistics - Configures statistics on a vCenter server
- vmware_vm_host_drs_rule - Creates vm/host group in a given cluster
- vmware_vspan_session - Create or remove a Port Mirroring session.
- vsphere_file - Manage files on a vCenter datastore

xenserver
^^^^^^^^^

- xenserver_guest - Manages virtual machines running on Citrix XenServer host or pool
- xenserver_guest_facts - Gathers facts for virtual machines running on Citrix XenServer host or pool
- xenserver_guest_powerstate - Manages power states of virtual machines running on Citrix XenServer host or pool

Clustering
~~~~~~~~~~

k8s
^^^

- k8s_auth - Authenticate to Kubernetes clusters which require an explicit login step
- k8s_service - Manage Services on Kubernetes

Crypto
~~~~~~

- get_certificate - Get a certificate from a host:port
- luks_device - Manage encrypted (LUKS) devices
- openssh_cert - Generate OpenSSH host or user certificates.
- openssh_keypair - Generate OpenSSH private and public keys.
- openssl_certificate_info - Provide information of OpenSSL X.509 certificates
- openssl_csr_info - Provide information of OpenSSL Certificate Signing Requests (CSR)
- openssl_privatekey_info - Provide information for OpenSSL private keys

acme
^^^^

- acme_inspect - Send direct requests to an ACME server

Database
~~~~~~~~

aerospike
^^^^^^^^^

- aerospike_migrations - Check or wait for migrations between nodes

mongodb
^^^^^^^

- mongodb_replicaset - Initialises a MongoDB replicaset.
- mongodb_shard - Add and remove shards from a MongoDB Cluster.

postgresql
^^^^^^^^^^

- postgresql_idx - Create or drop indexes from a PostgreSQL database
- postgresql_info - Gather information about PostgreSQL servers
- postgresql_membership - Add or remove PostgreSQL roles from groups
- postgresql_owner - Change an owner of PostgreSQL database object
- postgresql_pg_hba - Add, remove or modify a rule in a pg_hba file
- postgresql_ping - Check remote PostgreSQL server availability
- postgresql_query - Run PostgreSQL queries
- postgresql_set - Change a PostgreSQL server configuration parameter
- postgresql_slot - Add or remove slots from a PostgreSQL database
- postgresql_table - Create, drop, or modify a PostgreSQL table
- postgresql_tablespace - Add or remove PostgreSQL tablespaces from remote hosts

Files
~~~~~

- read_csv - Read a CSV file

Identity
~~~~~~~~

keycloak
^^^^^^^^

- keycloak_group - Allows administration of Keycloak groups via Keycloak API

Messaging
~~~~~~~~~

rabbitmq
^^^^^^^^

- rabbitmq_global_parameter - Manage RabbitMQ global parameters
- rabbitmq_vhost_limits - Manage the state of virtual host limits in RabbitMQ

Monitoring
~~~~~~~~~~

zabbix
^^^^^^

- zabbix_action - Create/Delete/Update Zabbix actions
- zabbix_map - Create/update/delete Zabbix maps

Net Tools
~~~~~~~~~

netbox
^^^^^^

- netbox_device - Create, update or delete devices within Netbox
- netbox_interface - Creates or removes interfaces from Netbox
- netbox_ip_address - Creates or removes IP addresses from Netbox
- netbox_prefix - Creates or removes prefixes from Netbox
- netbox_site - Creates or removes sites from Netbox

nios
^^^^

- nios_fixed_address - Configure Infoblox NIOS DHCP Fixed Address
- nios_member - Configure Infoblox NIOS members
- nios_nsgroup - Configure InfoBlox DNS Nameserver Groups

Network
~~~~~~~

aci
^^^

- aci_access_port_block_to_access_port - Manage port blocks of Fabric interface policy leaf profile interface selectors (infra:HPortS, infra:PortBlk)
- aci_access_sub_port_block_to_access_port - Manage sub port blocks of Fabric interface policy leaf profile interface selectors (infra:HPortS, infra:SubPortBlk)
- aci_fabric_scheduler - This modules creates ACI schedulers.
- aci_firmware_group - This module creates a firmware group
- aci_firmware_group_node - This modules adds and remove nodes from the firmware group
- aci_firmware_policy - This creates a firmware policy
- aci_maintenance_group - This creates an ACI maintenance group
- aci_maintenance_group_node - Manage maintenance group nodes
- aci_maintenance_policy - Manage firmware maintenance policies
- mso_label - Manage labels
- mso_role - Manage roles
- mso_schema - Manage schemas
- mso_schema_site - Manage sites in schemas
- mso_schema_site_anp - Manage site-local Application Network Profiles (ANPs) in schema template
- mso_schema_site_anp_epg - Manage site-local Endpoint Groups (EPGs) in schema template
- mso_schema_site_anp_epg_staticleaf - Manage site-local EPG static leafs in schema template
- mso_schema_site_anp_epg_staticport - Manage site-local EPG static ports in schema template
- mso_schema_site_anp_epg_subnet - Manage site-local EPG subnets in schema template
- mso_schema_site_bd - Manage site-local Bridge Domains (BDs) in schema template
- mso_schema_site_bd_l3out - Manage site-local BD l3out's in schema template
- mso_schema_site_bd_subnet - Manage site-local BD subnets in schema template
- mso_schema_site_vrf - Manage site-local VRFs in schema template
- mso_schema_site_vrf_region - Manage site-local VRF regions in schema template
- mso_schema_site_vrf_region_cidr - Manage site-local VRF region CIDRs in schema template
- mso_schema_site_vrf_region_cidr_subnet - Manage site-local VRF regions in schema template
- mso_schema_template - Manage templates in schemas
- mso_schema_template_anp - Manage Application Network Profiles (ANPs) in schema templates
- mso_schema_template_anp_epg - Manage Endpoint Groups (EPGs) in schema templates
- mso_schema_template_anp_epg_contract - Manage EPG contracts in schema templates
- mso_schema_template_anp_epg_subnet - Manage EPG subnets in schema templates
- mso_schema_template_bd - Manage Bridge Domains (BDs) in schema templates
- mso_schema_template_bd_subnet - Manage BD subnets in schema templates
- mso_schema_template_contract_filter - Manage contract filters in schema templates
- mso_schema_template_deploy - Deploy schema templates to sites
- mso_schema_template_externalepg - Manage external EPGs in schema templates
- mso_schema_template_filter_entry - Manage filter entries in schema templates
- mso_schema_template_l3out - Manage l3outs in schema templates
- mso_schema_template_vrf - Manage VRFs in schema templates
- mso_site - Manage sites
- mso_tenant - Manage tenants
- mso_user - Manage users

asa
^^^

- asa_og - Manage object groups on a Cisco ASA

checkpoint
^^^^^^^^^^

- checkpoint_access_layer_facts - Get access layer facts on Check Point over Web Services API
- checkpoint_access_rule - Manages access rules on Checkpoint over Web Services API
- checkpoint_access_rule_facts - Get access rules objects facts on Checkpoint over Web Services API
- checkpoint_host - Manages host objects on Checkpoint over Web Services API
- checkpoint_host_facts - Get host objects facts on Checkpoint over Web Services API
- checkpoint_object_facts - Get object facts on Check Point over Web Services API
- checkpoint_run_script - Run scripts on Checkpoint devices over Web Services API
- checkpoint_session - Manages session objects on Check Point over Web Services API
- checkpoint_task_facts - Get task objects facts on Checkpoint over Web Services API

cnos
^^^^

- cnos_banner - Manage multiline banners on Lenovo CNOS devices
- cnos_l2_interface - Manage Layer-2 interface on Lenovo CNOS devices.
- cnos_l3_interface - Manage Layer-3 interfaces on Lenovo CNOS network devices.
- cnos_linkagg - Manage link aggregation groups on Lenovo CNOS devices
- cnos_lldp - Manage LLDP configuration on Lenovo CNOS network devices.
- cnos_logging - Manage logging on network devices
- cnos_static_route - Manage static IP routes on Lenovo CNOS network devices
- cnos_system - Manage the system attributes on Lenovo CNOS devices
- cnos_user - Manage the collection of local users on Lenovo CNOS devices
- cnos_vrf - Manage VRFs on Lenovo CNOS network devices

edgeswitch
^^^^^^^^^^

- edgeswitch_facts - Collect facts from remote devices running Edgeswitch
- edgeswitch_vlan - Manage VLANs on Ubiquiti Edgeswitch network devices

eos
^^^

- eos_bgp - Configure global BGP protocol settings on Arista EOS.

f5
^^

- bigip_apm_policy_fetch - Exports the APM policy or APM access profile from remote nodes.
- bigip_apm_policy_import - Manage BIG-IP APM policy or APM access profile imports
- bigip_asm_policy_fetch - Exports the asm policy from remote nodes.
- bigip_asm_policy_import - Manage BIG-IP ASM policy imports
- bigip_asm_policy_manage - Manage BIG-IP ASM policies
- bigip_asm_policy_server_technology - Manages Server Technology on ASM policy
- bigip_asm_policy_signature_set - Manages Signature Sets on ASM policy
- bigip_device_auth_ldap - Manage LDAP device authentication settings on BIG-IP
- bigip_device_ha_group - Manage HA group settings on a BIG-IP system
- bigip_device_syslog - Manage system-level syslog settings on BIG-IP
- bigip_dns_cache_resolver - Manage DNS resolver cache configurations on BIG-IP
- bigip_dns_nameserver - Manage LTM DNS nameservers on a BIG-IP
- bigip_dns_resolver - Manage DNS resolvers on a BIG-IP
- bigip_dns_zone - Manage DNS zones on BIG-IP
- bigip_file_copy - Manage files in datastores on a BIG-IP
- bigip_firewall_dos_vector - Manage attack vector configuration in an AFM DoS profile
- bigip_firewall_global_rules - Manage AFM global rule settings on BIG-IP
- bigip_gtm_topology_record - Manages GTM Topology Records
- bigip_gtm_topology_region - Manages GTM Topology Regions
- bigip_ike_peer - Manage IPSec IKE Peer configuration on BIG-IP
- bigip_imish_config - Manage BIG-IP advanced routing configuration sections
- bigip_ipsec_policy - Manage IPSec policies on a BIG-IP
- bigip_monitor_gateway_icmp - Manages F5 BIG-IP LTM gateway ICMP monitors
- bigip_monitor_ldap - Manages BIG-IP LDAP monitors
- bigip_password_policy - Manages the authentication password policy on a BIG-IP
- bigip_profile_analytics - Manage HTTP analytics profiles on a BIG-IP
- bigip_profile_fastl4 - Manages Fast L4 profiles
- bigip_profile_http2 - Manage HTTP2 profiles on a BIG-IP
- bigip_profile_persistence_cookie - Manage cookie persistence profiles on BIG-IP
- bigip_profile_server_ssl - Manages server SSL profiles on a BIG-IP
- bigip_ssl_ocsp - Manage OCSP configurations on BIG-IP
- bigip_sys_daemon_log_tmm - Manage BIG-IP tmm daemon log settings
- bigip_traffic_selector - Manage IPSec Traffic Selectors on BIG-IP
- bigiq_device_discovery - Manage BIG-IP devices through BIG-IQ
- bigiq_device_facts - Collect facts from F5 BIG-IQ devices

fortimanager
^^^^^^^^^^^^

- fmgr_device - Add or remove device from FortiManager.
- fmgr_device_config - Edit device configurations
- fmgr_device_group - Alter FortiManager device groups.
- fmgr_device_provision_template - Manages Device Provisioning Templates in FortiManager.
- fmgr_fwobj_address - Allows the management of firewall objects in FortiManager
- fmgr_fwobj_ippool - Allows the editing of IP Pool Objects within FortiManager.
- fmgr_fwobj_ippool6 - Allows the editing of IP Pool Objects within FortiManager.
- fmgr_fwobj_service - Manages FortiManager Firewall Service Objects.
- fmgr_fwobj_vip - Manages Virtual IPs objects in FortiManager
- fmgr_fwpol_ipv4 - Allows the add/delete of Firewall Policies on Packages in FortiManager.
- fmgr_fwpol_package - Manages FortiManager Firewall Policies Packages.
- fmgr_ha - Manages the High-Availability State of FortiManager Clusters and Nodes.
- fmgr_query - Query FortiManager data objects for use in Ansible workflows.
- fmgr_secprof_appctrl - Manage application control security profiles
- fmgr_secprof_av - Manage security profile
- fmgr_secprof_dns - Manage DNS security profiles in FortiManager
- fmgr_secprof_ips - Managing IPS security profiles in FortiManager
- fmgr_secprof_profile_group - Manage security profiles within FortiManager
- fmgr_secprof_proxy - Manage proxy security profiles in FortiManager
- fmgr_secprof_spam - spam filter profile for FMG
- fmgr_secprof_ssl_ssh - Manage SSL and SSH security profiles in FortiManager
- fmgr_secprof_voip - VOIP security profiles in FMG
- fmgr_secprof_waf - FortiManager web application firewall security profile
- fmgr_secprof_wanopt - WAN optimization
- fmgr_secprof_web - Manage web filter security profiles in FortiManager

fortios
^^^^^^^

- fortios_antivirus_heuristic - Configure global heuristic options in Fortinet's FortiOS and FortiGate.
- fortios_antivirus_profile - Configure AntiVirus profiles in Fortinet's FortiOS and FortiGate.
- fortios_antivirus_quarantine - Configure quarantine options in Fortinet's FortiOS and FortiGate.
- fortios_antivirus_settings - Configure AntiVirus settings in Fortinet's FortiOS and FortiGate.
- fortios_application_custom - Configure custom application signatures in Fortinet's FortiOS and FortiGate.
- fortios_application_group - Configure firewall application groups in Fortinet's FortiOS and FortiGate.
- fortios_application_list - Configure application control lists.
- fortios_application_name - Configure application signatures in Fortinet's FortiOS and FortiGate.
- fortios_application_rule_settings - Configure application rule settings in Fortinet's FortiOS and FortiGate.
- fortios_authentication_rule - Configure Authentication Rules in Fortinet's FortiOS and FortiGate.
- fortios_authentication_scheme - Configure Authentication Schemes in Fortinet's FortiOS and FortiGate.
- fortios_authentication_setting - Configure authentication setting in Fortinet's FortiOS and FortiGate.
- fortios_dlp_filepattern - Configure file patterns used by DLP blocking in Fortinet's FortiOS and FortiGate.
- fortios_dlp_fp_doc_source - Create a DLP fingerprint database by allowing the FortiGate to access a file server containing files from which to create fingerprints in Fortinet's FortiOS and FortiGate.
- fortios_dlp_fp_sensitivity - Create self-explanatory DLP sensitivity levels to be used when setting sensitivity under config fp-doc-source in Fortinet's FortiOS and FortiGate.
- fortios_dlp_sensor - Configure DLP sensors in Fortinet's FortiOS and FortiGate.
- fortios_dlp_settings - Designate logical storage for DLP fingerprint database in Fortinet's FortiOS and FortiGate.
- fortios_dnsfilter_domain_filter - Configure DNS domain filters in Fortinet's FortiOS and FortiGate.
- fortios_dnsfilter_profile - Configure DNS domain filter profiles in Fortinet's FortiOS and FortiGate.
- fortios_endpoint_control_client - Configure endpoint control client lists in Fortinet's FortiOS and FortiGate.
- fortios_endpoint_control_forticlient_ems - Configure FortiClient Enterprise Management Server (EMS) entries in Fortinet's FortiOS and FortiGate.
- fortios_endpoint_control_forticlient_registration_sync - Configure FortiClient registration synchronization settings in Fortinet's FortiOS and FortiGate.
- fortios_endpoint_control_profile - Configure FortiClient endpoint control profiles in Fortinet's FortiOS and FortiGate.
- fortios_endpoint_control_settings - Configure endpoint control settings in Fortinet's FortiOS and FortiGate.
- fortios_extender_controller_extender - Extender controller configuration in Fortinet's FortiOS and FortiGate.
- fortios_firewall_DoS_policy - Configure IPv4 DoS policies in Fortinet's FortiOS and FortiGate.
- fortios_firewall_DoS_policy6 - Configure IPv6 DoS policies in Fortinet's FortiOS and FortiGate.
- fortios_firewall_address - Configure IPv4 addresses.
- fortios_firewall_address6 - Configure IPv6 firewall addresses in Fortinet's FortiOS and FortiGate.
- fortios_firewall_address6_template - Configure IPv6 address templates in Fortinet's FortiOS and FortiGate.
- fortios_firewall_addrgrp - Configure IPv4 address groups.
- fortios_firewall_addrgrp6 - Configure IPv6 address groups in Fortinet's FortiOS and FortiGate.
- fortios_firewall_auth_portal - Configure firewall authentication portals in Fortinet's FortiOS and FortiGate.
- fortios_firewall_central_snat_map - Configure central SNAT policies in Fortinet's FortiOS and FortiGate.
- fortios_firewall_dnstranslation - Configure DNS translation in Fortinet's FortiOS and FortiGate.
- fortios_firewall_identity_based_route - Configure identity based routing in Fortinet's FortiOS and FortiGate.
- fortios_firewall_interface_policy - Configure IPv4 interface policies in Fortinet's FortiOS and FortiGate.
- fortios_firewall_interface_policy6 - Configure IPv6 interface policies in Fortinet's FortiOS and FortiGate.
- fortios_firewall_internet_service - Show Internet Service application in Fortinet's FortiOS and FortiGate.
- fortios_firewall_internet_service_custom - Configure custom Internet Services in Fortinet's FortiOS and FortiGate.
- fortios_firewall_internet_service_group - Configure group of Internet Service in Fortinet's FortiOS and FortiGate.
- fortios_firewall_ip_translation - Configure firewall IP-translation in Fortinet's FortiOS and FortiGate.
- fortios_firewall_ipmacbinding_setting - Configure IP to MAC binding settings in Fortinet's FortiOS and FortiGate.
- fortios_firewall_ipmacbinding_table - Configure IP to MAC address pairs in the IP/MAC binding table in Fortinet's FortiOS and FortiGate.
- fortios_firewall_ippool - Configure IPv4 IP pools in Fortinet's FortiOS and FortiGate.
- fortios_firewall_ippool6 - Configure IPv6 IP pools in Fortinet's FortiOS and FortiGate.
- fortios_firewall_ipv6_eh_filter - Configure IPv6 extension header filter in Fortinet's FortiOS and FortiGate.
- fortios_firewall_ldb_monitor - Configure server load balancing health monitors in Fortinet's FortiOS and FortiGate.
- fortios_firewall_local_in_policy - Configure user defined IPv4 local-in policies in Fortinet's FortiOS and FortiGate.
- fortios_firewall_local_in_policy6 - Configure user defined IPv6 local-in policies in Fortinet's FortiOS and FortiGate.
- fortios_firewall_multicast_address - Configure multicast addresses in Fortinet's FortiOS and FortiGate.
- fortios_firewall_multicast_address6 - Configure IPv6 multicast address in Fortinet's FortiOS and FortiGate.
- fortios_firewall_multicast_policy - Configure multicast NAT policies in Fortinet's FortiOS and FortiGate.
- fortios_firewall_multicast_policy6 - Configure IPv6 multicast NAT policies in Fortinet's FortiOS and FortiGate.
- fortios_firewall_policy - Configure IPv4 policies.
- fortios_firewall_policy46 - Configure IPv4 to IPv6 policies in Fortinet's FortiOS and FortiGate.
- fortios_firewall_policy6 - Configure IPv6 policies in Fortinet's FortiOS and FortiGate.
- fortios_firewall_policy64 - Configure IPv6 to IPv4 policies in Fortinet's FortiOS and FortiGate.
- fortios_firewall_profile_group - Configure profile groups in Fortinet's FortiOS and FortiGate.
- fortios_firewall_profile_protocol_options - Configure protocol options in Fortinet's FortiOS and FortiGate.
- fortios_firewall_proxy_address - Web proxy address configuration in Fortinet's FortiOS and FortiGate.
- fortios_firewall_proxy_addrgrp - Web proxy address group configuration in Fortinet's FortiOS and FortiGate.
- fortios_firewall_proxy_policy - Configure proxy policies in Fortinet's FortiOS and FortiGate.
- fortios_firewall_schedule_group - Schedule group configuration in Fortinet's FortiOS and FortiGate.
- fortios_firewall_schedule_onetime - Onetime schedule configuration in Fortinet's FortiOS and FortiGate.
- fortios_firewall_schedule_recurring - Recurring schedule configuration in Fortinet's FortiOS and FortiGate.
- fortios_firewall_service_category - Configure service categories in Fortinet's FortiOS and FortiGate.
- fortios_firewall_service_custom - Configure custom services in Fortinet's FortiOS and FortiGate.
- fortios_firewall_service_group - Configure service groups in Fortinet's FortiOS and FortiGate.
- fortios_firewall_shaper_per_ip_shaper - Configure per-IP traffic shaper in Fortinet's FortiOS and FortiGate.
- fortios_firewall_shaper_traffic_shaper - Configure shared traffic shaper in Fortinet's FortiOS and FortiGate.
- fortios_firewall_shaping_policy - Configure shaping policies in Fortinet's FortiOS and FortiGate.
- fortios_firewall_shaping_profile - Configure shaping profiles in Fortinet's FortiOS and FortiGate.
- fortios_firewall_sniffer - Configure sniffer in Fortinet's FortiOS and FortiGate.
- fortios_firewall_ssh_host_key - SSH proxy host public keys in Fortinet's FortiOS and FortiGate.
- fortios_firewall_ssh_local_ca - SSH proxy local CA in Fortinet's FortiOS and FortiGate.
- fortios_firewall_ssh_local_key - SSH proxy local keys in Fortinet's FortiOS and FortiGate.
- fortios_firewall_ssh_setting - SSH proxy settings in Fortinet's FortiOS and FortiGate.
- fortios_firewall_ssl_server - Configure SSL servers in Fortinet's FortiOS and FortiGate.
- fortios_firewall_ssl_setting - SSL proxy settings in Fortinet's FortiOS and FortiGate.
- fortios_firewall_ssl_ssh_profile - Configure SSL/SSH protocol options in Fortinet's FortiOS and FortiGate.
- fortios_firewall_ttl_policy - Configure TTL policies in Fortinet's FortiOS and FortiGate.
- fortios_firewall_vip - Configure virtual IP for IPv4 in Fortinet's FortiOS and FortiGate.
- fortios_firewall_vip46 - Configure IPv4 to IPv6 virtual IPs in Fortinet's FortiOS and FortiGate.
- fortios_firewall_vip6 - Configure virtual IP for IPv6 in Fortinet's FortiOS and FortiGate.
- fortios_firewall_vip64 - Configure IPv6 to IPv4 virtual IPs in Fortinet's FortiOS and FortiGate.
- fortios_firewall_vipgrp - Configure IPv4 virtual IP groups in Fortinet's FortiOS and FortiGate.
- fortios_firewall_vipgrp46 - Configure IPv4 to IPv6 virtual IP groups in Fortinet's FortiOS and FortiGate.
- fortios_firewall_vipgrp6 - Configure IPv6 virtual IP groups in Fortinet's FortiOS and FortiGate.
- fortios_firewall_vipgrp64 - Configure IPv6 to IPv4 virtual IP groups in Fortinet's FortiOS and FortiGate.
- fortios_firewall_wildcard_fqdn_custom - Config global/VDOM Wildcard FQDN address in Fortinet's FortiOS and FortiGate.
- fortios_firewall_wildcard_fqdn_group - Config global Wildcard FQDN address groups in Fortinet's FortiOS and FortiGate.
- fortios_ftp_proxy_explicit - Configure explicit FTP proxy settings in Fortinet's FortiOS and FortiGate.
- fortios_icap_profile - Configure ICAP profiles in Fortinet's FortiOS and FortiGate.
- fortios_icap_server - Configure ICAP servers in Fortinet's FortiOS and FortiGate.
- fortios_ips_custom - Configure IPS custom signature in Fortinet's FortiOS and FortiGate.
- fortios_ips_decoder - Configure IPS decoder in Fortinet's FortiOS and FortiGate.
- fortios_ips_global - Configure IPS global parameter in Fortinet's FortiOS and FortiGate.
- fortios_ips_rule - Configure IPS rules in Fortinet's FortiOS and FortiGate.
- fortios_ips_rule_settings - Configure IPS rule setting in Fortinet's FortiOS and FortiGate.
- fortios_ips_sensor - Configure IPS sensor.
- fortios_ips_settings - Configure IPS VDOM parameter in Fortinet's FortiOS and FortiGate.
- fortios_log_custom_field - Configure custom log fields in Fortinet's FortiOS and FortiGate.
- fortios_log_disk_filter - Configure filters for local disk logging. Use these filters to determine the log messages to record according to severity and type in Fortinet's FortiOS and FortiGate.
- fortios_log_disk_setting - Settings for local disk logging in Fortinet's FortiOS and FortiGate.
- fortios_log_eventfilter - Configure log event filters in Fortinet's FortiOS and FortiGate.
- fortios_log_fortianalyzer2_filter - Filters for FortiAnalyzer in Fortinet's FortiOS and FortiGate.
- fortios_log_fortianalyzer2_setting - Global FortiAnalyzer settings in Fortinet's FortiOS and FortiGate.
- fortios_log_fortianalyzer3_filter - Filters for FortiAnalyzer in Fortinet's FortiOS and FortiGate.
- fortios_log_fortianalyzer3_setting - Global FortiAnalyzer settings in Fortinet's FortiOS and FortiGate.
- fortios_log_fortianalyzer_filter - Filters for FortiAnalyzer in Fortinet's FortiOS and FortiGate.
- fortios_log_fortianalyzer_override_filter - Override filters for FortiAnalyzer in Fortinet's FortiOS and FortiGate.
- fortios_log_fortianalyzer_override_setting - Override FortiAnalyzer settings in Fortinet's FortiOS and FortiGate.
- fortios_log_fortianalyzer_setting - Global FortiAnalyzer settings in Fortinet's FortiOS and FortiGate.
- fortios_log_fortiguard_filter - Filters for FortiCloud in Fortinet's FortiOS and FortiGate.
- fortios_log_fortiguard_override_filter - Override filters for FortiCloud in Fortinet's FortiOS and FortiGate.
- fortios_log_fortiguard_override_setting - Override global FortiCloud logging settings for this VDOM in Fortinet's FortiOS and FortiGate.
- fortios_log_fortiguard_setting - Configure logging to FortiCloud in Fortinet's FortiOS and FortiGate.
- fortios_log_gui_display - Configure how log messages are displayed on the GUI in Fortinet's FortiOS and FortiGate.
- fortios_log_memory_filter - Filters for memory buffer in Fortinet's FortiOS and FortiGate.
- fortios_log_memory_global_setting - Global settings for memory logging in Fortinet's FortiOS and FortiGate.
- fortios_log_memory_setting - Settings for memory buffer in Fortinet's FortiOS and FortiGate.
- fortios_log_null_device_filter - Filters for null device logging in Fortinet's FortiOS and FortiGate.
- fortios_log_null_device_setting - Settings for null device logging in Fortinet's FortiOS and FortiGate.
- fortios_log_setting - Configure general log settings in Fortinet's FortiOS and FortiGate.
- fortios_log_syslogd2_filter - Filters for remote system server in Fortinet's FortiOS and FortiGate.
- fortios_log_syslogd2_setting - Global settings for remote syslog server in Fortinet's FortiOS and FortiGate.
- fortios_log_syslogd3_filter - Filters for remote system server in Fortinet's FortiOS and FortiGate.
- fortios_log_syslogd3_setting - Global settings for remote syslog server in Fortinet's FortiOS and FortiGate.
- fortios_log_syslogd4_filter - Filters for remote system server in Fortinet's FortiOS and FortiGate.
- fortios_log_syslogd4_setting - Global settings for remote syslog server in Fortinet's FortiOS and FortiGate.
- fortios_log_syslogd_filter - Filters for remote system server in Fortinet's FortiOS and FortiGate.
- fortios_log_syslogd_override_filter - Override filters for remote system server in Fortinet's FortiOS and FortiGate.
- fortios_log_syslogd_override_setting - Override settings for remote syslog server in Fortinet's FortiOS and FortiGate.
- fortios_log_syslogd_setting - Global settings for remote syslog server in Fortinet's FortiOS and FortiGate.
- fortios_log_threat_weight - Configure threat weight settings in Fortinet's FortiOS and FortiGate.
- fortios_log_webtrends_filter - Filters for WebTrends in Fortinet's FortiOS and FortiGate.
- fortios_log_webtrends_setting - Settings for WebTrends in Fortinet's FortiOS and FortiGate.
- fortios_report_chart - Report chart widget configuration in Fortinet's FortiOS and FortiGate.
- fortios_report_dataset - Report dataset configuration in Fortinet's FortiOS and FortiGate.
- fortios_report_layout - Report layout configuration in Fortinet's FortiOS and FortiGate.
- fortios_report_setting - Report setting configuration in Fortinet's FortiOS and FortiGate.
- fortios_report_style - Report style configuration in Fortinet's FortiOS and FortiGate.
- fortios_report_theme - Report themes configuratio in Fortinet's FortiOS and FortiGate.
- fortios_router_access_list - Configure access lists in Fortinet's FortiOS and FortiGate.
- fortios_router_auth_path - Configure authentication based routing in Fortinet's FortiOS and FortiGate.
- fortios_router_bfd - Configure BFD in Fortinet's FortiOS and FortiGate.
- fortios_router_bfd6 - Configure IPv6 BFD in Fortinet's FortiOS and FortiGate.
- fortios_router_bgp - Configure BGP in Fortinet's FortiOS and FortiGate.
- fortios_router_multicast - Configure router multicast in Fortinet's FortiOS and FortiGate.
- fortios_router_multicast6 - Configure IPv6 multicast in Fortinet's FortiOS and FortiGate.
- fortios_router_multicast_flow - Configure multicast-flow in Fortinet's FortiOS and FortiGate.
- fortios_router_ospf - Configure OSPF in Fortinet's FortiOS and FortiGate.
- fortios_router_ospf6 - Configure IPv6 OSPF in Fortinet's FortiOS and FortiGate.
- fortios_router_policy - Configure IPv4 routing policies in Fortinet's FortiOS and FortiGate.
- fortios_router_policy6 - Configure IPv6 routing policies in Fortinet's FortiOS and FortiGate.
- fortios_router_prefix_list - Configure IPv4 prefix lists in Fortinet's FortiOS and FortiGate.
- fortios_router_rip - Configure RIP in Fortinet's FortiOS and FortiGate.
- fortios_router_setting - Configure router settings in Fortinet's FortiOS and FortiGate.
- fortios_router_static - Configure IPv4 static routing tables in Fortinet's FortiOS and FortiGate.
- fortios_spamfilter_profile - Configure AntiSpam profiles in Fortinet's FortiOS and FortiGate.
- fortios_ssh_filter_profile - SSH filter profile in Fortinet's FortiOS and FortiGate.
- fortios_switch_controller_global - Configure FortiSwitch global settings in Fortinet's FortiOS and FortiGate.
- fortios_switch_controller_lldp_profile - Configure FortiSwitch LLDP profiles in Fortinet's FortiOS and FortiGate.
- fortios_switch_controller_lldp_settings - Configure FortiSwitch LLDP settings in Fortinet's FortiOS and FortiGate.
- fortios_switch_controller_mac_sync_settings - Configure global MAC synchronization settings in Fortinet's FortiOS and FortiGate.
- fortios_switch_controller_managed_switch - Configure FortiSwitch devices that are managed by this FortiGate in Fortinet's FortiOS and FortiGate.
- fortios_switch_controller_network_monitor_settings - Configure network monitor settings in Fortinet's FortiOS and FortiGate.
- fortios_system_accprofile - Configure access profiles for system administrators in Fortinet's FortiOS and FortiGate.
- fortios_system_admin - Configure admin users in Fortinet's FortiOS and FortiGate.
- fortios_system_api_user - Configure API users in Fortinet's FortiOS and FortiGate.
- fortios_system_central_management - Configure central management.
- fortios_system_dhcp_server - Configure DHCP servers in Fortinet's FortiOS and FortiGate.
- fortios_system_dns - Configure DNS in Fortinet's FortiOS and FortiGate.
- fortios_system_global - Configure global attributes in Fortinet's FortiOS and FortiGate.
- fortios_system_interface - Configure interfaces in Fortinet's FortiOS and FortiGate.
- fortios_system_sdn_connector - Configure connection to SDN Connector.
- fortios_system_settings - Configure VDOM settings in Fortinet's FortiOS and FortiGate.
- fortios_system_vdom - Configure virtual domain in Fortinet's FortiOS and FortiGate.
- fortios_system_virtual_wan_link - Configure redundant internet connections using SD-WAN (formerly virtual WAN link) in Fortinet's FortiOS and FortiGate.
- fortios_user_adgrp - Configure FSSO groups in Fortinet's FortiOS and FortiGate.
- fortios_user_radius - Configure RADIUS server entries in Fortinet's FortiOS and FortiGate.
- fortios_user_tacacsplus - Configure TACACS+ server entries in Fortinet's FortiOS and FortiGate.
- fortios_voip_profile - Configure VoIP profiles in Fortinet's FortiOS and FortiGate.
- fortios_vpn_ipsec_concentrator - Concentrator configuration in Fortinet's FortiOS and FortiGate.
- fortios_vpn_ipsec_forticlient - Configure FortiClient policy realm in Fortinet's FortiOS and FortiGate.
- fortios_vpn_ipsec_manualkey - Configure IPsec manual keys in Fortinet's FortiOS and FortiGate.
- fortios_vpn_ipsec_manualkey_interface - Configure IPsec manual keys in Fortinet's FortiOS and FortiGate.
- fortios_vpn_ipsec_phase1 - Configure VPN remote gateway in Fortinet's FortiOS and FortiGate.
- fortios_vpn_ipsec_phase1_interface - Configure VPN remote gateway in Fortinet's FortiOS and FortiGate.
- fortios_vpn_ipsec_phase2 - Configure VPN autokey tunnel in Fortinet's FortiOS and FortiGate.
- fortios_vpn_ipsec_phase2_interface - Configure VPN autokey tunnel in Fortinet's FortiOS and FortiGate.
- fortios_vpn_ssl_settings - Configure SSL VPN in Fortinet's FortiOS and FortiGate.
- fortios_vpn_ssl_web_portal - Portal in Fortinet's FortiOS and FortiGate.
- fortios_waf_profile - Web application firewall configuration in Fortinet's FortiOS and FortiGate.
- fortios_wanopt_profile - Configure WAN optimization profiles in Fortinet's FortiOS and FortiGate.
- fortios_wanopt_settings - Configure WAN optimization settings in Fortinet's FortiOS and FortiGate.
- fortios_web_proxy_explicit - Configure explicit Web proxy settings in Fortinet's FortiOS and FortiGate.
- fortios_web_proxy_global - Configure Web proxy global settings in Fortinet's FortiOS and FortiGate.
- fortios_web_proxy_profile - Configure web proxy profiles in Fortinet's FortiOS and FortiGate.
- fortios_webfilter_content - Configure Web filter banned word table in Fortinet's FortiOS and FortiGate.
- fortios_webfilter_content_header - Configure content types used by Web filter.
- fortios_webfilter_fortiguard - Configure FortiGuard Web Filter service.
- fortios_webfilter_ftgd_local_cat - Configure FortiGuard Web Filter local categories.
- fortios_webfilter_ftgd_local_rating - Configure local FortiGuard Web Filter local ratings.
- fortios_webfilter_ips_urlfilter_cache_setting - Configure IPS URL filter cache settings.
- fortios_webfilter_ips_urlfilter_setting - Configure IPS URL filter settings.
- fortios_webfilter_ips_urlfilter_setting6 - Configure IPS URL filter settings for IPv6.
- fortios_webfilter_override - Configure FortiGuard Web Filter administrative overrides.
- fortios_webfilter_profile - Configure Web filter profiles.
- fortios_webfilter_search_engine - Configure web filter search engines.
- fortios_webfilter_urlfilter - Configure URL filter lists in Fortinet's FortiOS and FortiGate.
- fortios_wireless_controller_global - Configure wireless controller global settings in Fortinet's FortiOS and FortiGate.
- fortios_wireless_controller_setting - VDOM wireless controller configuration in Fortinet's FortiOS and FortiGate.
- fortios_wireless_controller_utm_profile - Configure UTM (Unified Threat Management) profile in Fortinet's FortiOS and FortiGate.
- fortios_wireless_controller_vap - Configure Virtual Access Points (VAPs) in Fortinet's FortiOS and FortiGate.
- fortios_wireless_controller_wids_profile - Configure wireless intrusion detection system (WIDS) profiles in Fortinet's FortiOS and FortiGate.
- fortios_wireless_controller_wtp - Configure Wireless Termination Points (WTPs), that is, FortiAPs or APs to be managed by FortiGate in Fortinet's FortiOS and FortiGate.
- fortios_wireless_controller_wtp_profile - Configure WTP profiles or FortiAP profiles that define radio settings for manageable FortiAP platforms in Fortinet's FortiOS and FortiGate.

frr
^^^

- frr_bgp - Configure global BGP settings on Free Range Routing(FRR).
- frr_facts - Collect facts from remote devices running Free Range Routing (FRR).

ftd
^^^

- ftd_install - Installs FTD pkg image on the firewall

ingate
^^^^^^

- ig_config - Manage the configuration database on an Ingate SBC.
- ig_unit_information - Get unit information from an Ingate SBC.

ios
^^^

- ios_bgp - Configure global BGP protocol settings on Cisco IOS.
- ios_ntp - Manages core NTP configuration.

iosxr
^^^^^

- iosxr_bgp - Configure global BGP protocol settings on Cisco IOS-XR

itential
^^^^^^^^

- iap_start_workflow - Start a workflow in the Itential Automation Platform
- iap_token - Get token for the Itential Automation Platform

junos
^^^^^

- junos_ping - Tests reachability using ping from devices running Juniper JUNOS

meraki
^^^^^^

- meraki_content_filtering - Edit Meraki MX content filtering policies
- meraki_static_route - Manage static routes in the Meraki cloud
- meraki_syslog - Manage syslog server settings in the Meraki cloud.

netvisor
^^^^^^^^

- pn_access_list - CLI command to create/delete access-list
- pn_access_list_ip - CLI command to add/remove access-list-ip
- pn_admin_service - CLI command to modify admin-service
- pn_admin_session_timeout - CLI command to modify admin-session-timeout
- pn_admin_syslog - CLI command to create/modify/delete admin-syslog
- pn_connection_stats_settings - CLI command to modify connection-stats-settings
- pn_cpu_class - CLI command to create/modify/delete cpu-class
- pn_cpu_mgmt_class - CLI command to modify cpu-mgmt-class
- pn_dhcp_filter - CLI command to create/modify/delete dhcp-filter
- pn_dscp_map - CLI command to create/delete dscp-map
- pn_dscp_map_pri_map - CLI command to modify dscp-map-pri-map
- pn_igmp_snooping - CLI command to modify igmp-snooping
- pn_port_config - CLI command to modify port-config
- pn_port_cos_bw - CLI command to modify port-cos-bw
- pn_port_cos_rate_setting - CLI command to modify port-cos-rate-setting
- pn_prefix_list_network - CLI command to add/remove prefix-list-network
- pn_role - CLI command to create/delete/modify role
- pn_snmp_community - CLI command to create/modify/delete snmp-community
- pn_snmp_trap_sink - CLI command to create/delete snmp-trap-sink
- pn_snmp_vacm - CLI command to create/modify/delete snmp-vacm
- pn_stp - CLI command to modify stp
- pn_stp_port - CLI command to modify stp-port.
- pn_switch_setup - CLI command to modify switch-setup
- pn_user - CLI command to create/modify/delete user
- pn_vflow_table_profile - CLI command to modify vflow-table-profile
- pn_vrouter_bgp_network - CLI command to add/remove vrouter-bgp-network
- pn_vrouter_interface_ip - CLI command to add/remove vrouter-interface-ip
- pn_vrouter_ospf6 - CLI command to add/remove vrouter-ospf6
- pn_vrouter_pim_config - CLI command to modify vrouter-pim-config

onyx
^^^^

- onyx_buffer_pool - Configures Buffer Pool
- onyx_igmp_interface - Configures IGMP interface parameters
- onyx_igmp_vlan - Configures IGMP Vlan parameters
- onyx_ptp_global - Configures PTP Global parameters
- onyx_ptp_interface - Configures PTP on interface
- onyx_vxlan - Configures Vxlan

restconf
^^^^^^^^

- restconf_config - Handles create, update, read and delete of configuration data on RESTCONF enabled devices.
- restconf_get - Fetch configuration/state data from RESTCONF enabled devices.

routeros
^^^^^^^^

- routeros_facts - Collect facts from remote devices running MikroTik RouterOS

skydive
^^^^^^^

- skydive_capture - Module which manages flow capture on interfaces
- skydive_edge - Module to add edges to Skydive topology
- skydive_node - Module which add nodes to Skydive topology

voss
^^^^

- voss_config - Manage Extreme VOSS configuration sections

vyos
^^^^

- vyos_ping - Tests reachability using ping from VyOS network devices

Notification
~~~~~~~~~~~~

- matrix - Send notifications to matrix
- rabbitmq_publish - Publish a message to a RabbitMQ queue.

Packaging
~~~~~~~~~

language
^^^^^^^^

- pip_package_info - pip package information

os
^^

- apt_repo - Manage APT repositories via apt-repo
- installp - Manage packages on AIX
- rhsm_release - Set or Unset RHSM Release version
- snap - Manages snaps

Remote Management
~~~~~~~~~~~~~~~~~

cpm
^^^

- cpm_plugconfig - Get and Set Plug Parameters on WTI OOB and PDU power devices
- cpm_plugcontrol - Get and Set Plug actions on WTI OOB and PDU power devices

dellemc
^^^^^^^

- idrac_firmware - Firmware update from a repository on a network share (CIFS, NFS).
- idrac_server_config_profile - Export or Import iDRAC Server Configuration Profile (SCP).

intersight
^^^^^^^^^^

- intersight_facts - Gather facts about Intersight
- intersight_rest_api - REST API configuration for Cisco Intersight

lxca
^^^^

- lxca_cmms - Custom module for lxca cmms inventory utility
- lxca_nodes - Custom module for lxca nodes inventory utility

manageiq
^^^^^^^^

- manageiq_group - Management of groups in ManageIQ.
- manageiq_tenant - Management of tenants in ManageIQ.

redfish
^^^^^^^

- idrac_redfish_command - Manages Out-Of-Band controllers using iDRAC OEM Redfish APIs
- idrac_redfish_config - Manages servers through iDRAC using Dell Redfish APIs
- idrac_redfish_facts - Manages servers through iDRAC using Dell Redfish APIs

ucs
^^^

- ucs_disk_group_policy - Configures disk group policies on Cisco UCS Manager
- ucs_dns_server - Configure DNS servers on Cisco UCS Manager
- ucs_managed_objects - Configures Managed Objects on Cisco UCS Manager
- ucs_org - Manages UCS Organizations for UCS Manager
- ucs_service_profile_template - Configures Service Profile Templates on Cisco UCS Manager

Source Control
~~~~~~~~~~~~~~

- github_webhook - Manage GitHub webhooks
- github_webhook_facts - Query information about GitHub webhooks
- gitlab_runner - Create, modify and delete GitLab Runners.

bitbucket
^^^^^^^^^

- bitbucket_access_key - Manages Bitbucket repository access keys
- bitbucket_pipeline_key_pair - Manages Bitbucket pipeline SSH key pair
- bitbucket_pipeline_known_host - Manages Bitbucket pipeline known hosts
- bitbucket_pipeline_variable - Manages Bitbucket pipeline variables

Storage
~~~~~~~

glusterfs
^^^^^^^^^

- gluster_heal_facts - Gather facts about self-heal or rebalance status

hpe3par
^^^^^^^

- ss_3par_cpg - Manage HPE StoreServ 3PAR CPG

ibm
^^^

- ibm_sa_domain - Manages domains on IBM Spectrum Accelerate Family storage systems
- ibm_sa_host_ports - Add host ports on IBM Spectrum Accelerate Family storage systems.
- ibm_sa_vol_map - Handles volume mapping on IBM Spectrum Accelerate Family storage systems.

netapp
^^^^^^

- na_elementsw_cluster_config - Configure Element SW Cluster
- na_elementsw_cluster_snmp - Configure Element SW Cluster SNMP
- na_elementsw_initiators - Manage Element SW initiators
- na_ontap_flexcache - NetApp ONTAP FlexCache - create/delete relationship
- na_ontap_igroup_initiator - NetApp ONTAP igroup initiator configuration
- na_ontap_lun_copy - NetApp ONTAP copy LUNs
- na_ontap_net_subnet - NetApp ONTAP Create, delete, modify network subnets.
- na_ontap_nvme - NetApp ONTAP Manage NVMe Service
- na_ontap_nvme_namespace - NetApp ONTAP Manage NVME Namespace
- na_ontap_nvme_subsystem - NetApp ONTAP Manage NVME Subsystem
- na_ontap_portset - NetApp ONTAP Create/Delete portset
- na_ontap_qos_policy_group - NetApp ONTAP manage policy group in Quality of Service.
- na_ontap_quotas - NetApp ONTAP Quotas
- na_ontap_security_key_manager - NetApp ONTAP security key manager.
- na_ontap_snapshot_policy - NetApp ONTAP manage Snapshot Policy
- na_ontap_unix_group - NetApp ONTAP UNIX Group
- na_ontap_unix_user - NetApp ONTAP UNIX users
- na_ontap_vscan_on_access_policy - NetApp ONTAP Vscan on access policy configuration.
- na_ontap_vscan_on_demand_task - NetApp ONTAP Vscan on demand task configuration.
- na_ontap_vscan_scanner_pool - NetApp ONTAP Vscan Scanner Pools Configuration.

purestorage
^^^^^^^^^^^

- purefa_dns - Configure FlashArray DNS settings
- purefa_dsrole - Configure FlashArray Directory Service Roles
- purefa_ntp - Configure Pure Storage FlashArray NTP settings
- purefa_offload - Create, modify and delete NFS or S3 offload targets
- purefa_ra - Enable or Disable Pure Storage FlashArray Remote Assist
- purefa_user - Create, modify or delete FlashArray local user account
- purefb_bucket - Manage Object Store Buckets on a  Pure Storage FlashBlade.
- purefb_ds - Configure FlashBlade Directory Service
- purefb_dsrole - Configure FlashBlade  Management Directory Service Roles
- purefb_network - Manage network interfaces in a Pure Storage FlashBlade
- purefb_s3acc - Create or delete FlashBlade Object Store accounts
- purefb_s3user - Create or delete FlashBlade Object Store account users
- purefb_subnet - Manage network subnets in a Pure Storage FlashBlade

vexata
^^^^^^

- vexata_volume - Manage volumes on Vexata VX100 storage arrays

zfs
^^^

- zfs_delegate_admin - Manage ZFS delegated administration (user admin privileges)

System
~~~~~~

- aix_devices - Manages AIX devices
- aix_filesystem - Configure LVM and NFS file systems for AIX
- aix_lvg - Manage LVM volume groups on AIX
- gather_facts - Gathers facts about remote hosts
- pids - Retrieves process IDs list if the process is running otherwise return empty list
- selogin - Manages linux user to SELinux user mapping
- xfconf - Edit XFCE4 Configurations
- xfs_quota - Manage quotas on XFS filesystems

Web Infrastructure
~~~~~~~~~~~~~~~~~~

ansible_tower
^^^^^^^^^^^^^

- tower_notification - create, update, or destroy Ansible Tower notification.
- tower_receive - Receive assets from Ansible Tower.
- tower_send - Send assets to Ansible Tower.
- tower_workflow_launch - Run a workflow in Ansible Tower

sophos_utm
^^^^^^^^^^

- utm_aaa_group - Create, update or destroy an aaa group object in Sophos UTM.
- utm_aaa_group_info - get info for reverse_proxy frontend entry in Sophos UTM
- utm_ca_host_key_cert - create, update or destroy ca host_key_cert entry in Sophos UTM
- utm_ca_host_key_cert_info - Get info for a ca host_key_cert entry in Sophos UTM
- utm_dns_host - create, update or destroy dns entry in Sophos UTM
- utm_network_interface_address - Create, update or destroy network/interface_address object
- utm_network_interface_address_info - Get info for a network/interface_address object
- utm_proxy_auth_profile - create, update or destroy reverse_proxy auth_profile entry in Sophos UTM
- utm_proxy_exception - Create, update or destroy reverse_proxy exception entry in Sophos UTM
- utm_proxy_frontend - create, update or destroy reverse_proxy frontend entry in Sophos UTM
- utm_proxy_frontend_info - create, update or destroy reverse_proxy frontend entry in Sophos UTM
- utm_proxy_location - create, update or destroy reverse_proxy location entry in Sophos UTM
- utm_proxy_location_info - create, update or destroy reverse_proxy location entry in Sophos UTM

Windows
~~~~~~~

- win_chocolatey_facts - Create a facts collection for Chocolatey
- win_credential - Manages Windows Credentials in the Credential Manager
- win_dns_record - Manage Windows Server DNS records
- win_domain_group_membership - Manage Windows domain group membership
- win_format - Formats an existing volume or a new volume on an existing partition on Windows
- win_hosts - Manages hosts file entries on Windows.
- win_http_proxy - Manages proxy settings for WinHTTP
- win_inet_proxy - Manages proxy settings for WinINet and Internet Explorer
- win_optional_feature - Manage optional Windows features
- win_partition - Creates, changes and removes partitions on Windows Server
- win_psrepository - Adds, removes or updates a Windows PowerShell repository.
- win_rds_cap - Manage Connection Authorization Policies (CAP) on a Remote Desktop Gateway server
- win_rds_rap - Manage Resource Authorization Policies (RAP) on a Remote Desktop Gateway server
- win_rds_settings - Manage main settings of a Remote Desktop Gateway server
- win_snmp - Configures the Windows SNMP service
- win_user_profile - Manages the Windows user profiles.

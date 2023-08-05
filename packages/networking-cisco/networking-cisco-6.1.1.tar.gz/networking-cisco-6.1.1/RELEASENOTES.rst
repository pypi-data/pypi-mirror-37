================
networking-cisco
================

.. _networking-cisco_6.1.1:

6.1.1
=====

.. _networking-cisco_6.1.1_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/subnet_id_fk_const-f28230dc9aa4d32a.yaml @ 68a5b4b5af4f08a4ffddce0cdaf42d538a3c738f

- Fixes a bug in the networking-cisco migrations when run against MariaDB
  which prevent the `subnet_id` field being added as a primary key due to it
  previously being added as a foreign key.
  See: https://bugs.launchpad.net/networking-cisco/+bug/1791121


.. _networking-cisco_6.1.0:

6.1.0
=====

.. _networking-cisco_6.1.0_New Features:

New Features
------------

.. releasenotes/notes/support_for_queens-6c2b67b426b6d5de.yaml @ d3dfe4f0591d7763ff514a03144932b6c50ecc1d

- Adds support for the OpenStack Neutron queens release.


.. _networking-cisco_6.1.0_Deprecation Notes:

Deprecation Notes
-----------------

.. releasenotes/notes/host-mapping-cfg-new-method-17063db7feb4ba97.yaml @ 10d5418d81c3b1391ec70e8a1f95c98b9fdd4501

- Nexus: Host Mapping Configuration being replaced
  
  The host mapping configuration beneath the header `ml2_mech_cisco_nexus`
  currently does not have a static config option name.  This can lead to
  some issues where even typographical errors can be interpreted as a host
  mapping config.  The config option `host_ports_mapping` has been introduced
  to resolve this shortcoming.  The following demonstrates the before and
  after config change.
  
  ``Before:`` `hostname_abc=ethernet:1/19`,
  ``After:`` `host_ports_mapping=hostname_abc:[ethernet:1/19]`


.. _networking-cisco_6.1.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/port-not-found-exception-3d2f47dc1298855c.yaml @ 21faaf82723be98f2ad3d252e0eebaf36257d990

- Nexus: Do not raise exception during update_postcommit when port not found
  
  Occasionally spurious updates are seen in parallel with deletes for same
  vlan.  In this window an update can be received after the port binding
  is removed.  This change reports a warning message instead of raising
  an exception keeping it consistent with other ML2 driver behavior.  This
  circumstance will more likely be seen when there are multiple neutron
  threads and controllers.

.. releasenotes/notes/trunk-no-support-in-newton-fix-dbf02e6d10e22361.yaml @ 3e65e80212d41923fdaa874633abc09158fada03

- Nexus: Neutron trunking feature not supported in Newton
  
  Introduced a fix to prevent an error from being generated
  when using openstack newton or below branches with
  baremetal configurations.  The error message seen
  is "TypeError: get_object() got an unexpected keyword"
  "argument 'port_id'".  For implementation details,
  refer to https://review.openstack.org/#/c/542877.


.. _networking-cisco_6.0.0:

6.0.0
=====

.. _networking-cisco_6.0.0_Upgrade Notes:

Upgrade Notes
-------------

.. releasenotes/notes/change-to-ucsmsdk-5e57c6b0e80ba334.yaml @ 276b08f25e40e43fc6d83b7022bddb25a9bdbcc7

- Cisco UCSM: The ucsmsdk is now the default replacing the UcsSdk
  
  The ucsmsdk is now the default package for interacting with UCSM.
  Use of the now deprecated UcsSdk will still work if the ucsmsdk is not
  installed. However, all new features will be developed using the ucsmsdk
  so users are encouraged to upgrade.

.. releasenotes/notes/remove-csr1kv-routing-code-5f436f831c468b3a.yaml @ 4e7a7d3710e3d1c3b7f7e062eee3c2addc4dc4c8

- All code for CSR1kv-based routing has been removed from networking-cisco.
  The code was removed in commit 917480566afa2b40dc382bc4f535d173bad7736d.

.. releasenotes/notes/remove-n1kv-driver-code-428635c33a58a365.yaml @ 4716a637713b11160b63acaa1989eeaf27459a68

- All Nexus 1000v driver code has been removed from networking-cisco,
  and all n1kv related tables have been dropped. The code was removed
  in commit 0730ec9e6b76b3c1e75082e9dd1af55c9faeb34c

.. releasenotes/notes/remove_ncs-85a89eac7d93bb18.yaml @ 93b162df0404571995fd549e6959276bfb542292

- NCS: Remove support for Network Control System (NCS).
  The code was removed in commit 31e4880299d04ceb399aa38097fc5f2b26e30ab1


.. _networking-cisco_6.0.0_Deprecation Notes:

Deprecation Notes
-----------------

.. releasenotes/notes/change-to-ucsmsdk-5e57c6b0e80ba334.yaml @ 276b08f25e40e43fc6d83b7022bddb25a9bdbcc7

- Cisco UCSM: Use of the UcsSdk has been deprecated for removal
  
  Use of of the UcsSdk will be removed in a future release. It has been
  replaced by the ucsmsdk. While use of the UcsSdk will continue to work
  until its complete removal, no new features will be added so users are
  encouraged to upgrade.


.. _networking-cisco_5.5.2:

5.5.2
=====

.. _networking-cisco_5.5.2_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/Mapping-DbDuplicateEntry-multictrl-b531dde46b9c214c.yaml @ 0ccd0f0af6d60640f6fa6e9c1262fe5f3947a673

- Nexus: DBDuplicateEntry error from interface mapping db table with multi-controllers
  
  When there are multiple controllers running, they could simultaneously attempt to
  initialize the Nexus host interface mapping db table using the user's static host
  mapping configuration. This could result in a `DBDuplicateEntry` exception.  This
  type of error is seen with static user configured hosts but not ironic learned
  hosts.  Refer to :ref:`dupl_entry` for error message details and corrective action.
  For implementation details, refer to
  https://bugs.launchpad.net/networking-cisco/+bug/1743573.


.. _networking-cisco_5.5.0:

5.5.0
=====

.. _networking-cisco_5.5.0_New Features:

New Features
------------

.. releasenotes/notes/single-ucsm-vnic-sp-templates-c282733a496321fe.yaml @ 0c46030a5699b04418f84514d2ff15f5c7c1f6f9

- Cisco UCSM: vNIC and Service Profile Template support for Single UCSM
  
  This feature allows a cloud admin to take advantage of the Service
  Profile Template and vNIC Template configuration options available
  on the UCS Manager. The UCSM driver can be provided with the Service
  Profile or the Service Profile Template configuration, and it will
  handle the configuration of the UCS Servers accordingly. The vNIC
  Templates can be used to configure several vNIC on different UCS
  Servers, all connected to the same physical network. The driver
  will handle configuration of the appropriate vNIC Template with
  the VLAN configuration associated with the corresponding neutron
  provider network.


.. _networking-cisco_5.4.0:

5.4.0
=====

.. _networking-cisco_5.4.0_Security Issues:

Security Issues
---------------

.. releasenotes/notes/nexus-restapi-improvements-6a0f6771284a3610.yaml @ cd210d2711fb2435840526da124572c9efd16d01

- Nexus: https certification now supported by RESTAPI Client
  
  The Nexus RESTAPI Client now sends requests using https instead of http
  which results in communication with the Nexus to be encrypted.
  Certificate verification can also be performed.  A new configuration
  option 'https_verify' controls this latter capability.  When set to
  False, the communication path is insecure making it vulnerable to
  man-in-the-middle attacks.  Initially, the default for 'https_verify'
  is set to False but will change to True in the 'Cisco 6.0.0' release.
  If a certificate is already available and configured on the Nexus device,
  it is highly recommended to set this options to True in the
  neutron start-up configuration file.
  
  For testing or lab purposes, a temporary local certificate
  can be generated and the certificate filename can be provided
  in the configuration option 'https_local_certificate'. This depends
  on the Nexus device being configured with the local key and certificate
  file.
  
  Both configuration options are available for every Nexus switch
  configured.  Refer to the
  :doc:`Nexus Configuration Reference </configuration/ml2-nexus>`
  for more details on these options as well as
  https://bugs.launchpad.net/networking-cisco/+bug/1735295

.. releasenotes/notes/obfuscate-password-24c308c1efc68342.yaml @ 2f603f6afc4cfd5d0980447eec98153fa8a78540

- Nexus: Obfuscate password
  
  In log output, obfuscate Nexus Switch password provided in Neutron Start-up configuration.

.. releasenotes/notes/ucsm-https-verify-ebfe8d1921d52035.yaml @ a886819483f061f744d0d5d4d662fe3260417a41

- Cisco UCSM: Add config to control SSL certificate checks
  
  This feature allows a cloud admin to disable SSL certificate
  checking when the UCSM driver connects to the UCS Managers
  provided in its configuration. SSL certificate checking is
  ON by default and setting the ``ucsm_https_verify``
  configuration parameter to ``False`` turns it OFF. Turning it
  OFF makes the connection insecure and vulnerable to
  man-in-the-middle attacks.


.. _networking-cisco_5.4.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/Mapping-DBDuplicateEntry-fix-992db50b17ecbe21.yaml @ 334e1a794546f8f2b0bcce0491f476f659f712a6

- Nexus: DBDuplicateEntry error seen with Nexus interface mapping database
  
  Introduced a fix to resolve the issue when the same port-channel is
  configured for multiple hosts beneath the same switch, a `DBDuplicateEntry`
  error is seen.  This type of configuration is seen with static
  configurations only and not ironic.  Refer to :ref:`dupl_entry` for sample
  config, more error message details, and corrective action.  For implementation
  details, refer to https://bugs.launchpad.net/networking-cisco/+bug/1735540.

.. releasenotes/notes/replace-dot-in-cfg-var-for-tripleo-5f0b1954567df3ac.yaml @ db9b1c7ed89f46ee09d777d4a9f7d44dece3e007

- Nexus: Remove '.' from configuration variable names
  
  When testing new configuration variables with puppet and tripleo,
  the use of dot '.' in configuration variable name fails.
  There is only one such variable which is `intfcfg.portchannel`. It
  is replaced with `intfcfg_portchannel`.


.. _networking-cisco_5.4.0_Other Notes:

Other Notes
-----------

.. releasenotes/notes/nexus-restapi-improvements-6a0f6771284a3610.yaml @ cd210d2711fb2435840526da124572c9efd16d01

- Nexus: RESTAPI Client Scaling Improvement
  
  To improve performance, the same cookie will be used in requests until
  it expires and the Nexus device returns a status_code of 403.  When
  this is detected, an attempt to refresh the cookie occurs and upon
  successful receipt of a new cookie the request that originally failed
  will be resent.
  For more details, refer to
  https://bugs.launchpad.net/networking-cisco/+bug/1735295


.. _networking-cisco_5.3.0:

5.3.0
=====

.. _networking-cisco_5.3.0_New Features:

New Features
------------

.. releasenotes/notes/nexus_followup_relnotes-4a91cc7e4f8c7377.yaml @ 0e1b1a02e9c6f83b0e85c72ad03ed222f27977a4

- Nexus: Improved port-channel support with baremetal events
  
  When there are multiple ethernet interfaces in the baremetal's
  neutron port event, the Nexus driver determines whether the
  interfaces are already configured as members of a port-channel.
  If not, it creates a new port-channel interface and adds the
  ethernet interfaces as members. In either case, trunk vlans are
  applied to the port-channel.  For this to be successful,
  a new configuration variable 'vpc_pool' must be defined with
  a pool of vpc ids for each switch.  This must be defined beneath
  the section header [ml2_mech_cisco_nexus:<switch-ip-address>].
  A vpc id common between participating switches will be selected.
  To get more details on defining this variable, refer to
  networking-cisco repo, file:
  etc/neutron/plugins/ml2/ml2_conf_cisco.ini
  For implementation details on automated port-channel creation,
  refer to
  https://bugs.launchpad.net/networking-cisco/+bug/1707286 and
  https://bugs.launchpad.net/networking-cisco/+bug/1691822 and
  https://bugs.launchpad.net/networking-cisco/+bug/1705294

.. releasenotes/notes/nexus_followup_relnotes-4a91cc7e4f8c7377.yaml @ 0e1b1a02e9c6f83b0e85c72ad03ed222f27977a4

- Nexus: User customizable port-channels for baremetal interfaces
  
  When the Nexus driver creates port-channels for baremetal events,
  an additional capability was provided to allow the user to custom
  configure port-channels that are created.  This is done by way
  of the config variable 'intfcfg.portchannel'  beneath each switch's
  section header [ml2_mech_cisco_nexus:<switch-ip-address>].
  Nexus CLI commands are defined in this variable unique for each
  switch and sent while creating the port-channel. For details, refer to
  https://bugs.launchpad.net/networking-cisco/+bug/1706965

.. releasenotes/notes/nexus_trunk_support-cd12b7e7e59911a5.yaml @ be811d104ad2e826f7d8a6e6cc9cf7cfb4f7cc15

- Nexus: Neutron Trunk Support
  
  The Nexus mechanism driver support of the neutron trunk feature
  (https://docs.openstack.org/ocata/networking-guide/config-trunking.html)
  is to create and trunk on the Nexus switch the trunk subport's network
  VLAN(s) configured under the neutron trunk parent port.

.. releasenotes/notes/provider_network-b564489765be1a9a.yaml @ 1d3e17fc3e12a1897bf3eb0aa248771e86ffa9b6

- Nexus: Provider Network Limited Operations
  
  The Openstack administrator may want to control how the neutron port
  events program the Nexus switch for provider networks. Two configuration
  variables have been introduced to suppress vlan creation and the vlan trunk
  port setting on the Nexus switch for provider networks. These variables,
  'provider_vlan_auto_create' and 'provider_vlan_auto_trunk', are defined under
  the [ml2_cisco] section header.

.. releasenotes/notes/ucsm_auto_detection_of_compute_hosts-28b26f712f2b9b3b.yaml @ a886819483f061f744d0d5d4d662fe3260417a41

- Cisco UCSM: Auto detection of Compute hosts
  
  This feature allows a cloud admin to expand the size of the Openstack
  cloud dynamically by adding more compute hosts to an existing UCS
  Manager. The cloud admin can now add the hostname of this new compute
  host to the "Name" field of its Service Profile on the UCSM. Then when
  a VM is scheduled on this compute host, the Cisco UCSM ML2 mechanism
  driver goes through all the Service Profiles of all the UCSMs known to
  it to figure out the UCSM and the Service Profile associated with that
  host. After learning the UCSM and Service Profile, the mechanism driver
  saves this information for future operations. Note that this method
  cannot be used to add more Controller nodes to the cloud.


.. _networking-cisco_5.3.0_Upgrade Notes:

Upgrade Notes
-------------

.. releasenotes/notes/add-host-interface-map-table-6d8a5c1715ac035c.yaml @ 0e1b1a02e9c6f83b0e85c72ad03ed222f27977a4

- Nexus: Add host to switch/interface mapping database table
  
  A new database table for host to interface mapping is added
  for baremetal deployments.  The administrator must perform a
  database migration to incorporate this upgrade.  The new database
  table name is 'cisco_ml2_nexus_host_interface_mapping'.
  For more details, refer to
  https://bugs.launchpad.net/networking-cisco/+bug/1691194

.. releasenotes/notes/deprecate-ncclient-driver-81db436a78249397.yaml @ 0e1b1a02e9c6f83b0e85c72ad03ed222f27977a4

- Nexus: Set RESTAPI driver as default replacing ncclient driver
  
  The Nexus 9K handles the RESTAPI events more efficiently and without
  session limitations.  It is now the default and will be the only
  choice in 'Cisco 7.0.0' release.  This may require the administrator
  to upgrade the Nexus operating system.  If necessary, use
  'nexus_driver=ncclient' to temporarily go back to original default
  driver; however, some enhancements may not be available when using
  this driver. For details, refer to
  https://bugs.launchpad.net/networking-cisco/+bug/1705036

.. releasenotes/notes/dflt_replay_enabled-c7a60499266bd795.yaml @ 0e1b1a02e9c6f83b0e85c72ad03ed222f27977a4

- Nexus: Set default for Configuration Replay to enabled
  
  Configuration replay is now enabled by default by setting the variable
  'switch_heartbeat_time' to 30 seconds (defined under the [ml2_cisco]
  section header).  If the administrator does not want this feature enabled,
  set this variable to 0. When enabled, the nexus driver checks each switch
  for connectivity and will restore the configuration known to the driver
  if a switch recovers from failure.  For details, refer to
  https://bugs.launchpad.net/networking-cisco/+bug/1712090

.. releasenotes/notes/nexus_followup_relnotes-4a91cc7e4f8c7377.yaml @ 0e1b1a02e9c6f83b0e85c72ad03ed222f27977a4

- Nexus: New vpc id allocation database table
  
  To implement the vpc id pool for automated port-channel creation with
  baremetal deployments, a new database table was created so a
  database migration is needed to incorporate the new vpc id table.
  The new database table name is 'cisco_ml2_nexus_vpc_alloc'. For more details,
  refer to
  https://bugs.launchpad.net/networking-cisco/+bug/1707286 and
  https://bugs.launchpad.net/networking-cisco/+bug/1691822 and
  https://bugs.launchpad.net/networking-cisco/+bug/1705294


.. _networking-cisco_5.3.0_Deprecation Notes:

Deprecation Notes
-----------------

.. releasenotes/notes/deprecate-ncclient-driver-81db436a78249397.yaml @ 0e1b1a02e9c6f83b0e85c72ad03ed222f27977a4

- Nexus: The ncclient/ssh config driver has been deprecated for removal
  
  Use of ncclient/ssh_driver will be removed in the 'Cisco 7.0.0'
  release.  It will be replaced by the RESTAPI Driver.  Some
  configuration options are also deprecated for removal
  since they relate only to the ncclient driver.  These include
  'persistent_switch_config', 'never_cache_ssh_connection',
  'host_key_checks', and 'nexus_driver'. For details, refer to
  https://bugs.launchpad.net/networking-cisco/+bug/1705036


.. _networking-cisco_5.3.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/elim_MultiConfigParser_fr_nexus-6a50c543949d1ca4.yaml @ c982b6ceef4a842a1644b6a4a263b5fa76960956

- Nexus:  Eliminate warning message for 'MultiConfigParser' from Nexus ML2 Plugin
  
  The 'MultiConfigParser' class is deprecated as seen by warnings in the neutron
  log file.  Refer to https://bugs.launchpad.net/networking-cisco/+bug/1712853
  for details.

.. releasenotes/notes/greenpool_traceback-7ceb08e183bac3cf.yaml @ ecf048397700d45e7d11b3c031bb8dedaa635f22

- ASR1k: Fix greenpool.py traceback in Ocata
  
  The ASR1k plugin was wrapping neutron and plugin DB operations
  in common transactions that was generating a lot of strange
  tracebacks in the neutron server logs. This commit removes
  the transaction wrapper to make the operations more independent
  of each other, eliminating the tracebacks entirely.

.. releasenotes/notes/replace-get-session-in-nexus-9ccd3c0c8d15d997.yaml @ 0e1b1a02e9c6f83b0e85c72ad03ed222f27977a4

- Nexus:  Eliminate warning message for 'neutron.db.api.get_session'
  
  The 'neutron.db.api.get_session' API is deprecated as seen by warnings in
  the neutron log file so it is replaced.  For details, refer to
  https://bugs.launchpad.net/networking-cisco/+bug/1713498


.. _networking-cisco_5.3.0_Other Notes:

Other Notes
-----------

.. releasenotes/notes/remove-unused-config-4501b85d6043e674.yaml @ 0e1b1a02e9c6f83b0e85c72ad03ed222f27977a4

- Nexus: Remove unused configuration variables
  
  The configuration variables 'svi_round_robin',
  'provider_vlan_name_prefix', and 'vlan_name_prefix'
  are no longer used by the nexus driver and can be removed.
  For further details, refer to
  https://bugs.launchpad.net/networking-cisco/+bug/1712118


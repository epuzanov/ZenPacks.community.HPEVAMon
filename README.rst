===========================
ZenPacks.community.HPEVAMon
===========================

About
=====

This project is `Zenoss <http://www.zenoss.com/>`_ extension (ZenPack) that
makes it possible to model and monitor HP EVA 4X00/6X00/8X00 devices. It
creates a **/Devices/Storage/SMI-S/HP/EVA** Device Class for monitoring these
storage devices.


Requirements
============

Zenoss
------

You must first have, or install, Zenoss 2.5.2 or later. This ZenPack was tested
against Zenoss 2.5.2 and Zenoss 3.2. You can download the free Core version of
Zenoss from http://community.zenoss.org/community/download

ZenPacks
--------

You must first install
`CIMMon ZenPack <http://community.zenoss.org/docs/DOC-5913>`_.

Installation
============

Upgrade
-------

#. delete existing HP EVA Devices from your Zenoss inventory.
#. uninstall old HPEVAMon ZenPack 
#. delete /CIM/HPEVA device class
#. install latest HPEVAMon ZenPack

Normal Installation (packaged egg)
----------------------------------

Download the `HPEVAMon ZenPack <http://community.zenoss.org/docs/DOC-5867>`_.
Copy this file to your Zenoss server and run the following commands as the
**zenoss** user.

    ::

        zenpack --install ZenPacks.community.HPEVAMon-2.0.egg
        zenoss restart

Developer Installation (link mode)
----------------------------------

If you wish to further develop and possibly contribute back to the HPEVAMon
ZenPack you should clone the git
`repository <https://github.com/epuzanov/ZenPacks.community.HPEVAMon>`_, then
install the ZenPack in developer mode using the following commands.

    ::

        git clone git://github.com/epuzanov/ZenPacks.community.HPEVAMon.git
        zenpack --link --install ZenPacks.community.HPEVAMon
        zenoss restart


Usage
=====

#. You should now have /Storage/SMI-S/HP/EVA device class.
#. Click on the HPEVA class and select Details.
#. Click Configuration Properties on the left.
#. In the right pane, in both **zCIMConnectionString** and
   **zCIMHWConnectionString** fields replace **${here/manageIp}** text with 
   the IP address or hostname of the EVA Command View server. The reason for
   this is that you'ere going to use the EVA server as a boker to grab data
   regarding the EVAs themselves, hence you request data about an EVA using it's
   WWN and that request is fired at the Command View IP/Hostname.
#. In the **zWinPassword** and **zWinUser** add the correct credentials of a
   user account that can access the server.  (possibly create a new user account
   in AD and add this account to the CV server)
#. Hit Save.
#. Click on See All at the top of the left pane.
#. Still in the **EVA** class click on the icon at the top of the main pane to
   add a new single device. Use Command View get the WWN (without dashes) of
   your EVA and paste into the Hostname or IP field and click Add.
#. Give Zenoss a chance to perform the Add Job, when I first added our EVA the
   Job service was down and needed starting.
#. Once the device has been added, go into it and from the icon on the bottom
   left select Model Device. At this point I had issues with Zenoss connecting
   to Zenhub and got timeout errors. It eventually reconnected and carried on
   sometimes it didn't, just restart the modelling if it fails but give it a
   chance to retry.
#. Once the modelling has completed you should then see a load of objects in
   the Components menu in the left pane as well as a new hardware tab where the
   graphical disk view can be found.

Graphing should start almost immediately, you may need to soom in to see it
starting. I may have seen an issue involving the renaming of the device from
the WWN where graphing stops after the rename...well that's what appears to
have happened....so rename at your peril!

The following elements are discovered:

- Storage Controllers (Status and Performance)
- Storage Enclosures (Status Only)
- Physical Disks (Status and Performance)
- Storage Groups (Status and Performance)
- Data Replication Groups  (Status and Performance)
- Virtual Disks (Status and Performance)
- Host FC Ports (Status and Performance)
- Disk FC Ports (Status Only)

Modeler Plugins
---------------

- **community.cim.HPEVAComputerSystemMap** - ComputerSystem modeler plugin, tried
  to identify snmpSysName, snmpDescr, snmpContact, Model, Vendor and Serial
  Number information for storage device
- **community.cim.HPEVAConsistencySetMap** - Collection modeler plugin, tried to
  identify Replication groups
- **community.cim.HPEVADiskDriveMap** - Hard Disks modeler plugin
- **community.cim.HPEVANetworkPortMap** - FC Ports modeler plugin
- **community.cim.HPEVAOperatingSystemMap** - Operating System modeler plugin,
  tried identify OS Version and OS Vendor
- **community.cim.HPEVARedundancySetMap** - Redundancy Set modeler plugin, tried
  identify Redundancy sets
- **community.cim.HPEVAStorageDiskEnclosureMap** - Disk Enclosures modeler
  plugin, tried to identify Model, Vendor and Layout of Disk Enclosures
- **community.cim.HPEVAStorageProcessorCardMap** - Controller modeler plugin, tried to
  identify storage controllers
- **community.cim.HPEVAStoragePoolMap** - Storage Pool (Disk Group) modeler
  plugin, tried to identify storage pools configured on storage
- **community.cim.HPEVAStorageVolumeMap** - Storage Volume modeler plugin, tried
  to identify Logical Disks configured on Storage

Device Classes
--------------

- Devices/Storage/SMI-S/HP/EVA

Monitoring Templates
--------------------

- Devices/Storage/SMI-S/HP/EVA/Device
- Devices/Storage/SMI-S/HP/EVA/HPEVA_ConsistencySet
- Devices/Storage/SMI-S/HP/EVA/HPEVA_DiskDriveStatisticalData
- Devices/Storage/SMI-S/HP/EVA/HPEVA_HostFCPortStatisticalData
- Devices/Storage/SMI-S/HP/EVA/HPEVA_StoragePool
- Devices/Storage/SMI-S/HP/EVA/HPEVA_StorageSystemControllerStatisticalData
- Devices/Storage/SMI-S/HP/EVA/HPEVA_VolumeStatisticalData

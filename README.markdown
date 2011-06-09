# ZenPacks.community.HPEVAMon

## About
This project is [Zenoss][] extension (ZenPack) that makes it possible to
model and monitor HP EVA 4X00/6X00/8X00 devices. It creates a
__/Devices/CIM/HPEVA__ Device Class for monitoring these storage devices.

## Requirements

### Zenoss
You must first have, or install, Zenoss 2.5.2 or later. This ZenPack was
tested against Zenoss 2.5.2 and Zenoss 3.1.0. You can download
the free Core version of Zenoss from
<http://community.zenoss.org/community/download>.

### ZenPacks
You must first install [WBEMDataSource ZenPack][].

## Installation

### Normal Installation (packaged egg)
Download the [HPEVAMon ZenPack][]. Copy this file to your Zenoss
server and run the following commands as the zenoss user.

    zenpack --install ZenPacks.community.HPEVAMon-1.11.egg
    zenoss restart

### Developer Installation (link mode)
If you wish to further develop and possibly contribute back to the HPEVAMon
ZenPack you should clone the [git repository][], then install the ZenPack in
developer mode using the following commands.

    git clone git://github.com/epuzanov/ZenPacks.community.HPEVAMon.git
    zenpack --link --install ZenPacks.community.HPEVAMon
    zenoss restart


## Usage
 1. You should now have CIM/HPEVA device class.
 1. Click on the HPEVA class and select Details.
 1. Click Configuration Properties on the left.
 1. In the right pane, scroll to the bottom and in the __zWbemProxy__ field add
the IP address or hostname of the EVA Command View server. The reason for this
is that you'ere going to use the EVA server as a boker to grab data regarding
the EVAs themselves, hence you request data about an EVA using it's WWN and
that request is fired at the Command View IP/Hostname.
 1. In the __zWinPassword__ and __zWinUser__ add the correct credentials of a
user account that can access the server.  (possibly create a new user account
in AD and add this account to the CV server)
 1. Hit Save.
 1. Click on See All at the top of the left pane.
 1. Still in the HPEVA class click on the icon at the top of the main pane to
add a new single device. Use Command View get the WWN of your EVA and paste
into the Hostname or IP field and click Add.
 1. Give Zenoss a chance to perform the Add Job, when I first added our EVA the
Job service was down and needed starting.
 1. Once the device has been added, go into it and from the icon on the bottom
left select Model Device. At this point I had issues with Zenoss connecting to
Zenhub and got timeout errors. It eventually reconnected and carried on
sometimes it didn't, just restart the modelling if it fails but give it a
chance to retry.
 1. Once the modelling has completed you should then see a load of objects in
the Components menu in the left pane as well as a new hardware tab where the
graphical disk view can be found.

Graphing should start almost immediately, you may need to soom in to see it
starting. I may have seen an issue involving the renaming of the device from
the WWN where graphing stops after the rename...well that's what appears to
have happened....so rename at your peril!

The following elements are discovered:

 * Storage Controllers (Status and Performance)
 * Storage Enclosures (Status Only)
 * Physical Disks (Status and Performance)
 * Storage Groups (Status and Performance)
 * Data Replication Groups  (Status and Performance)
 * Virtual Disks (Status and Performance)
 * Host FC Ports (Status and Performance)
 * Disk FC Ports (Status Only)


[Zenoss]: <http://www.zenoss.com/>
[HPEVAMon ZenPack]: <http://community.zenoss.org/docs/DOC-5867>
[WBEMDataSource ZenPack]: <http://community.zenoss.org/docs/DOC-3409>
[git repository]: <https://github.com/epuzanov/ZenPacks.community.HPEVAMon>

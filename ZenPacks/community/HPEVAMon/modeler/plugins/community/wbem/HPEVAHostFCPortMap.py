################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAHostFCPortMap

HPEVAHostFCPortMap maps HPEVA_HostFCPort class to HPEVAHostFCPort class.

$Id: HPEVA_HostFCPortMap.py,v 1.3 2011/06/03 21:49:18 egor Exp $"""

__version__ = '$Revision: 1.3 $'[11:-2]


from ZenPacks.community.WBEMDataSource.WBEMPlugin import WBEMPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class HPEVAHostFCPortMap(WBEMPlugin):
    """Map HPEVA_HostFCPort class to HostFCPort"""

    maptype = "HPEVAHostFCPortMap"
    modname = "ZenPacks.community.HPEVAMon.HPEVAHostFCPort"
    relname = "fcports"
    compname = "hw"
    deviceProperties = WBEMPlugin.deviceProperties + ('snmpSysName',)

    tables = {
            "HPEVA_HostFCPort":
                (
                "CIM_FCPort",
                None,
                "root/eva",
                    {
                    "__path":"snmpindex",
                    "ActiveFC4Types":"fc4Types",
                    "CreationClassName":"_ccn",
                    "Description":"description",
                    "DeviceID":"id",
                    "Caption":"interfaceName",
                    "FullDuplex":"fullDuplex",
                    "LinkTechnology":"linkTechnology",
                    "NetworkAddresses":"networkAddresses",
                    "PermanentAddress":"wwn",
                    "PortType":"type",
                    "Speed":"speed",
                    "SupportedMaximumTransmissionUnit":"mtu",
                    "SystemName":"setController",
                    },
                ),
            }

    linkTypes = {
        0:'Unknown',
        1: 'Other',
        2: 'Ethernet',
        3: 'IB',
        4: 'FC',
        5: 'FDDI',
        6: 'ATM',
        7: 'Token Ring',
        8: 'Frame Relay',
        9: 'Infrared',
        10: 'Bluetooth',
        11: 'Wireless LAN',
    }

    portTypes = {
        0: "Unknown",
        1: "Other",
        10: "N",
        11: "NL",
        12: "F/NL",
        13: "Nx",
        14: "E",
        15: "F",
        16: "FL",
        17: "B",
        18: "G",
    }

    fcTypes = {
        0: "Unknown",
        1: "Other",
        4: "ISO/IEC 8802 - 2 LLC",
        5: "IP over FC",
        8: "SCSI - FCP",
        9: "SCSI - GPP",
        17: "IPI - 3 Master",
        18: "IPI - 3 Slave",
        19: "IPI - 3 Peer",
        21: "CP IPI - 3 Master",
        22: "CP IPI - 3 Slave",
        23: "CP IPI - 3 Peer",
        25: "SBCCS Channel",
        26: "SBCCS Control Unit",
        27: "FC-SB-2 Channel",
        28: "FC-SB-2 Control Unit",
        32: "Fibre Channel Services (FC-GS, FC-GS-2, FC-GS-3)",
        34: "FC-SW",
        36: "FC - SNMP",
        64: "HIPPI - FP",
        80: "BBL Control",
        81: "BBL FDDI Encapsulated LAN PDU",
        82: "BBL 802.3 Encapsulated LAN PDU",
        88: "FC - VI",
        96: "FC - AV",
        255: "Vendor Unique"
    }

    def process(self, device, results, log):
        """collect WBEM information from this device"""
        log.info("processing %s for device %s", self.name(), device.id)
        rm = self.relMap()
        sysname = getattr(device,"snmpSysName","") or device.id.replace("-","")
        for instance in results.get("HPEVA_HostFCPort", []):
            if not instance["setController"].startswith(sysname): continue
            try:
                om = self.objectMap(instance)
                om.id = self.prepId(om.id)
                if om._ccn == 'HPEVA_DiskFCPort':
                    self.modname = "ZenPacks.community.HPEVAMon.HPEVADiskFCPort"
                if om.setController: om.setController = om.setController.strip()
                if om.interfaceName:om.interfaceName=om.interfaceName.split()[-1]
                om.type = self.portTypes.get(getattr(om, "type", 0), "Unknown")
                om.linkTechnology = self.linkTypes.get(getattr(om,
                                            "linkTechnology", 0), "Unknown")
                om.fc4Types = [self.fcTypes.get(t, "Unknown") \
                                        for t in getattr(om, "fc4Types", [])]
            except AttributeError:
                continue
            rm.append(om)
        return rm

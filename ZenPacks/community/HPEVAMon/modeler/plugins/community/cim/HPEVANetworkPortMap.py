################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVANetworkPortMap

HPEVANetworkPortMap maps HPEVA_NetworkPort class to CIM_NetworkPort class.

$Id: HPEVANetworkPortMap.py,v 1.5 2012/02/22 00:07:51 egor Exp $"""

__version__ = '$Revision: 1.5 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMNetworkPortMap \
    import CIMNetworkPortMap

class HPEVANetworkPortMap(CIMNetworkPortMap):
    """Map HPEVA_DiskFCPort and HPEVA_HostFCPort classes to CIM_NetworkPort class"""

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_NetworkPort":
                (
                    "SELECT * FROM CIM_NetworkPort",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "description":"Description",
                        "mtu":"ActiveMaximumTransmissionUnit",
                        "interfaceName":"ElementName",
                        "adminStatus":"EnabledDefault",
                        "operStatus":"EnabledState",
                        "type":"LinkTechnology",
                        "macaddress":"PermanentAddress",
                        "speed":"Speed",
                        "_sysname":"SystemName",
                    }
                ),
            "CIM_SystemComponent":
                (
                    "SELECT GroupComponent,PartComponent FROM HPEVA_SystemDevice",
                    None,
                    cs,
                    {
                        "gc":"GroupComponent", # System
                        "pc":"PartComponent", # SystemComponent
                    },
                ),
            "CIM_ElementStatisticalData":
                (
                    "SELECT ManagedElement,Stats FROM HPEVA_HostFCPortElementStatisticalData",
                    None,
                    cs,
                    {
                        "me":"ManagedElement",
                        "stats":"Stats",
                    },
                ),
            }

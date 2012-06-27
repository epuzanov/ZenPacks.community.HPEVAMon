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

$Id: HPEVANetworkPortMap.py,v 1.7 2012/06/27 19:50:24 egor Exp $"""

__version__ = '$Revision: 1.7 $'[11:-2]

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
                    "SELECT __PATH,ActiveMaximumTransmissionUnit,Description,DeviceID,ElementName,EnabledDefault,EnabledState,LinkTechnology,PermanentAddress,Speed,SystemName FROM CIM_NetworkPort",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "mtu":"ActiveMaximumTransmissionUnit",
                        "description":"Description",
                        "_deviceid":"DeviceID",
                        "interfaceName":"ElementName",
                        "adminStatus":"EnabledDefault",
                        "operStatus":"EnabledState",
                        "type":"LinkTechnology",
                        "macaddress":"PermanentAddress",
                        "speed":"Speed",
                        "_sysname":"SystemName",
                    }
                ),
            }

    def _getController(self, results, inst):
        return 'HPEVA_StorageProcessorSystem.Name="%s  ",CreationClassName="HPEVA_StorageProcessorSystem"'%inst.get("_sysname")

    def _getStatPath(self, results, inst):
        if not str(inst.get("setPath")).startswith("HPEVA_HostFCPort"):
            return ""
        return 'HPEVA_HostFCPortStatisticalData.InstanceID="%s.%s"'%(
            inst.get("_sysname"),inst.get("_deviceid"))

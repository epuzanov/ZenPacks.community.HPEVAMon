################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAComputerSystemMap

HPEVAComputerSystemMap maps HPEVA_ComputerSystem class to CIM_ComputerSystem class.

$Id: HPEVAComputerSystemMap.py,v 1.3 2012/10/17 18:21:15 egor Exp $"""

__version__ = '$Revision: 1.3 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMComputerSystemMap \
    import CIMComputerSystemMap

class HPEVAComputerSystemMap(CIMComputerSystemMap):
    """Map HPEVA_ComputerSystem CIM class to CIM_ComputerSystem class"""

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_ComputerSystem":
                (
                    "SELECT __PATH,Description,ElementName,FirmwareVersion,Name,PrimaryOwnerContact,OperationalStatus FROM HPEVA_StorageSystem",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "_descr":"Description",
                        "title":"ElementName",
                        "FWRev":"FirmwareVersion",
                        "_sysname":"Name",
                        "_contact":"PrimaryOwnerContact",
                        "status":"OperationalStatus",
                    },
                ),
            "CIM_PhysicalPackage":
                (
                    "SELECT __PATH,Manufacturer,Model,Replaceable,SerialNumber,Tag,Version FROM HPEVA_PhysicalPackage",
                    None,
                    cs,
                    {
                        "_pPath":"__PATH",
                        "_manuf":"Manufacturer",
                        "setProductKey":"Model",
                        "serialNumber":"SerialNumber",
                        "tag":"Tag",
                    },
                ),
            }

    def _getPackage(self, results, inst):
        sysname = inst.get("_sysname")
        if not sysname: return {}
        for pack in results.get("CIM_PhysicalPackage") or ():
            if sysname == str(pack.get("tag")): break
        else: pack = {}
        return pack

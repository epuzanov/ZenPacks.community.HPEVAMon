################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAStorageDiskEnclosureMap

HPEVAStorageDiskEnclosureMap maps HPEVA_StorageDiskEnclosure class to
CIM_Chassis class.

$Id: HPEVAStorageDiskEnclosureMap.py,v 1.5 2012/06/22 00:08:59 egor Exp $"""

__version__ = '$Revision: 1.5 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMChassisMap \
    import CIMChassisMap

class HPEVAStorageDiskEnclosureMap(CIMChassisMap):
    """Map HPEVA_StorageDiskEnclosure CIM class to CIM_Chassis class"""

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_Chassis":
                (
                    "SELECT * FROM HPEVA_StorageDiskEnclosure",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "_cptype":"ChassisPackageType",
                        "title":"ElementName",
                        "_manuf":"Manufacturer",
                        "setProductKey":"Model",
                        "serialNumber":"SerialNumber",
                        "_pn":"PartNumber",
                        "id":"Tag",
                        "_sysname":"Tag",
                    },
                ),
            "CIM_SystemComponent":
                (
                    "SELECT GroupComponent,PartComponent FROM HPEVA_ComponentCS",
                    None,
                    cs,
                    {
                        "gc":"GroupComponent", # System
                        "pc":"PartComponent", # SystemComponent
                    },
                ),
            "CIM_ComputerSystemPackage":
                (
                    "SELECT Antecedent,Dependent FROM HPEVA_EnclosureComputerSystemPackage",
                    None,
                    cs,
                    {
                        "ant":"Antecedent", # Chassis
                        "dep":"Dependent", # ComputerSystem
                    },
                ),
            "HPEVA_StorageSystem":
                (
                    "SELECT * FROM HPEVA_StorageSystem",
                    None,
                    cs,
                    {
                        "model":"Model",
                        "name":"Name",
                    },
                ),
            }

    def _isSystemChassis(self, results, sysname, inst):
        return False

    def _getLayout(self, results, inst):
        model = inst.get("setProductKey")
        if model not in ("M5314A", "M5314C", "M6412A"):
            sysname = inst.get("_sysname").split(".", 1)[0]
            for ssys in results.get("HPEVA_StorageSystem") or ():
                if ssys.get("name") != sysname: break
            else: ssys = {"model":"Unknown"}
            sysmodel = ssys.get("model")
            if sysmodel in ("HSV300", "HSV400", "HSV450"):
                model = "M6412A"
            elif sysmodel in ("HSV200-B", "HSV210-B", "HSV200B", "HSV210B"):
                model = "M5314C"
            else:
                model = "M5314A"
            inst["setProductKey"] = model
        return {"M6412A":"h1 4 7 10,2 5 8 11,3 6 9 12",
                "M5314A":"h1 4 7 10,2 5 8 11,3 6 9 12",
                "M5314C":"h1 4 7 10,2 5 8 11,3 6 9 12",
                }.get(model) or "v1 2 3 4 5 6 7 8 9 10 11 12 13 14"

################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVADiskDriveMap

HPEVADiskDriveMap maps HPEVA_DiskDrive class to CIM_DiskDrive class.

$Id: HPEVADiskDriveMap.py,v 1.3 2012/06/22 00:07:14 egor Exp $"""

__version__ = '$Revision: 1.3 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMDiskDriveMap \
    import CIMDiskDriveMap
import re
CAPTIONPAT = re.compile(r'^Shelf (\d*), Disk Bay (\d*), Disk Group (.*)$')

class HPEVADiskDriveMap(CIMDiskDriveMap):
    """Map CIM_DiskDrive CIM class to HardDisk class"""

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_DiskDrive":
                (
                    "SELECT * FROM HPEVA_DiskDrive",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "id":"DeviceID",
                        "diskType":"DriveType",
                        "formFactor":"FormFactor",
                        "size":"MaxMediaSize",
                        "description":"ElementName",
                        "title":"ElementName",
                        "setProductKey":"Model",
                        "bay":"Caption",
                        "_sysname":"SystemName",
                    }
                ),
            "CIM_PhysicalPackage":
                (
                    "SELECT * FROM HPEVA_DiskModule",
                    None,
                    cs,
                    {
                        "_pPath":"__PATH",
                        "_manuf":"Manufacturer",
                        "setProductKey":"Model",
                        "replaceable":"Replaceable",
                        "serialNumber":"SerialNumber",
                        "FWRev":"Version",
                    },
                ),
            "CIM_StoragePool":
                (
                    "SELECT * FROM CIM_StoragePool",
                    None,
                    cs,
                    {
                        "_path":"__PATH",
                        "_primordial":"Primordial",
                        "name":"Name",
                    },
                ),
            "CIM_SystemComponent":
                (
                    "SELECT GroupComponent,PartComponent FROM HPEVA_DiskDriveSystemDevice",
                    None,
                    cs,
                    {
                        "gc":"GroupComponent", # System
                        "pc":"PartComponent", # SystemComponent
                    },
                ),
            "CIM_Realizes":
                (
                    "SELECT Antecedent,Dependent FROM HPEVA_DiskModuleRealizes",
                    None,
                    cs,
                    {
                        "ant":"Antecedent", # PhysicalPackage
                        "dep":"Dependent", # DiskDrive
                    },
                ),
            "CIM_Container":
                (
                    "SELECT GroupComponent,PartComponent FROM HPEVA_DiskEnclosureModule",
                    None,
                    cs,
                    {
                        "gc":"GroupComponent", # Enclosure
                        "pc":"PartComponent", # PhysicalPackage
                    },
                ),
            "CIM_ElementStatisticalData":
                (
                    "SELECT ManagedElement,Stats FROM HPEVA_DiskDriveElementStatisticalData",
                    None,
                    cs,
                    {
                        "me":"ManagedElement",
                        "stats":"Stats",
                    },
                ),
            }

    def _diskTypes(self, diskType):
        return str(diskType).strip().lower()

    def _diskTypeImg(self, diskType):
        return {"online":"scsi",
                "nearonline":"ata",
                "ssd":"ssd",
                }.get(str(diskType).strip().lower()) or "scsi"

    def _formFactors(self, formFactor):
        return "lff"

    def _getPackage(self, results, inst):
        package = self._findInstance(results, "CIM_PhysicalPackage", "_pPath",
                    self._findInstance(results, "CIM_Realizes", "dep",
                    inst.get("setPath")).get("ant"))
        r = CAPTIONPAT.match(str(inst.get("bay")))
        if r:
            package["bay"] = int(r.group(2))
            package["setStoragePool"] = r.group(3)
        return package

    def _getPool(self, results, inst):
        spName = inst.get("setStoragePool")
        if not spName: return ""
        sysname = inst.get("_sysname") or ""
        for sp in results.get("CIM_StoragePool") or ():
            spPath = sp.get("_path") or "rimordial"
            if sysname not in spPath: continue
            if str(sp.get("_primordial")).lower() == "true": continue
            if "rimordial" in spPath: continue
            if sp.get("name") == spName: break
        else: spPath = ""
        return spPath

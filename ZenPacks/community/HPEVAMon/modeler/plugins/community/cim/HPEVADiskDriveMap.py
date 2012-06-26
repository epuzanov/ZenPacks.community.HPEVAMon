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

$Id: HPEVADiskDriveMap.py,v 1.4 2012/06/26 23:37:50 egor Exp $"""

__version__ = '$Revision: 1.4 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMDiskDriveMap \
    import CIMDiskDriveMap
import re
CAPTIONPAT = re.compile(r'^Shelf (?P<setChassis>\d*), Disk Bay (?P<bay>\d*), Disk Group (?P<setStoragePool>.*)$')

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
                    "SELECT __PATH,Caption,DeviceID,DriveType,ElementName,FormFactor,MaxMediaSize,Model,Name,SystemName FROM HPEVA_DiskDrive",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "bay":"Caption",
                        "id":"DeviceID",
                        "diskType":"DriveType",
                        "description":"ElementName",
                        "title":"ElementName",
                        "formFactor":"FormFactor",
                        "size":"MaxMediaSize",
                        "setProductKey":"Model",
                        "_diskname":"Name",
                        "_sysname":"SystemName",
                    }
                ),
            "CIM_PhysicalPackage":
                (
                    "SELECT __PATH,Manufacturer,Model,Replaceable,SerialNumber,Tag,Version FROM CIM_PhysicalPackage",
                    None,
                    cs,
                    {
                        "_pPath":"__PATH",
                        "_manuf":"Manufacturer",
                        "setProductKey":"Model",
                        "replaceable":"Replaceable",
                        "serialNumber":"SerialNumber",
                        "tag":"Tag",
                        "FWRev":"Version",
                    },
                ),
            "CIM_StoragePool":
                (
                    "SELECT __PATH,ActualDiskFailureProtectionLevel,DiskGroupType,DiskType,ElementName,InstanceID,Name,PoolID,Primordial,TotalManagedSpace,Usage FROM HPEVA_StoragePool",
                    None,
                    cs,
                    {
                        "_path":"__PATH",
                        "_primordial":"Primordial",
                        "name":"Name",
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
        tag = ".".join((str(inst.get("_sysname")),str(inst.get("_diskname"))))
        for package in results.get("CIM_PhysicalPackage") or ():
            if package.get("tag") == tag: break
        else: package = {}
        r = CAPTIONPAT.match(str(inst.get("bay")))
        if r:
            package.update(r.groupdict())
        return package

    def _getBay(self, results, inst):
        return int(inst.get("bay") or -1)

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

    def _getChassis(self, results, inst):
        try:
            sName = int(inst.get("setChassis"))
        except Exception:
            return ""
        return 'HPEVA_StorageDiskEnclosure.Tag="%s.\\Hardware\\Disk Enclosure %s",CreationClassName="HPEVA_StorageDiskEnclosure"'%(
            inst.get("_sysname"), sName)

    def _getStatPath(self, results, inst):
        return 'HPEVA_DiskDriveStatisticalData.InstanceID="%s.%s"'%(
            inst.get("_sysname"),inst.get("_diskname"))

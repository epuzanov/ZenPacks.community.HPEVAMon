################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAStorageVolumeMap

HPEVAStorageVolumeMap maps HPEVA_StorageVolume class to CIM_StorageVolume class.

$Id: HPEVAStorageVolumeMap.py,v 1.5 2012/06/22 00:10:05 egor Exp $"""

__version__ = '$Revision: 1.5 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMStorageVolumeMap \
    import CIMStorageVolumeMap

class HPEVAStorageVolumeMap(CIMStorageVolumeMap):
    """Map HPEVA_StorageVolume CIM class to CIM_StorageVolume class"""

    modname = "ZenPacks.community.HPEVAMon.HPEVA_StorageVolume"

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_StorageVolume":
                (
                    "SELECT * FROM HPEVA_StorageVolume",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "accessType":"Access",
                        "blockSize":"BlockSize",
                        "id":"DeviceID",
                        "title":"ElementName",
                        "diskType":"raidType",
                        "mirrorCache":"MirrorCache",
                        "preferredPath":"PreferredPath",
                        "readCachePolicy":"ReadCachePolicy",
                        "writeCachePolicy":"WriteCachePolicy",
                        "setStoragePool":"DiskGroupID",
                        "_sysname":"SystemName",
                    },
                ),
            "CIM_SystemComponent_remove":
                (
                    "SELECT GroupComponent,PartComponent FROM HPEVA_StorageVolumeSystemDevice",
                    None,
                    cs,
                    {
                        "gc":"GroupComponent", # System
                        "pc":"PartComponent", # SystemComponent
                    },
                ),
            "CIM_AllocatedFromStoragePool_remove":
                (
                    "SELECT Antecedent,Dependent FROM HPEVA_VolumeAllocatedFromStoragePool",
                    None,
                    cs,
                    {
                        "ant":"Antecedent",
                        "dep":"Dependent",
                    },
                ),
            "CIM_MemberOfCollection":
                (
                    "SELECT Member,Collection FROM HPEVA_OrderedMemberOfCollection",
                    None,
                    cs,
                    {
                        "member":"Member",
                        "collection":"Collection",
                    },
                ),
            "CIM_ElementStatisticalData":
                (
                    "SELECT ManagedElement,Stats FROM HPEVA_VolumeElementStatisticalData",
                    None,
                    cs,
                    {
                        "me":"ManagedElement",
                        "stats":"Stats",
                    },
                ),
            }

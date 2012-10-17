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

$Id: HPEVAStorageVolumeMap.py,v 1.8 2012/10/17 18:24:27 egor Exp $"""

__version__ = '$Revision: 1.8 $'[11:-2]

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
                    "SELECT __PATH,Access,BlockSize,DeviceID,DiskGroupID,ElementName,MirrorCache,Name,NumberOfBlocks,PreferredPath,raidType,ReadCachePolicy,SystemName,WriteCachePolicy,OperationalStatus FROM HPEVA_StorageVolume",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "accessType":"Access",
                        "blockSize":"BlockSize",
                        "id":"DeviceID",
                        "setStoragePool":"DiskGroupID",
                        "title":"ElementName",
                        "mirrorCache":"MirrorCache",
                        "_diskname":"Name",
                        "totalBlocks":"NumberOfBlocks",
                        "preferredPath":"PreferredPath",
                        "diskType":"raidType",
                        "readCachePolicy":"ReadCachePolicy",
                        "_sysname":"SystemName",
                        "writeCachePolicy":"WriteCachePolicy",
                        "status":"OperationalStatus",
                    },
                ),
            "CIM_MemberOfCollection":
                (
                    "SELECT Member,Collection FROM CIM_MemberOfCollection",
                    None,
                    cs,
                    {
                        "member":"Member",
                        "collection":"Collection",
                    },
                ),
            }

    def _getStatPath(self, results, inst):
        return 'HPEVA_VolumeStatisticalData.InstanceID="%s.%s"'%(
            inst.get("_sysname"),inst.get("_diskname"))

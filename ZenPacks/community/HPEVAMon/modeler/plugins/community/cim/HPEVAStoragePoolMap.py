################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAStoragePoolMap

HPEVAStoragePoolMap maps HPEVA_StoragePool class to CIM_StoragePool class.

$Id: HPEVAStoragePoolMap.py,v 1.5 2012/06/22 00:09:36 egor Exp $"""

__version__ = '$Revision: 1.5 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMStoragePoolMap \
    import CIMStoragePoolMap

class HPEVAStoragePoolMap(CIMStoragePoolMap):
    """Map HPEVA_StoragePool CIM class to CIM_StoragePool class"""

    modname = "ZenPacks.community.HPEVAMon.HPEVA_StoragePool"

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_StoragePool":
                (
                    "SELECT * FROM HPEVA_StoragePool",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "id":"InstanceID",
                        "title":"ElementName",
                        "poolId":"PoolID",
                        "_primordial":"Primordial",
                        "totalManagedSpace":"TotalManagedSpace",
                        "usage":"Usage",
                        "protLevel":"ActualDiskFailureProtectionLevel",
                        "diskGroupType":"DiskGroupType",
                        "diskType":"DiskType",
                        "_sysname":"InstanceID",
                    },
                ),
            "CIM_SystemComponent":
                (
                    "SELECT GroupComponent,PartComponent FROM HPEVA_HostedStoragePool",
                    None,
                    cs,
                    {
                        "gc":"GroupComponent", # System
                        "pc":"PartComponent", # SystemComponent
                    },
                ),
            }

